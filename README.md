---

# Interview Project

## Overview

This project is designed to manage URL redirection rules with JWT authentication. It is containerized using Docker and can be managed using `docker-compose` and `Makefile` commands.

## Requirements

- Docker
- Docker Compose
- Make

## Setup

1. Clone the repository:
    ```bash
    git clone git@github.com:AnnHalii/interview_project.git
    cd interview_project/
    ```

2. Build the Docker image && Start the application:
    ```bash
    make run
    ```

   This will build and start the Docker containers using `docker-compose`. It will run the application in detached mode.

## Makefile Commands

The Makefile includes several commands to help you manage the project.

- **build**: Builds the Docker image with the tag specified in `IMAGE`.
    ```bash
    make build
    ```

- **run**: Builds the image (if not already built) and starts the containers in detached mode.
    ```bash
    make run
    ```

- **stop**: Stops the running Docker containers.
    ```bash
    make stop
    ```

- **logs**: Streams the logs of the `web` container.
    ```bash
    make logs
    ```

- **exec**: Opens a bash shell in the `web` container for debugging or maintenance.
    ```bash
    make exec
    ```

- **destroy**: Stops and removes the containers.
    ```bash
    make destroy
    ```

- **test**: Runs the tests using `api-test` container.
    ```bash
    make test
    ```
## Acceptance Criteria

The detailed ACs for this project can be found [here](https://gist.github.com/andrey484/d689eca178d9455e7c23e7709f70f536).

## Additional Notes

- Make sure Docker and Docker Compose are properly installed on your machine before running these commands.

---