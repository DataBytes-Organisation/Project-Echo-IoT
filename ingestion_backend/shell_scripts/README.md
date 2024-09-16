# shell_scripts

## Overview
This directory contains shell_scripts used for for the ingestion backend. They can be integrated with CI/CD pipelines that are developed or ran locally.

## Scripts

|Script|Description|
|---|---|
|python_ci.sh|This script performs continuous integration steps for the python service component of the docker image. It runs pytest unit tests (with coverage), pylint for linting and then mypy for static type checking.|

## Running the scripts
To run a script located here change the current working directory to this location and run:

```sh
./<script name>
```

IE.

```
./python_ci.sh
```
