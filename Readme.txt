The Application is a python flask Application and mongodb cloud is used for database

to run the Application python is necessory

1. Install all the python libraries required as in requirements.txt file.
2. from the commandline/terminal run app.py python file.
3. after running it displays a local host link, copy the link and paste in any browser(Microsoft Edge/Fire fox/chrome).

The application is hosted in heroku url: https://movlib22.herokuapp.com/

After opening the link you will land in the login page from where you can also go for signup page if you are new and register as a new user. after registeration you can login and after successfull login you will be redirected to the home page. In home page you can search for the movies using the search bor and see the list of related movies and you can see any movie details and you can add the movie to the playlist as a private/public list. You can see your play list in the home page if you don't have any list it just shows you dont have any playlist. you can also see others playlist in the home page.

issues:
The retriving of the list is not working properly, the backend is returning blank list to front end, I tried the same code shippet in jupyter notebook and i found it is working, but the same is not working in the flask. 