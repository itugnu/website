# website - This is Amazing Website
Public website for ITUGnu

[![Build Status](https://travis-ci.org/itugnu/website.svg?branch=master)](https://travis-ci.org/itugnu/website)
[![Coverage Status](https://coveralls.io/repos/github/itugnu/website/badge.svg?branch=master)](https://coveralls.io/github/itugnu/website?branch=master)

INSTALL
-------

* Clone project from git
* Create virtual environment: `virtualenv venv -p python3.6`
* Switch to virtual environment: `source venv/bin/activate`
* Install requirements: `pip install -r requirements.txt`
* Create `local_settings.py` file in the project root directory
* Initialize database: `./manage.py migrate`
* Run application: `./manage.py runserver`

DEPLOYMENT
----------

* Ubuntu: `apt install python3.6 python3.6-dev nginx libpq-dev postgresql postgresql-contrib`
* Set-up database and create settings file using `cp local_settings.template.py local_settings.py` (hint: use link (`ln -s`))
* Install virtualenv: `sudo pip3 install virtualenv`
* Create user: `useradd -m itugnu`
* Check `etc` folder for deployment files (nginx & supervisor)
* Application uses gunicorn and PostgreSQL (psycopg2-binary) database for deployment
* Translations needs to be compiled to use them: `./manage.py compilemessages`


LICENSE
-------

    Copyright 2018 ITUGnu <info@itugnu.org>

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

AUTHORS
-------

* Emin Mastizada <emin@linux.com> - Code
* Ahmed Ihsan Erdem <ihsan@itugnu.org> - Code
* Muhammed Ali Yeter <muhammed@itugnu.org> - Code
* Sercan Sahan <sercan@itugnu.org> - Code
* Emek Gozluklu <emek@itugnu.org> - Code
* Jabrail Lezgintsev <lezgintsev13@yandex.ru> - Russian Translation
