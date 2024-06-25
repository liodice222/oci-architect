4-29:
- did some basic additions to my code in the morning and transitioning to getting site up on oracle for the rest of the afternoon. 
-ended up not being able to run an instance so contacted my deloitte coach to resolve this
-attempted to make more front end adjustments but hit blockers with 
    -jinj2 not working properly in my .html for conditional statements 
    -could not install RDKit using conda - got incmopatibilty errors - I wanted to use this for a visual of the search query 

4-30:
I didn't realize I was opening the wrong port to check my server -- once I was on the correct one I realized I had an import loop so I had to create a new database file and re-import my app files to my routes etc. Now everything works in postman. I also had the wrong syntax for connecting my html to my css (i wasn't using the flask syntax) so now that is working. I spent the day trying to navigate my new tenancy and create a new instance however i keep getting the same connection timeout error so i will try to work with someone else on my team to see how to resolve this. for the rest of the day i am trying to implement more functionality to my app. 

5-1
Complteded MVP today and maybe spent too much time trying to connect to a tool for 2d molecule rendering. 

5-2
No coding after last push until  I get this deployed on OCI

5-6 still had trouble with deployment over the weekend - doing some small changes here like updating login functionality before re-attempting deployment. I can deploy it as a static website but i haven't figured out how to deploy it on a wsgi. Also considering creating a separate db with usernames/passwords so that i can incorporate load balancing in deployment. 

5-7 finally got app deployed using nginx and gunicorn wsgi - today i added a new html page for when there is no compound information found, and attempting to create an analytics database and fix my login functionality. right now users can login but it's not secure, i would like to make a logout button and require sign in before being allowed to type into the search bar. 

5-9 created final changes, added an additional search bar in compound_info page, made some CSS changes, made sure that user cannot search before logging in. 