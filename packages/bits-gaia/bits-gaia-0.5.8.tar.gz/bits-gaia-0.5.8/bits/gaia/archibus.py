# -*- coding: utf-8 -*-
"""Archibus class file."""
import requests


class Archibus:
    """Archibus class."""

    def __init__(
        self,
        client_id,
        client_secret,
        auth_domain="dev-49038290.okta.com",
        base_url="https://broad-archibus.buildingi.com:446/archibus/api/v1",
    ):
        """Initialize an Archibus instance."""
        self.auth_domain = auth_domain
        self.client_id = client_id
        self.client_secret = client_secret

        self.base_url = base_url
        self.data_url = f"{self.base_url}/data"
        self.headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
        }
        self._authorize()

    def _authorize(self):
        """Authorize an access token."""
        url = f"https://{self.auth_domain}/oauth2/default/v1/token"
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/x-www-form-urlencoded",
        }
        params = {
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "grant_type": "client_credentials",
        }
        response = requests.post(url, headers=headers, params=params)
        response.raise_for_status()
        token = response.json()["access_token"]
        self.headers["Authorization"] = f"Bearer {token}"

    def _get(self, url, params=None):
        """Return a GET response."""
        response = requests.get(
            url,
            headers=self.headers,
            params=params,
            verify=False,
        )
        response.raise_for_status()
        return response.json()

    def get_buildings(self):
        """Return a list of buildings."""
        params = {
            "dataSource": "Api_Buildings_v1",
        }
        buildings = []
        for building in self._get(self.data_url, params=params):
            data = {}
            for key in building:
                k = key.replace("bl.", "")
                if k == "bl_id.key":
                    continue
                data[k] = building[key]
            buildings.append(data)
        return buildings

    def get_employee_locations(self):
        """Return a list of employee locations."""
        params = {
            "dataSource": "Api_HrEmLocations_broad",
        }
        locations = []
        for location in self._get(self.data_url, params=params):
            data = {}
            for key in location:
                k = key.replace("em.", "")
                if k == "em_id.key":
                    continue
                data[k] = location[key]
            locations.append(data)
        return locations
