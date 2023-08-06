# -*- coding: utf-8 -*-
"""Workday class for Gaia."""
import datetime
import logging

import requests
from zeep import Client
from zeep.wsse.username import UsernameToken


class Workday:
    """Workday Class."""

    def __init__(self, base_url, username, password, tenant, version="v31.0"):
        """Initialize a Workday instance."""
        self.base_url = base_url
        self.username = username
        self.password = password
        self.tenant = tenant
        self.version = version

        self.login = f"{self.username}@{self.tenant}"

    def auth(self, service):
        """Authenticate to Workday SOAP api."""
        token = UsernameToken(self.login, self.password)
        url = f"{self.base_url}/{self.tenant}/{service}/{self.version}?wsdl"
        return Client(url, wsse=token)

    #
    # People Feed
    #
    def get_workday_people_feed(self, report_days=0):
        """Return the response from Workday."""
        service = "customreport2"
        url = f"{self.base_url}/{service}/{self.tenant}/{self.username}/CR_INT027_People_Feed_Outbound"
        auth = (self.username, self.password)
        effective_date = datetime.date.today() + datetime.timedelta(days=report_days)
        params = {
            "Effective_as_of_Date": effective_date.strftime("%Y-%m-%d-08:00"),
            "format": "json",
        }
        try:
            response = requests.get(url, auth=auth, params=params)
            response.raise_for_status()
        except requests.exceptions.HTTPError as http_error:
            logging.error(f"Failed running Workday People feed: {http_error}.")
            raise http_error
        return response.json().get("Report_Entry", [])

    #
    # Desks
    #
    def update_desk(self, position_id, location_id):
        """Update desk for a single worker from Workday."""
        client = self.auth("Human_Resources")

        work_space_reference = {
            "ID": {
                "_value_1": location_id,
                "type": "Location_ID",
            },
        }
        work_space_change_event_data = {
            "Position_Reference": {
                "ID": {
                    "_value_1": position_id,
                    "type": "Position_ID",
                },
            },
            "Effective_Date": datetime.date.today(),
        }
        if location_id:
            work_space_change_event_data["Work_Space_Reference"] = work_space_reference

        return client.service.Change_Work_Space(
            Business_Process_Parameters=None,
            Work_Space_Change_Event_Data=work_space_change_event_data,
        )

    #
    # Locations
    #
    def get_locations_by_name(self, name):
        """Return locations that match the given name."""
        request_criteria = {
            "Location_Name": name,
        }
        return self.get_locations(request_criteria=request_criteria)

    def get_locations(self, request_criteria=None):
        """Return locations."""
        client = self.auth("Human_Resources")
        params = {
            "Count": 999,
            "Page": 1,
        }
        response = client.service.Get_Locations(
            Request_Criteria=request_criteria,
            Response_Filter=params,
        )
        locations = response["Response_Data"]["Location"]
        page = response["Response_Results"]["Page"]
        total_pages = response["Response_Results"]["Total_Pages"]
        while page < total_pages:
            params["Page"] += 1
            response = client.service.Get_Locations(
                Request_Criteria=request_criteria,
                Response_Filter=params,
            )
            locations.extend(response["Response_Data"]["Location"])
            page = response["Response_Results"]["Page"]
        return locations

    def move_location(self, location, parent_id):
        """Move a location to a new parent."""
        location["Location_Data"]["Superior_Location_Reference"] = {
            "ID": [{"_value_1": parent_id, "type": "Location_ID"}],
        }
        return self.update_location(location)

    def prepare_location(self, location):
        """Prepare a location record."""
        location_data = location["Location_Data"]
        location_id = location_data["Location_ID"]
        name = location_data["Location_Name"]
        usage_type = location_data["Location_Usage_Reference"][0]["ID"][1]["_value_1"]

        # location type
        location_type_reference = location_data["Location_Type_Reference"]
        location_type = location_type_reference[0]["ID"][1]["_value_1"] if location_type_reference else None

        # parent location
        parent_location = location_data["Superior_Location_Reference"]
        parent = parent_location["ID"][1]["_value_1"] if parent_location else None

        # inactive
        inactive = location_data["Inactive"]

        return {
            "id": location_id,
            "inactive": inactive,
            "name": name,
            "location_type": location_type,
            "usage_type": usage_type,
            "parent": parent,
            "data": location,
        }

    def prepare_locations(self, locations):
        """Prepare all location records."""
        prepared = []
        for location in locations:
            prepared.append(self.prepare_location(location))
        return prepared

    def update_location(self, location):
        """Update a location in Workday."""
        client = self.auth("Human_Resources")
        return client.service.Put_Location(
            Location_Reference=location["Location_Reference"],
            Location_Data=location["Location_Data"],
        )

    #
    # Phones
    #
    def update_phone(self, emplid, phone, employee=True):
        """Update phone for a single worker from Workday."""
        id_type = "Employee_ID" if employee else "Contingent_Worker_ID"

        client = self.auth('Human_Resources')

        # RoleObject
        RoleObjectType = client.get_type('ns0:RoleObjectType')
        Person_Reference = RoleObjectType(
            ID={'_value_1': emplid, 'type': id_type},
        )

        # Get_Change_Work_Contact_Information_Request_References
        Get_Change_Work_Contact_Information_Request_ReferencesType = client.get_type(
            'ns0:Get_Change_Work_Contact_Information_Request_ReferencesType',
        )

        # Request_References
        Request_References = Get_Change_Work_Contact_Information_Request_ReferencesType(
            Person_Reference=Person_Reference,
        )

        # Get_Change_Work_Contact_Information
        request = client.service.Get_Change_Work_Contact_Information(
            Request_References=Request_References,
            Response_Filter=None,
            Request_Criteria_Data=None,
        )

        # get Response_Data
        Response_Data = request['Response_Data'][0]
        Change_Work_Contact_Information = Response_Data['Change_Work_Contact_Information'][0]
        Change_Work_Contact_Information_Data = Change_Work_Contact_Information[
            'Change_Work_Contact_Information_Data'
        ][0]

        # set Event_Effective_Date to today
        Change_Work_Contact_Information_Data['Event_Effective_Date'] = datetime.date.today()

        # check for Person_Phone_Information_Data
        if not Change_Work_Contact_Information_Data[
            'Person_Contact_Information_Data'
        ][
                'Person_Phone_Information_Data'
        ]:

            # Country_Phone_CodeObject
            Country_Phone_CodeObjectType = client.get_type('ns0:Country_Phone_CodeObjectType')
            Country_Code_Reference = Country_Phone_CodeObjectType(
                ID={'_value_1': 'db8d3ca6446c11de98360015c5e6daf6', 'type': 'WID'},
            )

            # Phone_Device_TypeObject
            Phone_Device_TypeObjectType = client.get_type('ns0:Phone_Device_TypeObjectType')
            Device_Type_Reference = Phone_Device_TypeObjectType(
                ID={'_value_1': '80ac8a2075550197e6cb81ca5c2ee205', 'type': 'WID'},
            )

            # Phone_Core_Data
            Phone_Core_DataType = client.get_type('ns0:Phone_Core_DataType')
            Phone_Data = Phone_Core_DataType(
                Country_Code_Reference=Country_Code_Reference,
                Complete_Phone_Number=phone,
                Device_Type_Reference=Device_Type_Reference,
            )

            # Communication_Usage_TypeObject
            Communication_Usage_TypeObjectType = client.get_type(
                'ns0:Communication_Usage_TypeObjectType',
            )
            Type_Reference = Communication_Usage_TypeObjectType(
                ID={'_value_1': '1f27f250dfaa4724ab1e1617174281e4', 'type': 'WID'},
            )

            # Communication_Usage_Type_Data
            Communication_Usage_Type_DataType = client.get_type(
                'ns0:Communication_Usage_Type_DataType',
            )
            Type_Data = Communication_Usage_Type_DataType(
                Type_Reference=Type_Reference,
                Primary=True,
            )

            # Communication_Method_Usage_Information_Data
            Communication_Method_Usage_Information_DataType = client.get_type(
                'ns0:Communication_Method_Usage_Information_DataType',
            )
            Usage_Data = Communication_Method_Usage_Information_DataType(
                Type_Data=Type_Data,
            )

            # Person_Phone_data
            Person_Phone_DataType = client.get_type('ns0:Person_Phone_DataType')
            Phone_Information_Data = Person_Phone_DataType(
                Phone_Data=[Phone_Data],
                Usage_Data=[Usage_Data],
                Phone_Reference=None,
                Phone_ID=None,
            )

            # Person_Phone_Information_Data
            Person_Phone_Information_DataType = client.get_type(
                'ns0:Person_Phone_Information_DataType',
            )
            Person_Phone_Information_Data = Person_Phone_Information_DataType(
                Phone_Information_Data=[Phone_Information_Data],
            )

            Change_Work_Contact_Information_Data[
                'Person_Contact_Information_Data'
            ][
                'Person_Phone_Information_Data'
            ] = Person_Phone_Information_Data

        # update work phone number
        if phone:
            Change_Work_Contact_Information_Data[
                'Person_Contact_Information_Data'
            ][
                'Person_Phone_Information_Data'
            ][
                'Phone_Information_Data'
            ][0][
                'Phone_Data'
            ][0][
                'Complete_Phone_Number'
            ] = phone

            Change_Work_Contact_Information_Data[
                'Person_Contact_Information_Data'
            ][
                'Person_Phone_Information_Data'
            ][
                'Phone_Information_Data'
            ][0][
                'Phone_Data'
            ][0][
                'Extension'
            ] = None

        # or remove work phone numbers
        else:
            for pid in Change_Work_Contact_Information_Data[
                'Person_Contact_Information_Data'
            ][
                    'Person_Phone_Information_Data'
            ][
                'Phone_Information_Data'
            ]:
                pid['Delete'] = True

        del Change_Work_Contact_Information_Data[
            'Person_Contact_Information_Data'
        ]['Person_Address_Information_Data']
        del Change_Work_Contact_Information_Data[
            'Person_Contact_Information_Data'
        ]['Person_Email_Information_Data']
        del Change_Work_Contact_Information_Data[
            'Person_Contact_Information_Data'
        ]['Person_Instant_Messenger_Information_Data']
        del Change_Work_Contact_Information_Data[
            'Person_Contact_Information_Data'
        ]['Person_Web_Address_Information_Data']

        return client.service.Change_Work_Contact_Information(
            Change_Work_Contact_Information_Data=Change_Work_Contact_Information_Data,
        )

    #
    # Workers
    #
    def get_worker(self, emplid, employee=True):
        """Return a worker based on EMPLID."""
        id_type = "Employee_ID" if employee else "Contingent_Worker_ID"
        request_references = {
            "Worker_Reference": {
                "ID": [
                    {
                        "type": id_type,
                        "_value_1": emplid,
                    },
                ],
            },
        }
        results = self.get_workers(request_references=request_references)
        if results:
            return results[0]
        return None

    def get_workers(self, request_criteria=None, request_references=None, response_group=None):
        """Return workers."""
        client = self.auth("Human_Resources")
        params = {
            "Count": 999,
            "Page": 1,
        }
        response = client.service.Get_Workers(
            Request_Criteria=request_criteria,
            Request_References=request_references,
            Response_Filter=params,
            Response_Group=response_group,
        )
        workers = response["Response_Data"]["Worker"]
        page = response["Response_Results"]["Page"]
        total_pages = response["Response_Results"]["Total_Pages"]
        while page < total_pages:
            params["Page"] += 1
            response = client.service.Get_Workers(
                Request_Criteria=request_criteria,
                Request_References=request_references,
                Response_Filter=params,
                Response_Group=response_group,
            )
            workers.extend(response["Response_Data"]["Worker"])
            page = response["Response_Results"]["Page"]
        return workers

    def get_worker_locations(self, location_ids):
        """Return all workers and their locations."""
        response_group = {
            "Include_Employment_Information": True,
        }
        workers = self.get_workers(response_group=response_group)
        locations = {}
        for worker in workers:
            emplid = worker["Worker_Data"]["Worker_ID"]
            worker_job_data = worker["Worker_Data"]["Employment_Data"]["Worker_Job_Data"]
            position_data = worker_job_data[0]["Position_Data"]
            building = position_data["Business_Site_Summary_Data"]["Location_Reference"]["ID"][1]["_value_1"]
            desk = None
            location_id = None
            if position_data["Work_Space__Reference"]:
                location_id = position_data["Work_Space__Reference"]["ID"][1]["_value_1"]
                if location_id in location_ids:
                    desk = location_ids[location_id]["name"]
                location = {
                    "building": building,
                    "desk": desk,
                    "emplid": emplid,
                    "id": location_id,
                    "position_id": position_data["Position_ID"],
                }
            locations[emplid] = location
        return locations
