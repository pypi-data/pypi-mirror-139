# -*- coding: utf-8 -*-
"""Redis class for Gaia."""
import json

from google.cloud import firestore
from redis import StrictRedis


class Redis(StrictRedis):
    """Redis class."""

    def __init__(self, host, port):
        """Initialize a redis instance."""
        super().__init__(host=host, port=port)

    def _get_firestore_collection(self, collection):
        """Return a firestore collection as a list of dicts."""
        client = firestore.Client()
        data = []
        for doc in client.collection(collection).stream():
            data.append(doc.to_dict())
        return data

    def get_collection(self, collection):
        """Return a list of dicts from Redis (or Firestore)."""
        json_string = self.get(collection)
        if json_string:
            return json.loads(json_string)
        data = self._get_firestore_collection(collection)
        self.set(collection, json.dumps(data, default=str))
        return data
