'''Gitlab CI variable manager API wrapper'''
import urllib
import requests

class GitlabDotenvAPI:
    '''Gitlab CI variable manager API wrapper'''
    def __init__(self, url, token):
        self.url = self._url_to_api_url(url)
        self.headers = {'PRIVATE-TOKEN': token}

    @staticmethod
    def _url_to_api_url(url):
        urlp = urllib.parse.urlparse(url)
        project_id = urllib.parse.quote_plus(urlp.path.lstrip("/"), safe='')
        return f'{urlp.scheme}://{urlp.netloc}/api/v4/projects/{project_id}/variables'

    def _generate_url(self, key, scope=None):
        safe_key = urllib.parse.quote_plus(key, safe='')
        url = f'{self.url}/{safe_key}'
        if scope is not None:
            url = f'{url}?filter[environment_scope]={scope}'
        return url

    def get_all(self):
        '''Get every CI variable'''
        page = '1'
        result = []
        while page.isnumeric():
            response = requests.get(f'{self.url}?per_page=100&page={page}', headers=self.headers)
            response.raise_for_status()
            result.extend(response.json())
            page = response.headers['X-Next-Page']
        return result

    def create(self, data):
        '''Create a CI variable'''
        response = requests.post(self.url, headers=self.headers, data=data)
        response.raise_for_status()
        return response.json()

    def get(self, key, scope=None):
        '''Get a CI variable'''
        response = requests.get(self._generate_url(key, scope), headers=self.headers)
        response.raise_for_status()
        return response.json()

    def update(self, key, data, scope=None):
        '''Update a CI variable'''
        response = requests.put(self._generate_url(key, scope), headers=self.headers, data=data)
        response.raise_for_status()
        return response.json()

    def delete(self, key, scope=None):
        '''Delete a CI variable'''
        response = requests.delete(self._generate_url(key, scope), headers=self.headers)
        response.raise_for_status()
