from typing import List, Dict, Optional
import requests
from decouple import config
from .rate_limits import rate_limited, throttle_backoff_limited
from cachetools import TTLCache, cached
from cachetools.keys import hashkey
"""
Rate Limits:
 - 30 requests/second per IP
 - 10,000 requests/day per API key --> (not covered, can acquire more keys and play with random.choice)
 - Dynamic backoff throttling per method: If an application receives a response with the backoff field set, it must wait that many seconds before hitting the same method again.
 - Heavy caching (don't repeat identical requests within 1 minute)
"""

MAX_PAGES = 24
DEFAULT_BATCH = 60 * 60 * 24 # 1 day
ANSWERS_SHORT_CACHING = TTLCache(maxsize=256, ttl=60)
COMMENTS_SHORT_CACHING = TTLCache(maxsize=256, ttl=60)

class StackExchangeError(Exception): ...

class StackExchangeClient:
    def __init__(self, api_key: Optional[str] = None, session: Optional[requests.Session] = None):
        self.__api_key = api_key or config("STACK_EXCHANGE_API_KEY", default=None)
        self.session = session or requests.Session(
        ## establish possibly a proxy or other configs
        )
        self.BASE_URL = "https://api.stackexchange.com/2.3"
        self.SITE = "stackoverflow"

    def get_answers(self, start_date_unix: int, end_date_unix: int,
                          batch: int = DEFAULT_BATCH, mock_api: bool = False) -> List[Dict]:
        """
        Retrieve answers from Stack Overflow within a specified date range.

        Args:
            start_date_unix (int): Start date as Unix timestamp for filtering answers
            end_date_unix (int): End date as Unix timestamp for filtering answers
            batch (int, optional): Batch size for API requests. Defaults to DEFAULT_BATCH.
            mock_api (bool, optional): If True, uses mock data instead of live API. Defaults to False.

        Returns:
            List[Dict]: List of answer dictionaries containing Stack Overflow answer data

        Raises:
            StackExchangeError: If API request fails or returns invalid data        
        """
        answers: List[Dict] = []
        if mock_api:
            url = "https://gist.githubusercontent.com/PanagopoulosGeorge/4a5b2c1304971e502d64a5c1b13248bb/raw/6b748538ebeb137597655514a7dd47547d387f35/gistfile1.txt"
            response = self.session.get(url)
            results = response.json()['items']
            return results
        for batch_start in self._iterate_batches(start_date_unix, end_date_unix, batch):
            batch_end = min(batch_start + batch - 1, end_date_unix)
            answers.extend(self._fetch_paginated(
                f"{self.BASE_URL}/answers",
                {
                    "site": self.SITE,
                    "fromdate": batch_start,
                    "todate":   batch_end,
                    "order": "asc",
                    "sort":  "creation",
                    **({"key": self.__api_key} if self.__api_key else {}),
                },
                object_to_fetch = 'answer'
            ))
        return answers

    def get_comments(self, answer_ids: List[int], batch_size: int = 90) -> List[Dict]:
        """
        Retrieve comments for a list of answer IDs from Stack Exchange API.

        Args:
            answer_ids (List[int]): List of answer IDs to fetch comments for
            batch_size (int, optional): Number of answer IDs to process in each batch. 
                                       Defaults to 90 to stay within API limits.

        Returns:
            List[Dict]: List of comment dictionaries containing comment data from the API

        Raises:
            StackExchangeError: If API request fails or returns an error        
        """
        comments: List[Dict] = []
        for i in self._iterate_batches(0, len(answer_ids), batch_size):
            ids = ";".join(map(str, answer_ids[i: i + batch_size]))
            url = f"{self.BASE_URL}/answers/{ids}/comments"
            comments.extend(self._fetch_paginated(url, {"site": self.SITE}, object_to_fetch = 'comment'))
        return comments

    @staticmethod
    def _iterate_batches(start: int, end: int, delta: int):
        cur = start
        while cur < end:
            yield cur
            cur += delta

    def _fetch_paginated(self, url: str, base_params: dict, object_to_fetch = 'answer') -> List[Dict]:
        """
        Fetch all items from a paginated StackExchange API endpoint.
                
                Args:
                    url (str): The API endpoint URL to fetch from
                    base_params (dict): Base parameters to include in all requests
                    object_to_fetch (str, optional): Type of object being fetched ('answer' or 'comment'). 
                                                Defaults to 'answer'.
                
                Returns:
                    List[Dict]: A list of all items retrieved from all pages of the API response
                
                Note:
                     - This method automatically handles pagination by incrementing the page parameter
                       until all available data has been retrieved.
        """
        items, page = [], 1
        while True:
            params = {**base_params, "page": page}
            data = self.__fetch(url, params=params, timeout=10, object_to_fetch = object_to_fetch)
            items.extend(data.get("items", []))
            if not data.get("has_more", False):
                break
            if page >= MAX_PAGES and not self.__api_key:
                raise StackExchangeError("Exceeded max page limit")
            page += 1
        return items

    @rate_limited(max_per_second=30)
    def __fetch(self, url, params=None, timeout=10, object_to_fetch='answer'):
        """
        Note:
            - This method redirects to the appropriate fetch method based on the object_to_fetch parameter, 
              in order to respect the per-endpoint api limitation.
        """
        data = self.__fetch_answer(url, params=params, timeout=timeout) if object_to_fetch == 'answer' else self.__fetch_comment(url, params=params, timeout=timeout)
        return data

    @throttle_backoff_limited
    @cached(cache=ANSWERS_SHORT_CACHING,
            key=lambda *args, **kwargs: hashkey(args[0], tuple(sorted(kwargs.get('params', {}).items()))))
    def __fetch_answer(self, url, params=None, timeout=10):
        response = self.session.get(url, params=params, timeout=timeout)
        try:
            response.raise_for_status()
        except requests.HTTPError as exc:
            raise StackExchangeError(str(exc)) from exc
        return response.json()


    @throttle_backoff_limited
    @cached(cache=COMMENTS_SHORT_CACHING,
            key=lambda *args, **kwargs: hashkey(args[0], tuple(sorted(kwargs.get('params', {}).items()))))

    def __fetch_comment(self, url, params=None, timeout=10):
        response = self.session.get(url, params=params, timeout=timeout)
        try:
            response.raise_for_status()
        except requests.HTTPError as exc:
            raise StackExchangeError(str(exc)) from exc
        return response.json()