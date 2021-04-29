#!/usr/bin/env python

from dagster import (
    pipeline,
    repository,
    schedule,solid
)


@solid
def hello(_):
    return "World"


@solid
def world(_):
    return "Hello"


@schedule(cron_schedule="* * * * *", pipeline_name="my_pipeline", execution_timezone="UTC")
def my_schedule(_context):
    return {}


@pipeline
def my_pipeline():
    return "{} {}".format(hello(), world())


@pipeline
def my_pipeline_2():
    return "{} {}".format(hello(), world())
