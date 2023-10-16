# library_service

API for library service
With our service users can perform readonly operations with books. Also, can create borrowings of the
books and manage the borrowings. Implemented return functionality for borrowings.
Users can see only their own borrowings and filter them by status(active\inactive).
Implemented payments via stripe (more info - https://stripe.com/docs). Dont forgot to obtain your very own STRIPE_SECRET_KEY
and put it into your .env
Implemented notification service vie Django-Q(https://django-q.readthedocs.io/en/latest/) and Telegram 
Bot API(https://core.telegram.org/bots/api).
Modern authentication via JWT.
API has convenient documentation provided by drf_spectacular and Swagger.
Optimised database queries.


Setup
Create and activate a virtual environment (Python3) using your preferred method. 
This functionality is built into Python, if you do not have a preference.

From the command line, type:

 - git clone https://github.com/N1khto/library_service
 - pip install -r requirements.txt
 - get your own DJANGO_SECRET_KEY (form https://djecrety.ir/) 
and put it into your own .env file or directly into settings
 - python manage.py migrate
 - python manage.py createsuperuser 
 - python manage.py runserver