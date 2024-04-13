# TAScheduler Project

This will walk you through setting up your development environment, including the creation of a virtual environment, installation of dependencies, and starting the Django development server.


## Prerequisites

Before you begin, make sure you have Python installed on your system. This project uses Python 3.8 or later.

## Clone the Repository

First, clone the project repository from GitHub to your local machine using the following command in your terminal (replace <url> with the actual repository URL):

  ```
  git clone [<url>](https://github.com/julianbartosz/Commit_Issues-Django_Project-CS361_Rock.git)
  cd <Commit_Issues-Project>
  ```

Replace project-directory with the name of the folder that Git creates on your system.

## Create a Virtual Environment

A virtual environment is a self-contained directory that contains a Python installation for a particular version of Python, plus a number of additional packages. Creating a virtual environment allows you to manage project dependencies separately from your global Python environment.

For Windows
Run the following commands in your command prompt:

  ```
  python -m venv env
  env\Scripts\activate
  ```

For macOS and Linux
Run the following commands in your terminal:

  ```
  python3 -m venv env
  source env/bin/activate
  ```
You have to change the path for your specific case. As an example, this is how my command looks..

  ```
  source /Users/julianbartosz/cs361/Commit_Issues-Project/root/.venv/bin/activate
  ```

After activation, your terminal prompt will change to show the name of the activated environment.

## Install Project Dependencies

With your virtual environment activated, install the project dependencies using the following command:
  
  ```
  pip install -r requirements.txt
  ```
or
  ```
  pip3 install -r requirements.txt
  ```

This command reads the requirements.txt file in your project directory and installs all the necessary Python packages.

## Set Up the Database

Run the following command to make migrations to your database. This step sets up your database schema according to the models defined in your Django apps.

  ```
  python manage.py makemigrations
  python manage.py migrate
  ```
or 
  ```
  python3 manage.py makemigrations
  python3 manage.py migrate
  ```

## Create an Admin User

To access the Django admin interface, you need to create a superuser account. Use the following command and follow the prompts to set up the user:

  ```
  python manage.py createsuperuser
  ```
or
  ```
  python3 manage.py createsuperuser
  ```

Enter your desired username, email, and password when prompted.

## Run the Development Server

Now you're ready to start the development server and see the project in action. Run:

  ```
  python manage.py runserver
  ```
or
  ```
  python3 manage.py runserver
  ```

This command starts the Django development server. You can access your application by navigating to http://127.0.0.1:8000/ in your web browser.

## Access the Admin Panel

To access the Django admin interface, navigate to http://127.0.0.1:8000/admin and log in using the superuser credentials you created earlier.

## Stopping the Server

To stop the Django development server, press Ctrl+C in your command prompt or terminal window.
