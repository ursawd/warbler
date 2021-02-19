# Step Seven: Research and Understand Login Strategy

## Look over the code in app.py related to authentication

* How is the logged in user being kept track of?
  * session["curr_user"]
* What is Flask’s g object?
  * global variable used to store information during the duration of a request cycle
* What is the purpose of add_user_to_g?
  * checks if user logged in, if so query's logged in user info from database and places user object in g global varaible. Current user object now available in all routes without query

* What does @app.before_request mean?
  * This decorator causes the view function which it is attached to be executed before each request
