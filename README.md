django_mushroom_example
=======================

This is a example project to show how to use [django-mushroom](https://github.com/DebVortex/django-mushroom "django-mushroom").

Installation
------------

You have to checkout and install several projects. I would recommend to use virtualenv to do this:

    $ pip install virtualenv
    [...]
    $ virtualenv my_virtual_env
    $ cd my_virtual_env
    /my_virtual_env $ source bin/activate
    (my_virtual_env) /my_virtual_env $

To start the example project, we need django-mushroom and mushroom:

    $ git clone https://bitbucket.org/terreon/mushroom.git
    $ cd mushroom/
    /mushroom $ pip install -r requirements.txt
    [...]
    /mushroom $ python setup.py install
    [...]
    /mushroom $ cd ..
    $ git clone git://github.com/DebVortex/django-mushroom.git
    $ cd django-mushroom/
    django-mushroom/ $ python setup.py install
    [...]

Now navigate to the directory you want to set up the example project. Check it out and start the server:

    $ git clone git://github.com/DebVortex/django_mushroom_example.git
    $ cd django_mushroom_example/
    /django_mushroom_example $ python manage.py syncdb
    [...]
    /django_mushroom_example $ python manage.py runserver_with_mushroom
    Validating models...

    0 errors found
    Django version 1.4.2, using settings 'django_mushroom_example.settings'
    Development server is running at http://127.0.0.1:8000/
    Mushroom server is running at http://127.0.0.1:8100/
    Quit the server with CONTROL-C.

Now you are able to visit ``http://127.0.0.1:8000/`` and take a look at a chat inside of django. The server also supports a "whisper" function. Just type `/msg <username> <message>`