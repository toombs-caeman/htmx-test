This is an experiment to learn about htmx and flask.

I'm only gonna spend a few hours to get a feel for it.

# Initial Concept
Using the sample sqlite database "Chinook", do some basic CRUD.
Flask will provide routing, and basic server side rendering, while HTMX will hopefully enable some dynamic filtering and pagination without writing a lot of javascript.

# the plan
[x] basic view and routes for tracks and artists
[x] list view for tracks and artists
[x] paginate/infinite scroll results
[ ] search for tracks by name (Active Search)
[ ] additional filters
[ ] keyboard shortcuts
[ ] hx-target - spooky action at a distance

# thoughts on Flask+HTMX
Flask is easy to use, as usual, though there still seems to be some impedence mismatch where trying to reuse endpoints on the flask level leads to inefficient use of the database.

HTMX is nice for someone who hates javascript.
It doesn't do everything, but that's probably good.
It takes a bit of thinking to get out of the mindset of passing json to pass data, but the idea does have some merit.

I do wonder though if HTMX lends itself more towards single use endpoints, whereas the same json data can be formatted and displayed in a variety of ways. I could see something based on [template tags](https://www.w3schools.com/TagS/tag_template.asp) which populates data from a json object. HTMX-like request boosting, with a json transport format, which is associated with a template specific to each page.

# Thoughts on these kinds of experiments
I kind of started this on a whim, without much of a plan.

It was helpful to start with the data, since chinook was a good starting point that told me what I was building, without having to come up with a concept (I could easily lose a lot of time there).

[htmx examples](https://htmx.org/examples/) was helpful as an indication of what I should try to do.

I got a bit bogged down in trying to optimize pagination, and so didn't get to experiment with much of the other functionality. For this kind of quick exploration perhaps I should be more strict about keeping it surface level.

I also spent a good bit of time massaging data out of the db. Normally this would be the domain of an ORM, but I'm not familar enough with any of them to spin something up for a quick experiment. Perhaps that should be the topic of my next exploration.

Overall though, very satisfying to just play around with this stuff. I'll have to do more little experiments like this.


# ref
* [flask](https://flask.palletsprojects.com/en/stable/)
    * [jinja](https://jinja.palletsprojects.com/en/stable/)
* [htmx](https://htmx.org/)
* [sqlite3](https://docs.python.org/3/library/sqlite3.html)
    * [chinook](https://www.sqlitetutorial.net/sqlite-sample-database/)
