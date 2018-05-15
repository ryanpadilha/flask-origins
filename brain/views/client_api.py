import json
import requests

from flask import current_app as app


API_BASE_URL = 'http://0.0.0.0:9000'
API_TIMEOUT = 120

API_HEADERS = {
    'xf-api-key': '',
    'xf-client-secret': '+h7Wz5wMF:%K%ad%@`'
}

API = {}


class IntegrationResource(object):
    def __init__(self, url):
        self.url = url

    def get(self, **kwargs):
        try:
            result = []
            r = requests.get(url=self.url, headers=API_HEADERS, allow_redirects=False, timeout=API_TIMEOUT, **kwargs)
            r.raise_for_status()

            if r.content:
                result = json.loads(r.content.decode('utf-8'))
        except requests.exceptions.Timeout as e:
            app.logger.error('Timeout Exception: {}'.format(e))
        except requests.exceptions.HTTPError as e:
            app.logger.error('HTTP Error Exception: {}'.format(e))
        except (requests.exceptions.TooManyRedirects, requests.exceptions.RequestException) as e:
            app.logger.error('Request Exception: {}'.format(e))

        return result

    def post(self, data=None, **kwargs):
        try:
            result = []
            if data:
                data = data.encode('utf-8')

            r = requests.post(url=self.url, data=data, headers=API_HEADERS,
                              allow_redirects=False, verify=False, **kwargs)
            r.raise_for_status()

            if r.content:
                result = json.loads(r.content.decode('utf-8'))
        except requests.exceptions.Timeout as e:
            app.logger.error('Timeout Exception: {}'.format(e))
        except requests.exceptions.HTTPError as e:
            app.logger.error('HTTP Error Exception: {}'.format(e))
        except (requests.exceptions.TooManyRedirects, requests.exceptions.RequestException) as e:
            app.logger.error('Request Exception: {}'.format(e))

        return result

    def put(self, data=None, **kwargs):
        try:
            result = []
            if data:
                data = data.encode('utf-8')

            r = requests.put(url=self.url, data=data, headers=API_HEADERS,
                             allow_redirects=False, verify=False, **kwargs)
            r.raise_for_status()

            if r.content:
                result = json.loads(r.content.decode('utf-8'))
        except requests.exceptions.Timeout as e:
            app.logger.error('Timeout Exception: {}'.format(e))
        except requests.exceptions.HTTPError as e:
            app.logger.error('HTTP Error Exception: {}'.format(e))
        except (requests.exceptions.TooManyRedirects, requests.exceptions.RequestException) as e:
            app.logger.error('Request Exception: {}'.format(e))

        return result

    def delete(self, data=None, **kwargs):
        try:
            result = []
            if data:
                data = data.encode('utf-8')

            r = requests.delete(url=self.url, data=data, headers=API_HEADERS,
                                allow_redirects=False, verify=False, **kwargs)
            r.raise_for_status()

            if r.content:
                result = json.loads(r.content.decode('utf-8'))
        except requests.exceptions.Timeout as e:
            app.logger.error('Timeout Exception: {}'.format(e))
        except requests.exceptions.HTTPError as e:
            app.logger.error('HTTP Error Exception: {}'.format(e))
        except (requests.exceptions.TooManyRedirects, requests.exceptions.RequestException) as e:
            app.logger.error('Request Exception: {}'.format(e))

        return result
