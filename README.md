# flask-blog
A simple blog made with flask

The blog is still in development but has some cool features, it uses MySQL as a database and i have provided a create_db file that will create
the required tables for the website to work


# How to run

1# Clone repository

2# In the directory run pip install -r requirements.txt

3# Run the creadte_db script ( you might have to run a migration with "flask db migrate" and "flask db upgrade" ) 

4# Set Flask environment variables to "FLASK_APP=app.py" and "FLASK_ENV=development"

5# Run the "flask run" command


# TODO - for now

Filter out requirements.txt file as it is a little bloated

Add image upload
