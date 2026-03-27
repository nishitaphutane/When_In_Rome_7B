# When_In_Rome_7B

A website dedicated for locals and travellers to see other people favorite spots that you may not typically come across. 

# Tests
In terminal run the command "python manage.py test WhenInRome"

The tests go over if the upvotes are counting properly, if the cities, profiles and reviews are made correctly and also if the following and unfollowing is functioning properly.

## Setup

### Clone the repository
fork and then git clone the repo url

### Install dependencies
pip install -r requirements.txt

### Run migrations
python manage.py migrate

### Populate the database
python populate_script.py

The script creates 4 users, 3 categories, 2 recommendations for each category, 2 reviews for every recommendation, random amount of upvotes for the recomendations, and also gives followers to the users.

### Run the server
python manage.py runserver

### Admin interface
First create a super user using the command "python manage.py createsuperuser"

Then visit the url "http://127.0.0.1:8000/admin/"

Log in with your details and you should be able to access the admin interface

