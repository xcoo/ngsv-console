# NGSV Console

## Requirements

* Python (v2.7)
    * pysam (>= v0.7)
    * Flask
    * gevent
    * gevent-websocket
    * Celery
    * MySQL-python
    * SQLAlchemy
    * Cython
* MySQL
* RabbitMQ

## Installation

### Create database

ngsv uses MySQL database.
First, create database.

```
$ cd [ngsv dir]/db
$ mysql -u root -p < samdb.sql
```

### Install ngsv-tools

```
$ cd [ngsv dir]/tools
$ python setup.py install
```

### Setup database

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

upload_dir=upload_dir
```

Start MySQL and RabbitMQ.

Start Celery.

```
$ cd [ngsv dir]/console
$ celery worker --app=taskserver -l info
```

Start web server

```
$ ./app.py
```

Browse `http://localhost:5000`. And upload bam/bed files.

Then, load data of the human genome.

```
$ cd [ngsv dir]/console/tools
$ python load_cytoband.py
$ python load_refGene.py
```

## License

Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except in compliance with the License.

You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and limitations under the License.