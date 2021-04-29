
from dagster import repository
from co2emissions import co2_emissions_pipeline


@repository
def eds_co2emissions():
    return [
        co2_emissions_pipeline
    ]
