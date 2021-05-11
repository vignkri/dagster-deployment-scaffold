#!/usr/bin/env python

from typing import Dict

import json
import boto3
import datetime as dt

import requests
import dateutil.parser as dateparser
from dagster import (
    pipeline,
    schedule,
    solid
)


@solid(
    description="Identify the last known modification time for metadata and resource"
)
def get_metadata_timestamps(context) -> Dict:
    base_url = "http://api.energidataservice.dk/{}"
    package_information_url = base_url.format("package_show")
    response = requests.request("GET", package_information_url,
        params={"id": "fcrreservesdk2", "include_tracking": True})
    if response.ok:
        result = response.json().get("result")
        context.log.info(json.dumps(result))
        return response.json()


@solid(
    description="Find the last known data point in the database."
)
def get_timestamp_of_latest_fcr_data(context) -> Dict:
    DATA_SPAN_QUERY = """SELECT MIN("{key}"), MAX("{key}") FROM "{datatable}";"""

    # Search the datastore for information
    base_url = "http://api.energidataservice.dk/{}"
    datastore_search_url = base_url.format("datastore_search_sql")

    # Handle response
    response = requests.request("GET", datastore_search_url,
        params={"sql": DATA_SPAN_QUERY.format(datatable="fcrreservesdk2", key="HourUTC")})
    if response.ok:
        result = response.json().get("result")
        context.log.info(json.dumps(response.json()))
        return response.json()


@solid
def get_last_12h_data(context, response: Dict, metadata_response: Dict):
    """Get last known data point
    """
    # Get metadata information
    _result = metadata_response.get("result")
    metadata_update_timestamp = _result.get("metadata_modified")
    metadata_resource_update_timestamp = _result.get('resources')[-1].get("last_modified")

    context.log.info(
        "Metadata updated: %s and Resource updated at: %s" % (
            metadata_update_timestamp,
            metadata_resource_update_timestamp
        )
    )
    # Get the last 12 hours of the dataset
    TIME_SERIES_QUERY = """SELECT * FROM "{datatable}" WHERE "HourUTC" BETWEEN '{start_time}' AND '{end_time}';"""
    # find_start_timestamp
    end_time = dateparser.parse(response.get("result").get("records")[-1].get("max"))
    start_time = end_time - dt.timedelta(hours=12)  # Handles 12 hour offsets

    # get last timestamp
    search_parameters = {
        "sql": TIME_SERIES_QUERY.format(datatable="fcrreservesdk2",
            start_time=start_time, end_time=end_time)
    }
    base_url = "http://api.energidataservice.dk/{}"
    datastore_search_url = base_url.format("datastore_search_sql")
    response = requests.request("GET", datastore_search_url,
        params=search_parameters)
    if response.ok:
        context.log.info("Response from the server: %s" % response.json())


@pipeline
def fcr_dk2_pipeline():
    get_last_12h_data(
        get_timestamp_of_latest_fcr_data(),
        get_metadata_timestamps()
    )
