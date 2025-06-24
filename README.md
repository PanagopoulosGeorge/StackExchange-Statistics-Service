# StackExchange-Statistics-Service
a Python-based REST API service that retrieves data from the StackExchange API, calculates specific statistics, and reports the results.

### Project Goals
 - Provide a REST API endpoint to retrieve StackOverflow answer data within a specified date/time range.
 - Calculate and return specific statistics based on the retrieved data.

 #### Functional Requirements 
 1. Expose a REST API endpoint at:
GET http://localhost:5000/api/v1/stackstats?since=<datetime>&until=<datetime>
 2. Accept two datetime parameters (since and until) in the format:
YYYY-MM-DD HH:MM:SS
 3. Retrieve StackOverflow answers within the specified date/time range using the StackExchange API (1st call).
 4. Retrieve comments associated with these answers (2nd call).
 5. Calculate the following:
    * Total number of **accepted** answers.
    * Average score of the **accepted** answers.
    * Average answer count per question.
    * Comment count for each of the top 10 answers with the highest scores.
 6. Cache the results for faster reapeated retrievals.
 
  #### Non-Functional Requirements 
  1. Python version: >=3.6

### Project structure:
```
src/
├── app/
│   ├── main.py                 # REST API entry point
│   ├── components/
│   │   ├── stackexchange.py    # StackExchange API integration
│   │   └── statistics.py       # Statistics calculation logic
│   ├── cache/
│   │   └── cache.py            # Caching logic
│   └── utils/
│       └── helpers.py          # Utility functions
├── tests/
│   ├── test_api.py             # API endpoint tests
│   ├── test_services.py        # Business logic tests
│   └── test_cache.py           # Cache tests
├── Dockerfile                  # Docker container definition
├── requirements.txt            # Python dependencies
└── README.md                   # Project documentation
```
