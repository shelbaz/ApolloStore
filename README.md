# Apollo Store
Your home to purchasing electronics online!

[![Build Status](https://travis-ci.com/Radu-Raicea/ApolloStore.svg?token=2ExxDcXbwqGBvJ5igREZ&branch=master)](https://travis-ci.com/Radu-Raicea/ApolloStore)

## Windows 10 Instructions (64-bit)

### Download Docker

`https://download.docker.com/win/stable/Docker%20for%20Windows%20Installer.exe`

### Meet the requirements for installing Docker on Windows

- You must have Windows 10 Pro, Enterprise or Education with the 64-bit version installed. If you don't, installing Docker will be slightly more complicated because you need to install the Docker Toolbox. If you're in that scenario, you can try installing it using the instructions here: `https://docs.docker.com/toolbox/overview/`

- You must have virtualization enabled on your computer. Sometimes it is enabled by default, but many times you need to go in the BIOS of your computer to enable it. Instructions for this vary from computer to computer, so I recommend searching instructions yourself.

- Hyper-V must be enabled (Docker should enable it automatically when you run it the first time).

### Install Docker

Follow steps 1 to 3 in the following link: `https://docs.docker.com/docker-for-windows/install/#install-docker-for-windows`

### Start Docker

Follow the instructions in the following link to start Docker: `https://docs.docker.com/docker-for-windows/install/#start-docker-for-windows`

### Clone App

Make sure you have Git installed on your computer before cloning the repository.

Open a Command Prompt and run the following commands:

`cd [path/where/you/want/to/clone]`

`git clone https://github.com/Radu-Raicea/ApolloStore.git`

### Build App

`cd ApolloStore`

`docker-compose up --build`

Check out `http://localhost/`

### Restarting the App

Press CTRL-C to kill the app

`docker-compose down`

`docker-compose up --build`



## macOS Instructions

### Download Docker

`https://download.docker.com/mac/stable/Docker.dmg`

### Install Docker

Follow steps 1 to 4 in the following link: `https://docs.docker.com/docker-for-mac/install/#install-and-run-docker-for-mac`

### Clone App

Make sure you have Git installed on your computer before cloning the repository.

Open a Terminal and run the following commands:

`cd [path/where/you/want/to/clone]`

`git clone https://github.com/Radu-Raicea/ApolloStore.git`

### Build App

`cd ApolloStore`

`docker-compose up --build`

Check out `http://localhost/`

### Restarting the App

Press CTRL-C to kill the app

`docker-compose down`

`docker-compose up --build`



## Linux Instructions (Ubuntu 16.04)

### Switch to root

`sudo -s`

### Install Docker

```
apt-get install \
apt-transport-https \
ca-certificates \
curl \
software-properties-common
```

`curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -`

```
add-apt-repository \
"deb [arch=amd64] https://download.docker.com/linux/ubuntu \
$(lsb_release -cs) \
stable"
```

`apt-get update`

`apt-get install docker-ce`

### Install Docker-Compose

```curl -L https://github.com/docker/compose/releases/download/1.13.0/docker-compose-`uname -s`-`uname -m` > /usr/local/bin/docker-compose```

`chmod +x /usr/local/bin/docker-compose`

### Clone App

`cd [path/where/you/want/to/clone]`

`git clone https://github.com/Radu-Raicea/ApolloStore.git`

### Build App

`cd ApolloStore`

`docker-compose up --build`

Check out `http://localhost/`

### Restarting the App

Press CTRL-C to kill the app

`docker-compose down`

`docker-compose up --build`
