# 100 Days of Code: Updated Coffee Shops Site

Day 88 of the 100 Days of Code course. For this project, the goal was to create an updated version of the coffee shops project from earlier in the course. 

The oroginal coffee shop website from day 62 had three routes. The home page, a page that lists the coffee shops and a hidden route, add, that can be used to add coffee shops to the shops list. When a shop was added using the add route, the details for that shop were saved in a csv file. The route that listed the shops was then rendered using the rows from that csv file.

For my personal touches for this project, I added the following functionality:

A contact page was added for users to send emails to the owner of the website.

Login functionality was added to the website. Only users that have accounts created can add, edit, and remove websites from the shops list page. A bit of touch that I kept from the original project was that I made it so that the login page was not listed in the navbar. Users must navigate to the login page to login before that can make changes to the website.

Instead of using a CSV to store shop information, I created a SQLite database to store the list of shops as well as the users that have registered for the website. The shops list page was then rendered using the data from that database.

This was my first flask project that I completed as part of the portfolio projects section of this course so some of the styling and code used to render the web pages and forms, could use some updating. However, the pages and functionality work well for the project. Subsequent projects such as the To-do list site and online shop project are coded more cleanly.
