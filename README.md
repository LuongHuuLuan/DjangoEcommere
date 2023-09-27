<h1 align="left">Welcome to DjangoEcommerce Project: Learning Django and REST Framework 👋</h1>

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![DjangoREST](https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray)

## Overview
> DjangoEcommerce is a project designed to help you understand how to use the Django framework and create a simple API using Django REST Framework. This project covers essential CRUD (Create, Read, Update, Delete) functionalities and token-based authentication through tokens and sessions.

## Key Topics

* **Understanding Django:** Gain insights into Django's fundamentals and how it facilitates web application development.
* **Exploring RESTful APIs:** Learn about REST (Representational State Transfer) and how to implement APIs following REST principles
* **CRUD Functionality:** Implement CRUD operations (Create, Read, Update, Delete) for managing a specific resource (e.g., products).
* **Token-Based Authentication:** Understand and implement token-based authentication to secure the API.

## Getting Started
This project use the Python 3.11, the pip 23.2.1 package and add some configuration files to deploy the app.

## Install

**Note:** Please ensure you have Python 3.11 and pip 23.2.1 installed on your computer before proceeding with these steps. If Python or pip is not installed, you can download it here:

* [python 3.11](https://www.python.org/downloads/release/python-3110/)
* [pip 23.2.1](https://pip.pypa.io/en/stable/installation/)

## **Steps**
1. Download the Source Code from GitHub:
```sh
git clone https://github.com/LuongHuuLuan/DjangoEcommere.git
```
Once this command is complete, you will have a directory named DjangoEcommere containing the project's source code.

2. Create a Virtual Environment:

Within the project directory (DjangoEcommere), it's advisable to create a virtual environment to install the dependencies in an isolated environment. Execute the following command:
```sh
python -m venv env
```
This creates a new virtual environment named myenv. You can choose a different name if you wish.

3. Activate the Virtual Environment:

* On Windows:
```sh
env\Scripts\activate
```
* On MacOS and Linux:
```sh
source myenv/bin/activate
```
Once the environment is activated, the python and pip commands will use the Python and pip versions within the virtual environment.

4. Install libraries

Next, we need to install the necessary libraries. The required packages are listed in the requirements.txt file.

```sh
pip install -r requirements.txt
```
5. Config .env

create .env file in the root folder add some line in this

```sh
DEBUG=True
SECRET_KEY=your secret key
ALLOWED_HOSTS=*
SQLITE_URL=sqlite:///db.sqlite3
#if use mysql
#DATABASE_URL=mysql://username:@host:port/database_name
```
the secret can created in [here](https://codinggear.blog/django-generate-secret-key/)
## Usage

Use the python manage.py runserver command to start the Django development 
```sh
python manage.py runserver
```
By default, the server will run on http://127.0.0.1:8000/. You can specify a different host and port if needed.
```sh
python manage.py runserver 0.0.0.0:8000
```
You can now interact with the Django application and explore its functionalities.

Remember to keep the terminal open and the Django development server running as long as you want to use the application. To stop the server, press Ctrl + C in the terminal.
## Author

👤 **Luong Huu Luan**

* Github: [@LuongHuuLuan](https://github.com/LuongHuuLuan)

## Show your support

Give a ⭐️ if this project helped you!

***
_This README was generated with ❤️ by [readme-md-generator](https://github.com/kefranabg/readme-md-generator)_