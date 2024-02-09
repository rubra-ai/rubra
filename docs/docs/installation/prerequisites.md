---
id: prerequisites
title: Prerequisites
sidebar_label: Prerequisites
sidebar_position: 0
---

Before diving into Rubra, make sure your machine is equipped with the following tools:

## Docker

Rubra utilizes Docker to containerize the application and streamline the development environment. Docker allows you to run applications in isolated containers, making it easier to manage dependencies and environments.

To install Docker on any operating system, please follow the [official Docker installation guide](https://docs.docker.com/engine/install/)

After installing Docker, you can ensure that the Docker daemon is running by executing the following command in your terminal or command prompt:

```sh
docker --version
```

## Docker Compose

You will also need Docker Compose, which is a tool for defining and orchestrating multi-container Docker applications. With Docker Compose, you can use a YAML file to configure your application's services and then create and start all the services from your configuration with a single command.

For Docker Compose installation instructions, visit the [Docker Compose installation guide](https://docs.docker.com/compose/install/).

To check if Docker Compose is installed on your system, you can run the following command in your terminal or command prompt:

```sh
docker-compose --version
```

## Docker Desktop (Optional)

If you don't want to manually install Docker and Docker Compose, you can use Docker Desktop. It's an easy way to install and set up Docker and Docker Compose on your machine. Docker Desktop is available for Mac, Linux, and Windows. Visit the [installation guide](https://docs.docker.com/desktop/) to get started.
