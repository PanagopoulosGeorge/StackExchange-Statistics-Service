from flask import Flask, request, jsonify
from datetime import datetime
from .components import statistics
from flask_caching import Cache
from decouple import config
import time
import sys
app = Flask(__name__)
stat_client = statistics.StackStatsCalculator()

cache = Cache()
app.config['CACHE_TYPE'] = 'simple'                                         # Set the cache type
app.config['CACHE_DEFAULT_TIMEOUT'] = config('CACHE_DEFAULT_TIMEOUT', 1800) # Set the default cache timeout in seconds
app.config['CACHE_KEY_PREFIX'] = 'stackstats'                               # Set the cache key prefix
cache.init_app(app)

@cache.cached(timeout=1800) # Cache results for half an hour
@app.route('/api/v1/stackstats', methods=['GET'])
def get_stack_stats():
    
    since_str = request.args.get('since')
    until_str = request.args.get('until')
    if not since_str or not until_str:
        return jsonify({"error": "Missing 'since' or 'until' parameters"}), 400
    try:
        since_dt = datetime.strptime(since_str, '%Y-%m-%d %H:%M:%S')
        until_dt = datetime.strptime(until_str, '%Y-%m-%d %H:%M:%S')
        since_unix = int(since_dt.timestamp())
        until_unix = int(until_dt.timestamp())
    except ValueError:
        return jsonify({"error": "Invalid datetime format. Use 'YYYY-MM-DD HH:MM:SS'"}), 400
    if since_dt >= until_dt:
        return jsonify({"error": "'since' datetime must be earlier than 'until' datetime"}), 400
    # Pass the parsed datetime objects to get_answers
    ## if timer starts from here ~ 500 ms (for mock - public gist) and > 1000 ms for an 1-hour API call
    start = time.time()
    stat_client.answers = stat_client.stackexchange_client.get_answers(start_date_unix=since_unix,
                                                                       end_date_unix=until_unix, mock_api=False)
    if "error" in stat_client.answers:
        return jsonify(stat_client.answers), 400
    
    ## if timer starts from here < 300 ms
    result = stat_client.compute()
    end = time.time()
    ms_elapsed = (end - start) * 1000
    print("Time elapsed: ", ms_elapsed)
    return jsonify(result), 200

if __name__ == '__main__':
    arg1 = sys.argv[1]
    debug = True if arg1 == '--debug' else False
    app.run(debug=debug, port=5000, host='0.0.0.0')