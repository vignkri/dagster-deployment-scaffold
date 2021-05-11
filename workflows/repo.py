
from dagster import repository
from fcr_dk1 import fcr_dk1_pipeline
from fcr_dk2 import fcr_dk2_pipeline


@repository
def eds_fcr_dk1():
    return [
        fcr_dk1_pipeline
    ]


@repository
def eds_fcr_dk2():
    return [
        fcr_dk2_pipeline
    ]
