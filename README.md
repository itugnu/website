# website
Public website for ITUGnu

INSTALL
-------

* Clone project from git
* Create virtual environment: `virtualenv venv -p python3`
* Switch to virtual environment: `source venv/bin/activate`
* Install requirements: `pip install -r requirements.txt`
* Create `local_settings.py` file in the project root directory
* Initialize database: `./manage.py migrate`
* Run application: `./manage.py runserver`

DEPLOYMENT
----------

* Check `etc` folder for deployment files (nginx & supervisor)
* Application uses gunicorn and PostgreSQL (psycopg2-binary) database for deployment


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

* Emin Mastizada <emin@linux.com>
* Ahmed Ihsan Erdem <ihsan@itugnu.org>
* Emek Gozluklu <emek@itugnu.org>
