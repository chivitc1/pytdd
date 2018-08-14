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