---
layout: post_with_ad
title: 우분투 도커 설치 (root user 용)
date: 2024-06-18 11:04:51 +0900
permalink: /20240618/en/install-docker-on-ubuntu-for-root
categories: web api
tags: docker, ubuntu
excerpt: (for root) Let's learn how to install Docker on Ubuntu.
---

## **Table of Contents**

* Update Ubuntu System Packages
* Install Required Packages
* Add Docker's Official GPG Key
* Add Docker's Official Repository
* Update and Install Docker
* Check Docker Status
* Start Docker
* Run Docker
* Enable Docker to Start Automatically

### Run All at Once

If you're in a hurry, you can just run the following commands:

#### Install

```sh
apt-get update && \
apt-get install -y apt-transport-https ca-certificates curl gnupg-agent software-properties-common && \
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | apt-key add - && \
add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" && \
apt-get update && \
apt-get install -y docker-ce docker-ce-cli containerd.io
```

### Enable Docker to Start Automatically on Boot
```sh
systemctl status docker
systemctl start docker # if needed
systemctl enable docker
```

### Update Ubuntu System Packages

Update the packages on your Ubuntu system to the latest versions.

```sh
apt-get update
```

### Install Required Packages

Install the required packages.

```sh
apt-get install apt-transport-https ca-certificates curl gnupg-agent software-properties-common
```

### Add Docker's Official GPG Key

Download and add Docker's official GPG key to apt-key.

```sh
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | apt-key add -
```

### Add Docker's Official Repository

Add Docker's official repository.

```sh
add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
```

### Update and Install Docker

Update and install Docker.

```sh
apt-get update
```

### Install Docker

Install Docker CE (Community Edition), Docker CE CLI (Command Line Interface), and containerd.io.

```sh
apt-get install docker-ce docker-ce-cli containerd.io
```

### Check Docker Status

Check if Docker is installed correctly.

```sh
systemctl status docker
```

### Start Docker

If Docker is not running, start it.

```sh
systemctl start docker
```

### Test Run Docker

Run a test Docker container.

```sh
docker run hello-world
```

If the installation was successful, you should see a message like this:

```
Hello from Docker!
This message shows that your installation appears to be working correctly.

To generate this message, Docker took the following steps:
 1. The Docker client contacted the Docker daemon.
 2. The Docker daemon pulled the "hello-world" image from the Docker Hub.
    (arm64v8)
 3. The Docker daemon created a new container from that image which runs the
    executable that produces the output you are currently reading.
 4. The Docker daemon streamed that output to the Docker client, which sent it
    to your terminal.

To try something more ambitious, you can run an Ubuntu container with:
 $ docker run -it ubuntu bash

Share images, automate workflows, and more with a free Docker ID:
 https://hub.docker.com/

For more examples and ideas, visit:
 https://docs.docker.com/get-started/
```

### Enable Docker to Start Automatically

Enable Docker to start automatically on boot.

```sh
systemctl enable docker
```