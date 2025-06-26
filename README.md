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
 6. Cache the results for faster repeated retrievals.
 7. Statistical measures will be rounded to three decimals. 
 
  #### Non-Functional Requirements 
  1. Python version: >=3.6

### Key Components

#### Structure
```aiignore
src/
├── app/
│   ├── components/
│   │   ├── stackexchange.py     # StackExchange API integration
        ├── rate_limits.py       # Comply with tha rate limitations of the Stackexchange API
        ├── statistics.py        # Statistics calculations
notebooks/
│   ├── stackexchange_notebook.ipynb # demo - tests
├── .gitignore
├── requirements.txt            # Python dependencies
└── README.md                   # Project documentation
```

#### Stackexchange API Client
- **`src/app/components/stackexchange.py`**: Contains the `StackExchangeClient` class for interacting with the StackExchange API. It supports fetching answers and comments with pagination and batching.
- **`notebooks/stackexchange_notebook.ipynb`**: A Jupyter Notebook demonstrating the usage of the `StackExchangeClient` and testing its functionality.
- **`TODO:`**: Add routines to validate API responses. 

#### Statistics Calculation
- **`src/app/components/statistics.py`**: Contains the `StatisticsCalculator` class for calculating statistics based on the retrieved StackOverflow data. It includes methods for calculating accepted answers, average scores, and comment counts for top answers.
- **`StatisticsCalculator.compute() method:`** Takes a list of answer ids and returns a dictionary with the calculated statistics.

#### Flask app
- **`src/app/run.py`**: Contains a simple endpoint for getting the response from the calculations.