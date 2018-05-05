# Book-A-Meal
[![Coverage Status](https://coveralls.io/repos/github/hoslack/Book-A-Meal_API/badge.svg?branch=master)](https://coveralls.io/github/hoslack/Book-A-Meal_API?branch=master) [![Requirements Status](https://requires.io/github/hoslack/Book-A-Meal_API/requirements.svg?branch=endpoints)](https://requires.io/github/hoslack/Book-A-Meal_API/requirements/?branch=endpoints)
## What? 
Book-A-Meal is an application that allows customers to make food orders and helps the food vendor know what the customers want to eat.
## Features
- Users can create an account and log in
- Admin (Caterer) should be able to manage (i.e: add, modify and delete) meal options in the application. Examples of meal options are: Beef with rice, Beef with fries etc
- Admin (Caterer) should be able to setup menu for a specific day by selecting from the meal options available on the system.
- Authenticated users (customers) should be able to see the menu for a specific day and select an option out of the menu.
- Authenticated users (customers) should be able to change their meal choice.
- Admin (Caterer) should be able to see the orders made by the user
- Admin should be able to see amount of money made by end of day
### Extra features
- Authenticated users (customers) should be able to see their order history
- Authenticated users (customers) should be able to get notifications when the menu for the day has been set.
- Admin (Caterer) should be able to see order history
- The application should be able to host more than one caterer.


## Screenshots of the UI
![Index](http://res.cloudinary.com/hoslack/image/upload/v1524319692/imageedit_5_6173175048_vnobg8.png)


![Sign Up](http://res.cloudinary.com/hoslack/image/upload/v1524319699/imageedit_6_4169369105_ekaxlm.png)


![Sign In](http://res.cloudinary.com/hoslack/image/upload/v1524319706/imageedit_7_5004553090_i3lgvg.png)

## Technology Stack:
- [PostgreSql](https://www.postgresql.org/) with [SQLAlchemy](https://www.sqlalchemy.org/) (database and ORM)
- [Flask](http://flask.pocoo.org/) (A Python microframework)
- [Reactjs](https://reactjs.org/) (A javaScript front-end framework)
- HTML and CSS

## Tools:
- [Pivotal Tracker](www.pivotaltracker.com) (A project management tool)
- [Pytest](https://docs.pytest.org/en/latest/) (A tool for testing)
- [VirtualEnv](https://virtualenv.pypa.io/en/stable/) (A tool for holding all dependencies used in the project)
- [Coverage](https://coverage.readthedocs.io/en/coverage-4.5.1/) (A tool for getting the coverage of the tests)
- [Travis CI](https://travis-ci.org/) (An online tool for continuous integration after testing)

## Getting Started
If you want to try out this application at this stage of development you just have to follow the simple instructions below:

On your terminal, paste these commands one by one.

***Please Ensure you have python3 and above before doing this***

Install pip 

`sudo apt-get install python-pip`

Clone the repository

`git clone https://github.com/hoslack/Book-A-Meal.git`

Get into the root direcory

`cd Book-A-Meal/`

Install virtualenv

`pip install virtualenv`

Create a virtual environment in the root directory

`virtualenv myenv`  ***or***

`virtualenv -p python3 myenv` ***or***

`python3 -m venv myenv` ***using python3 command***

Activate the virtualenv

`source myenv/bin/activate`

Install the requirements of the project

`pip install -r requirements.txt`

Create a file in the root directory called `.env` and add the two lines below

`export FLASK_APP="runapp.py"`

`export SECRET="secret-string-random-veryrandom"`

Activate the env variables 

`source .env`

Run the application 

`flask run`

The run tests 

`pytest tests`

***Done! That's all you need to get the project up and running***

## API Endpoints 
These you can test in your browser, or  Postman, or curl

URL Endpoint	|               HTTP Request   | Resource Accessed | Access Type|
-------------------|-----------------|-------------|------------------
/api/v1/auth/signup   |      POST	| Register a new user|public
/api/v1/auth/login	  |     POST	| Login and add user to session|public
/api/v1/auth/logout	  |     POST	| Logout and delete session|public
/api/v1/meals	  |     GET	| Get all the meal options|Admin Only(Private)
/api/v1/meals	              |      POST	|Add a meal option|Admin Only(Private)
/api/v1/meals/<mealId>	              |      PUT	|     Update the information of a meal option|Admin Only(Private)
/api/v1/meals/<mealId>            |  	DELETE	    | Remove a meal option | Admin Only(Private)
/api/v1/menu/	          |      POST	|     Setup the menu for the day  |Admin Only(Private)
/api/v1/menu/	          |      GET	| Get the menu for the day |Authenticated user(Private)
/api/v1/orders  |           POST    |Select the meal option from the menu|Authenticated user(Private)
/api/v1/orders/<orderId>     |     PUT	| Modify an order |Authenticated user(Private) (Time bound)
/api/v1/orders|	GET	| Get all the orders  |Admin Only(Private)


## Contributing
I appreciate your eagerness to chip in in this wonderful course but you will have to wait for a **month** or two. :blush:

## Author
- **Hoslack Ochieng** [@Hoslack](@hoslack)

## Licensing 
Book-A-Meal is [MIT Licensed](LICENSE.md)

## Acknowledgements
[Andela](andela.com) - *for giving me the chance and an awesome community to work with*
