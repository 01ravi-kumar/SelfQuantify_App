# this is the very first file that will run and launch webserver or website.

from website_code import make_app  # we are importing our flask app from __init__.py file

app=make_app()



if __name__ == "__main__": # this line ensure that only if we run this file only then app.debug is allowed, not when we import this file from some other file.
    app.debug=True
    app.run()