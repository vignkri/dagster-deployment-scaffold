# Dagster Pipelines and Task Workflows

Handles task workflows for extraction / load / transformations of input datasets
from different sources.


## How to setup environment

- Update the images
```
docker-compose -f docker-compose.local.yml build
```

- Bring the images up
```
docker-compose -f docker-compose.local.yml up
```

## How to handle updates to the workflows

```
docker-compose -f docker-compose.local.yml restart docker_example_pipelines
```