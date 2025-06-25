import requests

def _make_paginated_request(url: str, params: dict):
    """
    Handle paginated API requests.
    """
    results = []
    has_more = True
    page = 1

    while has_more:
        params["page"] = page
        try:
            response = requests.get(url, params=params)
            response.raise_for_status()
        except requests.RequestException as e:
            if page >= 24:
                print(f"Error: Too large date range requested (page: {page}), stopping further requests.")
                print("Error: an API Key may be required for large requests.")
            print(f"Error fetching data from StackExchange API, url:{url}, page: {page} : {e}")
            return []
        data = response.json()
        results.extend(data.get("items", []))
        has_more = data.get("has_more", False)
        page += 1

    return results

class StackExchangeClient:
    """
    Handles integration with the StackExchange API for retrieving answers and comments.
    """
    BASE_URL = "https://api.stackexchange.com/2.3/"
    ANSWERS_URL = f"{BASE_URL}answers"
    SITE = "stackoverflow"
    PAGESIZE = 100

    def get_answers(self, since, until):
        """
        Fetches answers from StackExchange within the specified date range.
        Params:
            - since (int): Start date as a Unix timestamp.
            - until (int): End date as a Unix timestamp.
        Returns:
            - List of answers with relevant details.
        """
        url = self.ANSWERS_URL
        params = {
            "fromdate": since,
            "todate": until,
            "site": self.SITE,
            "pagesize": self.PAGESIZE,
            "order": "asc",
            "sort": "creation"
        }
        return _make_paginated_request(url, params)

    def get_comments(self, answer_ids: list, batch_size: int = 90):
        """
        Fetches comments for a specific answer.
        Params:
            - answer_ids (list): The IDs of the answer to fetch comments for.
        Returns:
            - List of comments associated with the answer(s).
        """
        def _get_comments_for_batch(batch):
            concatenated_ids = ";".join(map(str, batch))

            url = f"{self.ANSWERS_URL}/{concatenated_ids}/comments"
            params = {
                "order": "asc",
                "sort": "creation",
                "site": self.SITE
            }
            return _make_paginated_request(url, params)

        if not answer_ids:
            return []
        if len(answer_ids) <= batch_size:
            return _get_comments_for_batch(answer_ids)
        else:
            print(f"Warning: Too many answer IDs provided ({len(answer_ids)}), switch to batch mode with batch size {batch_size}.")
        comments = []
        for i in range(0, len(answer_ids), batch_size):
            batch = answer_ids[i:i + batch_size]
            comments.extend(_get_comments_for_batch(batch))
        return comments