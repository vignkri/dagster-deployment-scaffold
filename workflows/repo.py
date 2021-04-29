
from dagster import repository
from co2emissions import my_pipeline, my_schedule, my_pipeline_2


@repository
def deploy_docker_repository():
    return [my_pipeline, my_schedule]

@repository
def scheduled_runs():
    return [my_pipeline_2]