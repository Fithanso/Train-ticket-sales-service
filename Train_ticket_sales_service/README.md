<h1>Version: 1.2.0</h1>

This is the application where users can choose a train route based on country, departure, arrival cities and date.
Hope you will find it worth your attention.

Project was developed with Python 3.8 and Django 4.1

You can find suitable voyage by choosing railway stations on the start page.

<h3>To test the main feature, on the start page choose the following: Leningradskiy r.s. -> Moskovskiy r.s. at 31.08.2022.</h3>

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

API GUIDE

You need to be registered and logged into the system to get an API token.
All models except SiteSetting are represented with all necessary CRUD operations that DRF provides:

1. site_root/rest_api/voyages/
2. site_root/rest_api/s_in_voyages/
3. site_root/rest_api/stations/
4. site_root/rest_api/cities/
5. site_root/rest_api/countries/
6. site_root/rest_api/trains/
7. site_root/rest_api/purchased_tickets/


Apart from that, there are two custom routes: 

1. [GET] site_root/rest_api/voyages/search/<departure_station_id>/<arrival_station_id>/<departure_date (YYYY-MM-DD)>/
2. [POST] site_root/rest_api/purchased_tickets/purchase/
You need to pass following parameters (examples): 
voyage_pk (3), departure_en_route_id (15), arrival_en_route_id (18), seat_numbers (125,126,127), customers_timezone (Europe/Moscow), customers_region_code (RU), customers_phone_number (9037930202), customers_email (example@mail.com).

You can also filter PurchasedTickets by customers_phone_number field with a request like this:
site_root/rest_api/purchased_tickets?customers_phonenumber=9037930202

