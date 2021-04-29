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

This is a piece of zsh code that looks for the container ID and uses it to restart
the docker container with the new piece of code.

```
docker restart $(docker ps | grep pipelines_image | cut -d " " -f1)
```