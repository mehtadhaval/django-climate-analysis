# Django-Climate-Analysis

 A Django app to fetch and analyze climate data of UK regions. http://www.metoffice.gov.uk/climate/uk/summaries/datasets#Yearorder 

#### Stack
 1. Python 3.4
 2. Django 1.10
 3. MySQL 5.6
 4. Elasticsearch 5.1
 6. Celery with RabbitMQ broker for async tasks

#### How Tos
 1. Create a request to fetch data : Go to django admin at <host>/admin/, Home -> Climate Data -> Requests -> Add New. Provide the type of data and region for which to fetch the data and Save it. It will be processed asynchronously and its status will be updated based on progress. You can re-process the request by selecting the row, and then in the "Action" drop-down, select "Process Request" and click Go.

 2. Current request processing pipeline stores data in two formats :
    
    In same format as received, i.e. One record represents data of all months in a year for given data type and region. This can be explored through Django Admin -> Climate Data -> Climate Data
    
    In a normalized format, where one record represents a single measurement of all data types (tmax, tmin, tmean, rainfall, sunshine) for given month and region. This can be explored through Django Admin -> Climate Data -> Normalized Climate data. The same data is also indexed in Elasticsearch for building visualizations on Kibana.

#### Setup

 1. Create virtualenv and install required dependencies - `virtualenv venv --python=/usr/bin/python3.4` and `pip install -r requirements.pip`
 2. Create `local_settings.py` in `$PROJ_DIR/climate_analysis` and configure according to your development environment
 3. Run migrations - `python manage.py migrate`
 4. Run development server - `python manage.py runserver`

#### Deploy

 1. Preferred deployment stack is nginx-uwsgi(emperor mode) on CentOS 7.
 2. nginx and uwsgi config scripts are located in $PROJ_DIR/deploy folder.
 3. Use `$PROJ_DIR/deploy/uwsgi/uwsgi.service` to configure uwsgi in emperor mode as a `systemd` service.
 4. Use `$PROJ_DIR/deploy/celery/celery.service` to configure celery service.
