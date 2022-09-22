----- run commands -------
cd task
pip install djangorestframework
pip install django-rest-knox
django-admin startproject a .
django-admin startapp users 

------ add to code ---------

in settings.py add in INSTALLED_APPS

'rest_framework',
'knox',
'users',
____________________________

open browser at 127.0.0.1:8000

----- run commands --------
py manage.py createsuperuser
username:- admin
password:- admin
_________________________

to access admin panel 127.0.0.1:8000/admin
enter username and password

__________________________________

Database : sqlite3
python manage.py migrate
 python .\manage.py runserver