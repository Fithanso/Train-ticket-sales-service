<h1>Version: 1.0.0</h1>

This is the application where users can choose a train route based on country, departure, arrival cities and date.
Hope you will find it worth your attention.

Project was developed with Python 3.8 and Django 4.1

You can find suitable voyage by choosing railway stations on the start page.

The application is built on the assumption that there are only two classes of seats: regular and business class. 
And also that all wagons are the same.

NOTE: 'bc' in code means 'business class'

WARNING! The program does some pdf rendering with pdfkit. You need to install wkhtmltopdf utility.

Application has divided setting files - a base one, one for local development by me and one for production.

The core application is train_main_app. Probably should have named it 'core' but too lazy to rename it.
Applications:
search - the most interesting. Searches for suitable itineraries.
site_api - contains api functions.
tickets - contains everything related to the purchase of tickets and search for already purchased ones.
train_main_app - core app, contains common functions and classes

get_object_or_404 is not used in views. I use InvalidParametersRedirectMixin and validators instead because I want 
user redirected rather than shown a 404 page.

Warning! Application has one weakspot - if two users try to buy same tickets almost immediately, both of them will have tickets bought.

If you don't use any real SMTP server, don't forget to turn on the smtp debug:
python -m smtpd -n -c DebuggingServer localhost:1025

