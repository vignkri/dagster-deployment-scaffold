#!/usr/bin/env python

import requests

from dagster import (
    pipeline,
    repository,
    schedule,solid
)


def get_package_information(package_id: str):
    """Get package information
    """
    base_url = "http://api.energidataservice.dk/{}"
    package_information_url = base_url.format("package_show")
    response = requests.request("GET", package_information_url,
        params={"id": package_id, "include_tracking": True}}
    return response


@solid
def get_last_modified_information(_):
    response = get_package_information(package_id="co2emis")
    if response.ok:
        print(response.json())
        return response
    else:
        return False

@pipeline
def co2_emissions_pipeline():
    response = get_last_modified_information()
    print(response)
