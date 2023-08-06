import posixpath

from urllib.parse import urljoin
import requests


def prepare_url(self, path=None):
    return urljoin(self.api_url,
                   posixpath.join("api/v1/telegram/users", path))


def create_telegram_user(self, user: dict):
    url = self.prepare_url()
    return requests.post(url, json=user).json()


def get_telegram_user(self, user: dict):
    url = self.prepare_url(f"{user.get('id')}")
    return requests.get(url).json()


def update_telegram_user(self, user: dict):
    url = self.prepare_url(f"{user.get('id')}")
    return requests.put(url, json=user).json()
