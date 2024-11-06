import requests


class GoogleBooksAPI:
    def __init__(self, api_key = None):
        self.api_key = api_key
        self.base_url = "https://www.googleapis.com/books/v1/volumes"

    def search(self, query, lang='en', start_index=0, max_results=40, fields=None):
        try:
            if fields:
                fields = ','.join(fields)
            params = {
                'q': query,
                # 'key': self.api_key,
                'langRestrict': lang,
                'startIndex': start_index,
                'maxResults': max_results,
                'fields':fields
            }
            if self.api_key:
                params['key'] = self.api_key
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            return response.json(), response.url
        except requests.exceptions.HTTPError as http_err:
            return {'error': str(http_err)}
        except Exception as err:
            return {'error': str(err)}
