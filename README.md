# Climate helpdesk

This repository holds the code for https://www.klimaathelpdesk.org, a website aimed at answering questions regarding climate
change, global warming, and related. This project was built using Django & Wagtail.

This is the 2020 redesign variant by Fabrique.
There are some changes. 


### Project setup
    
This project uses docker and docker-compose. 

To build the containers with the right dependencies, install the node dependencies (for the style of the templates) and the pip requirements (for the django applications), use:

    $ docker-compose -f local.yml build

Once this has been done, you can start the containers/services using the following command.

    $ docker-compose -f local.yml up -d

This will take care of starting the database container and the webserver. You'll be able to load the website on your browser by visiting [localhost:8000](http://localhost:8000)

If you remove the ``-d``, you will see the logs on screen, but the containers will run only while your terminal is open. 

To stop the containers you can use:

    $ docker-compose -f local.yml down
    
You can run the other manage commands with: 

    $ docker-compose -f local.yml run --rm django python3 manage.py command_name
    
For the frontend, we use webpack. 

If you are running a container, webpack can be run with:

    $ docker-compose -f local.yml run --rm django /node_modules/.bin/webpack --mode=production
    
You can change the ``--mode`` to ``--mode=development``. 

You can also watch for design changes using:

    $ docker-compose -f local.yml run --rm django /node_modules/.bin/webpack --mode=development --watch
 
