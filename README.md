# CanIStreamIt

A simple wrapper around the CanIStream.it API built using
ask-alexa-pykit and bulv1ne's CanIStreamIt Python wrapper.

The `skills/MOVIES` file is a list of 6000+ movies to use as a custom
slot type, to improve Alexa's understanding of the movie name.  To
regenerate it, visit netflixable.com, save the HTML source of the "list
of all movies" page, and say `make skills/MOVIES` in toplevel directory
of this package.

Brought to you by Pogo Press.
