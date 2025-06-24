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

### Key Components - Stackexchange API Client
- **`src/app/components/stackexchange.py`**: Contains the `StackExchangeClient` class for interacting with the StackExchange API. It supports fetching answers and comments with pagination and batching.
- **`notebooks/stackexchange_notebook.ipynb`**: A Jupyter Notebook demonstrating the usage of the `StackExchangeClient` and testing its functionality.
- **`.gitignore`**: Specifies files and directories to be ignored by Git.
- **`requirements.txt`**: Lists Python dependencies required for the project.
- **`README.md`**: Documentation for the project.