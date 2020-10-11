# Climate helpdesk

This repository holds the code for https://www.klimaathelpdesk.org, a website aimed at answering questions regarding climate
change, global warming, and related. This project was built using Django & Wagtail.

This is the 2020 redesign variant by Fabrique.
There are some changes. 


### Project setup
    
This project uses docker and docker-compose. 

To build the containers with the right dependencies and also install the pip requirements, use:

    $ docker-compose -f local.yml build

Once this has been done, you can start the containers/services using the following command.

    $ docker-compose -f local.yml up -d

If you remove the ``-d``, you will see the logs on screen, but the containers will run only while your terminal is open.
In this version, the Django process is not run automatically, instead you have to start the server yourself.

The following command will start the django server at port 8000 in the container and mirror it to your host machine.

    $ docker-compose -f local.yml run --publish 127.0.0.1:8000:8000 django python manage.py runserver 0.0.0.0:8000
    
    
You can run the other manage commands with: 

    $ docker-compose -f local.yml run django python manage.py command_name
    
For the frontend, we use webpack. 
To now run webpack you can use the following command in the src dir:

    $ yarn webpack
