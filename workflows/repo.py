
from dagster import repository
from co2emissions import co2_emissions_pipeline


@repository
def energidataservice_repository():
    return [co2_emissions_pipeline]
