# *****dependencies*****
export CURR_DIR='/home/deploy/django-climate-analysis/deploy/'

yum -y update
rpm -iUvh https://dl.fedoraproject.org/pub/epel/epel-release-latest-7.noarch.rpm || true
rpm -iUvh http://repoforge.eecs.wsu.edu/redhat/el7/en/x86_64/rpmforge/RPMS/rpmforge-release-0.5.3-1.el7.rf.x86_64.rpm || true
yum -y install wget
yum -y install scl-utils
yum -y install nginx rabbitmq-server
yum -y install python34-devel
yum -y install libtiff-devel libjpeg-devel libzip-devel freetype-devel lcms2-devel libwebp-devel tcl-devel tk-devel
yum -y install mysql-devel

wget https://bootstrap.pypa.io/get-pip.py
python3.4 get-pip.py
pip3 install virtualenv
yum -y install htop ntp git libffi-devel bzip2

# *****timezone*****
systemctl enable ntpd
systemctl start ntpd

echo "# configure timezone"
timedatectl set-timezone America/Los_Angeles
systemctl enable ntpd
systemctl start ntpd

# *****rabitmq*****

echo "# setup rabbitmq"
chkconfig rabbitmq-server on
systemctl enable rabbitmq-server
systemctl start rabbitmq-server
rabbitmqctl status
netstat -anop | grep 5672

# *****nginx*****
rm -rf /etc/nginx/conf.d/*.conf
yes | cp $CURR_DIR/nginx/nginx.conf /etc/nginx/
yes | cp $CURR_DIR/nginx/nginx-climate-analysis.conf /etc/nginx/conf.d/
# directory to keep ssl certs
chown deploy:deploy /etc/nginx/conf.d/nginx-climate-analysis.conf
systemctl enable nginx
systemctl restart nginx

# *****elastic*****
yum -y install java-1.8.0-openjdk.x86_64
java -version
mkdir -p /mnt/strive/softwares/
cd /mnt/strive/softwares/
rpm -iUvh https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-5.0.2.rpm || true
systemctl enable elasticsearch.service
rm -f /etc/elasticsearch/elasticsearch.yml
cp $CURR_DIR/elasticsearch/elasticsearch.yml /etc/elasticsearch/elasticsearch.yml
systemctl start  elasticsearch.service
curl -X GET 'http://127.0.0.1:9200' || true
netstat -naop | grep 9200
curl -X GET 'http://127.0.0.1:9200' || true

# *******kibana*******
rpm -iUvh https://artifacts.elastic.co/downloads/kibana/kibana-5.2.0-x86_64.rpm || true
systemctl daemon-reload
systemctl enable kibana.service
systemctl restart kibana.service

# *******uwsgi*******
mkdir /var/log/uwsgi -p
chown -R deploy:deploy /var/log/uwsgi
yes | cp $CURR_DIR/uwsgi/uwsgi.service /etc/systemd/system/uwsgi.service
mkdir /etc/uwsgi -p
mkdir /etc/uwsgi/vassals -p
yes | cp $CURR_DIR/uwsgi/uwsgi_emperor.ini /etc/uwsgi/emperor.ini
yes | cp -R $CURR_DIR/uwsgi/vassals/*.ini /etc/uwsgi/vassals/
chown -R deploy:deploy /etc/uwsgi
systemctl daemon-reload
systemctl enable uwsgi

# *******celery*******
echo "# create celery log folders :"
mkdir /var/log/celery -p
chown -R deploy:deploy /var/log/celery
mkdir /etc/celery -p
chown -R deploy:deploy /etc/celery
yes | cp $CURR_DIR/celery/celery.service /etc/systemd/system/celery.service
systemctl daemon-reload
systemctl enable celery

echo "Setup successful!!"