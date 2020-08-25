# Django Classy Start

A command Line utility for starting Django projects and apps in a most classy manner.


## Synopsis

* Install `django-classy-start` with `pip` (in your virtual environment).

  ```
  $ pip install django-classy-start
  ```

* Start a project

  ```
  $ classy-start project <project-name> .
  ```

  This initializes a project named `project-name` in the current working directory. Project is initialized with:
    + an `accounts` app containing a custom auth user model
    + a `.env` file with default project secrets
    + and more

  All of these are reflected in your settings file, so you don't have to bother yourself with wiring them up.

* Start your apps this way

  ```Python
  $ classy-start app <app-name>
  ```

  Your settings file isn't touched for this operation, though.


## Status

WIP
