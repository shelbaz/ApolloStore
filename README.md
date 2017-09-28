# Apollo Store
Your home to purchasing electronics online!

[![Build Status](https://travis-ci.com/Radu-Raicea/ApolloStore.svg?token=2ExxDcXbwqGBvJ5igREZ&branch=master)](https://travis-ci.com/Radu-Raicea/ApolloStore)


    .
    ├── docker-compose.yml
    ├── flask
    │   ├── config.py
    │   ├── Dockerfile
    │   ├── manage.py
    │   ├── project
    │   │   ├── __init__.py
    │   │   ├── models
    │   │   │   ├── auth_model.py
    │   │   │   ├── cart_model.py
    │   │   │   ├── desktop_model.py
    │   │   │   ├── __init__.py
    │   │   │   ├── inventory_model.py
    │   │   │   ├── item_model.py
    │   │   │   ├── laptop_model.py
    │   │   │   ├── monitor_model.py
    │   │   │   ├── tablet_model.py
    │   │   │   └── television_model.py
    │   │   ├── services
    │   │   │   ├── authentication.py
    │   │   │   ├── electronics.py
    │   │   │   └── __init__.py
    │   │   ├── static
    │   │   │   ├── css
    │   │   │   ├── img
    │   │   │   └── js
    │   │   ├── templates
    │   │   │   └── index.html
    │   │   └── website
    │   │       ├── __init__.py
    │   │       └── views.py
    │   ├── requirements.txt
    │   └── tests
    │       ├── base_authentication.py
    │       ├── base_create_objects.py
    │       ├── base_viewmodels.py
    │       ├── base_website.py
    │       ├── helpers.py
    │       ├── __init__.py
    │       ├── test_authentication.py
    │       ├── test_configs.py
    │       ├── test_create_objects.py
    │       ├── test_view_models.py
    │       └── test_website.py
    ├── nginx
    │   ├── app.conf
    │   ├── Dockerfile
    │   └── nginx.conf
    ├── postgres
    │   ├── create.sql
    │   └── Dockerfile
    └── README.md


## Installation
* [Windows 10 (64-bit Pro)](https://github.com/Radu-Raicea/ApolloStore/wiki/%5BInstallation%5D-Windows-10-Instructions-(64-bit-Pro))
* [Windows Toolbox](https://github.com/Radu-Raicea/ApolloStore/wiki/%5BInstallation%5D-Windows-Instructions-(Toolbox))
* [macOS (Yosemite 10.10.3 and higher)](https://github.com/Radu-Raicea/ApolloStore/wiki/%5BInstallation%5D-macOS-Instructions-(Yosemite-10.10.3-and-higher))
* [Linux (Ubuntu 16.04)](https://github.com/Radu-Raicea/ApolloStore/wiki/%5BInstallation%5D-Linux-Instructions-(Ubuntu-16.04))

## Flask
* [Using Flask Script to run commands while application is running](https://github.com/Radu-Raicea/ApolloStore/wiki/%5BFlask%5D-Using-Flask-Script-to-run-commands-while-the-application-is-running)
* [Running unit tests with Flask Testing and coverage](https://github.com/Radu-Raicea/ApolloStore/wiki/%5BFlask%5D-Running-unit-tests-with-Flask-Testing-and-coverage)

## Docker
* [Remove all Docker volumes to delete the database](https://github.com/Radu-Raicea/ApolloStore/wiki/%5BDocker%5D-Remove-all-Docker-volumes-to-delete-the-database)
* [Access the PostgreSQL command line terminal through Docker](https://github.com/Radu-Raicea/ApolloStore/wiki/%5BDocker%5D-Access-the-PostgreSQL-command-line-terminal-through-Docker)

## Other
* [Access the PostgreSQL database using a 3rd party software](https://github.com/Radu-Raicea/ApolloStore/wiki/%5BOther%5D-Access-the-PostgreSQL-database-using-a-3rd-party-software)