# pytdd
TDD with Python

# Insstall requirements
- Install Firefox to OS

- Install Geckodriver

curl https://github.com/mozilla/geckodriver/releases/download/v0.21.0/geckodriver-v0.21.0-arm7hf.tar.gz

tar -xf geckodriver*

mv geckodriver ~/.local/bin/

- Make virtual environment name=superlists for user

mkvirtualenv --python=python3.6 superlists

- Activate superlists venv

workon superlists

- Install django & selenium to venv

pip install "django<1.12" "selenium<4"

- Create django project name=superlists in current dir

django-admin.py startproject superlists

- View superlists dir

tree superlists/

- Go to superlists/ as working dir

cd superlists/

- Run server

python manage.py runserver

- Testl

python functional_test.py

- Create new app lists in project superlists

python manage.py startapp lists

- Run unit tests

python manage.py test

- Requirements to test tasks

1. An HTTP request comes in for a particular URL.
2. Django uses some rules to decide which view function should deal with the
request (this is referred to as resolving the URL).
3. The view function processes the request and returns an HTTP response.

So we want to test two things:

• Can we resolve the URL for the root of the site (“/”) to a particular view function
we’ve made?

• Can we make this view function return some HTML which will get the func‐
tional test to pass?

- What’s going on here?

resolve is the function Django uses internally to resolve URLs and find what
view function they should map to. We’re checking that resolve, when called with
“/”, the root of the site, finds a function called home_page.

What function is that? It’s the view function we’re going to write next, which will
actually return the HTML we want. You can see from the import that we’re plan‐
ning to store it in lists/views.py.

- Run test and fails

python manage.py test

(1) What is error

(2) Which test failing, is it our expected?

(3) Look for the code kickoff the failure - a function
