# -*- coding: utf-8 -*-
"""Azure class file."""
import os

from azure.identity import DefaultAzureCredential


class Azure:
    """Azure Class."""

    def __init__(self, client_id, client_secret, tenant_id):
        """Initialize an Azure class instance."""
        os.environ["AZURE_CLIENT_ID"] = client_id
        os.environ["AZURE_CLIENT_SECRET"] = client_secret
        os.environ["AZURE_TENANT_ID"] = tenant_id
        self.credential = DefaultAzureCredential()
