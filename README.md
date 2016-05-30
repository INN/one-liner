#Quickstart

	$ mkvirtualenv one-liner
	$ pip install -r requirements.txt
	$ mkdir data
	$ rm -Rf oneliner/migrations;
	$ ./manage.py makemigrations oneliner;
	$ pip install django_extensions
	$ ./manage.py makemigrations oneliner;
	$ ./manage.py migrate
	$ ./manage.py createsuperuser
	$ python manage.py runserver

Check it out at http://localhost:8000/

You can log in with the superuser info you just created.
