# LearnStock

1.Aims

The application aims to provide a learning website integrating a stock simulator with guiding information 
and stock knowledge information learning for first-time investors. This website should use plain language 
to help users learn stock knowledge and understand the stock investment process.


2.Function

1）Users can sign up, log in and log out successfully in this application. 
2）Users can edit their password and profiles. The admin can manage all the accounts.
3）Users can know how to buy and sell the stock with virtual money. 
4）Users can browse stock learning material that has been categorized. 
5）Users can browse some hot stock news.
6）Users can add new stock categories and add learning material themselves according to categorized to share with other users.
7）Users can add their comments for different learning material or news.

3.How to deploy it
step 1: create a virtual environment
      mkvirtualenv --python=python3.9 stock
      
step 2: Install all the required packages(could using "requirement.txt")
      pip install Django==2.1.5
      pip install django-registration-redux==2.2
      pip install Django==2.1.5
      pip install Pillow==8.3.1
      pip install requests==2.26.0
      
step 3:Enter the virtual environment and git the code from
       https://github.com/1YueyueLiu/LearnStock.git
       
step 4:Set up the database
        python manage.py makemigrations stock
        python manage.py migrate
        python populate_simulator.py
        python manage.py createsuperuser
        
4. the construction of code
    LearnStock
         __int__.py
         settings.py
         urls.py
         wsgi.py
    media
        profile_images
    static
        assets
        css
        images
        js
    stock
         migrations
         templatetags
         __int__.py
         admin.py
         apps.py
         .....
         urls.py
         views.py
     templates
         registrations
         stock
     .gitignore
     db.sqlite3
     manage.py
     populate_simulator.py
     requirements.txt
     
 5.The demo of application
 
https://youtu.be/n-XjoWe1pAw!

      
         
     
        
       
      
