# oci-project , revised for better security, see project for details

App using a 3rd party API (PubChem) using Flask to get information on a search query for a chemical compound. 
A user must be registered to login and use the search bar. 
Once registered, the username and password is seurely stored in a db using SQLAlchemy. 

Project was hosted on public instance on OCI using nginx and gunicorn as webserver configuration. 

Orginal Project Presentation: https://www.youtube.com/watch?v=PDdxAbJka7E 


Presentation post Secuirty Enhancements: https://www.youtube.com/watch?v=Upq4h0BlOP8

RECAP: 
Added security measures including: 
- prevent DOM XSS Attacks in search fields 
- prevent sql injection by: 1) ensure user input is treated as data by using placeholders 2)sanitize input 3)continue use of ORM for user auth
- prevent broken access control by ensuring autnentication of login
- More granular IM Policies
- OCI deployment examplew with load balancing


