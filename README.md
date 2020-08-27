# Django Classy Start

A command line utility for starting Django projects and apps in a most classy manner.


## Synopsis

* Install `django-classy-start` with `pip` (in your virtual environment).

  ```
  $ pip install django-classy-start
  ```

* Start a project

  ```
  $ classy-start project <project-name> .
  ```

  This initializes a project named `project-name` in the current working directory. In addition to the regular Django stuff, project is initialized with:
    + an `accounts` app containing a custom auth user model
    + a `.env` file with default project secrets
    + and more

  All of these are reflected in your settings file, so you don't have to bother yourself with wiring them up.

* Start your apps this way

  ```
  $ classy-start app <app-name>
  ```

  Your settings file isn't touched for this operation, though.


## Why?

### Mostly About the Auth User Model

[The Django docs on auth (customizing)](https://docs.djangoproject.com/en/3.1/topics/auth/customizing/#using-a-custom-user-model-when-starting-a-project) recommends setting up a custom user model for every new project as it's usually a real pain to change the auth user model after the database tables have been created.

And while it's easy **in theory** for everyone to remember to set up their auth user model first thing after starting a project with `django-admin`, it doesn't always pan out that way in practice.

`django-classy-start` handles all of that neatly with `classy-start`.


### And Then There are Secrets

Your `Django` project's `SECRET_KEY` setting is to be kept secret in production. And things like `DEBUG` and `ALLOWED_HOSTS` have different values in different environments.

And it's usually not always immediately clear to n00b1es how to keep these concerns separate in their projects.

`django-classy-start` addresses this problem for everyone by reading environment variables from a project-wide `.env` file.


### That's NOT All Folks!

And this may be my _oh, so, slight_ anal retentiveness speaking, but...

* Apps started by `django-admin` contain some files which have nothing but a line of import (and a line of comment). The imports are unused and linters balk at such things.

* String literals in project and app files are delimited with single quotes. Black, the PSF-blessed Python formatter __dictates__ that double quotes be used.

* `django-classy-start` encourages the good habit of housing test files in a tests directory.


## But Really, Why?

Okay, you got me. I just wanted something relatively non-trivial to do so I can learn more about Django and improve my unit testing game.

And I found that thing in building this.


## Status

v0.0.1 (Beta) released on PyPI
