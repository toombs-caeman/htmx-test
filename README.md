This is an experiment to learn about htmx and flask.

The idea is to just spend a handful of hours on it and see how far I can get.

# concept
Using the sqlite "Chinook" sample database, create a nice search interface for that data from scratch.

# features
* display track details
    * goto album view
* search for tracks by name
    * paginate/infinite scroll results
* filter by 

# thoughts
* templates
    * `thing.html` - detail view of the object
    * `thing.htmx` - line view of the object
* route
    * `/thing/` - list view
    * `/thing/<id>` - detail view
    * `/thing/new` - create/new
    * `/thing/<id>/edit` - update/edit
    * `/thing/<id>/delete` - delete

# ref
[flask]
[htmx](https://htmx.org/)
[jinja](https://jinja.palletsprojects.com/en/stable/)
[chinook](https://www.sqlitetutorial.net/sqlite-sample-database/)
