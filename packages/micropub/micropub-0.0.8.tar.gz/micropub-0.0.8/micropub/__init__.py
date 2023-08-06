"""Micropub client."""

import functools

import requests


class PostNotCreated(Exception):
    """Post failed to be created."""


class Client:
    """Micropub client."""

    def __init__(self, endpoint, access_token):
        """Initiate a session with the Micropub server."""
        self.session = requests.session()
        self.endpoint = endpoint
        self.access_token = access_token
        self.session.headers.update(Authorization=f"Bearer {access_token}")
        self.get = functools.partial(self.session.get, endpoint)
        self.post = functools.partial(self.session.post, endpoint)

    def get_post(self, permalink):
        """Get the post at `permalink`."""
        return self.get(params={"q": "source", "url": permalink})

    def create_post(self, properties, h="entry"):
        """Create a post of type `h` with given `properties`."""
        response = self.post(json={"type": [f"h-{h}"], "properties": properties})
        if response.status_code != 201:
            raise PostNotCreated()
        return response.url, response.links
