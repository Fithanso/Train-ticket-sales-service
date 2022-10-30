This is the application where users can choose a train route based on country, departure, arrival cities and date.
Hope you will find it worth your attention.

The application is built on the assumption that there are only two classes of seats: regular and business class. 
And also that all wagons are the same.

NOTE: 'bc' in code means 'business class'

Application has divided setting files - a base one, one for local development by me and one for production.

The core application is train_main_app. Probably should have named it 'core' but too lazy to rename it.
Applications:
search - the most interesting. Searches for suitable itineraries.
site_api - contains api functions.
tickets - contains everything related to the purchase of tickets and search for already purchased ones.
train_main_app - core app, contains common functions and classes

