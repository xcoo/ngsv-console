# NGSV Console

Web console for accessing database of NGSV.

# Requirements

* Python (v2.7)
    * pysam (>= v0.7)
    * Flask
    * Flask-SQLAlchemy
    * gevent
    * gevent-websocket
    * Celery
    * MySQL-python
    * SQLAlchemy
    * Cython
* MySQL
* RabbitMQ

# Installation

## Install ngsv-tools

```
$ git clone git@github.com:xcoo/ngsv-tools.git
$ cd ngsv-tools
$ python setup.py install
```

## Create database

ngsv uses MySQL database.
First, create database.

```
$ cd [ngsv-tools]/db
$ mysql -u root -p < ngsv.sql
```

## Setup database

Setup configuration.

```
$ cp config/ngsv.ini.example config/ngsv.ini
```

```
[db]
host=mysql_host
user=mysql_user
password=mysql_password
db_name=samdb

[console]
debug=False
testing=False

upload_dir=/path/upload_dir/
upload_dir_url=http://example.com/upload_files/

host=example.com
```

Start MySQL and RabbitMQ.

Start Celery.

```
$ cd ngsvconsole
$ celery worker --app=taskserver -l info
```

Start web server

```
$ ./run.py --wsgi
```

Browse `http://localhost:5000`. And upload bam/bed files.

## Load data of human genome

Load cytobands and refgenes to MySQL database by the following commandline ngsvtools.

```
$ ngsv loadcytoband [--dbuser USER] [--dbpassword PASSWORD]
$ ngsv loadrefgene [--dbuser USER] [--dbpassword PASSWORD]
```

# License

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License.

You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and limitations under the License.
