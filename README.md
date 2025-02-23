# TCC - Computer Science Bachelor thesis
This is my final project in the college [FEMA - Fundação Educaional do Municipio de Assis]([https://pages.github.com/](https://www.fema.edu.br/)).

## 1. ABSTRACT
With the advancement of technology and the increasing application of Artificial Intelligence
in everyday life, new opportunities emerge to explore the use of Convolutional Neural
Networks (CNNs) in various fields, including workplace safety. These networks have
proven to be powerful tools for image analysis and classification, contributing significantly
to areas such as medical assistance. This study focuses on the application of CNNs,
specifically the Yolov8 model, for detecting Personal Protective Equipment (PPE), aiming
at accident prevention and promoting a safer work environment. The research seeks to
demonstrate how this technology can be applied to ensure proper PPE usage, offering
support to both workers and managers in their safety practices.
Keywords: Computer Vision, Artificial Intelligence, Occupational Safety.

## 2. INTRODUCTION
To use this app you're gonna need python and mysql installed, in the settings.py you're gonna need to configure the location of the mysql in your server.

## 3. USAGE
### 3.1. Clone Project
To clone the project from Github you'll need to use this command.
```shell
$ git clone https://github.com/gabrielmossini/tcc.git
```
### 3.2. Python and Django configuration
First you need to install the repositories, if you're using Ubuntu or Debian based, you can verify using the following command.
```shell
$ python3 -V
```
Create a virtual enviroment inside the tcc/Aegis folder.
```shell
$ python3 -m venv venv
```
This install a virtual version of Python, pip within your project directory. To install any packges into the project, you must activate the enviroment using the following command.
```shell
$ source venv/bin/activate
```
Your shell prompt will change to reflect the virtual enviroment.
```shell
$ (venv) user@device:~/Aegis$
```
Now the virtual environment is activated, use <i>pip</i> to install Django. To install all the pips required you'll need to use this command inside the main project folder.
```shell
$ pip install -r requirements.txt
```
Verify the installation.
```shell
$ (venv) $ django-admin --version
output: 5.1.6 
```
#### 3.2.1 Repository Default User Configuration
All you're gonna need to do is two commands the first one:
```shell
$ python3 manage.py makemigrations
```
And the second one:
```shell
$ python3 manage.py migrate
```
Now you gonna need to create a default user, following this command.
```shell
$ python3 manage.py create_default_user
```

The user created is:
- User: <i> default </i>
- Password: <i> password123 </i>

## 4. Run
Now to run the app you're gonna to write this command in the terminal:
```shell
$ python3 manage.py runserver
```







