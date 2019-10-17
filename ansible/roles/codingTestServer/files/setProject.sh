#!/bin/bash

djangoPath='/usr/local/django'
projectName='codingTest'
documentRoot=$djangoPath'/'$projectName
appName='codingContents'

echo "export PublicIP=\$(curl ipv4.icanhazip.com)" >> /etc/profile
echo "export PublicIP=\$(curl ipv4.icanhazip.com)" >> /root/.bashrc
. /root/.bashrc

sed -i "s/'ENGINE': 'django.db.backends.sqlite3',/'ENGINE': 'django.db.backends.mysql',/g" $documentRoot/$projectName/settings.py
sed -i "s/'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),/'NAME': 'codingTest', \n        'UESR': 'codingTest',\n        'PASSWORD': 'It12345!',\n        'HOST': 'codingtestdb.cq7rwyqbhtdi.ap-northeast-2.rds.amazonaws.com',\n        'PORT': '3306',\n/g" $documentRoot/$projectName/settings.py

sed -i "s/ALLOWED_HOSTS = \[\]/ALLOWED_HOSTS = \['$PublicIP'\]/g" $documentRoot/$projectName/settings.py

sed -i "s/INSTALLED_APPS = \[/INSTALLED_APPS = \[\n    '$appName',/g" $documentRoot/$projectName/settings.py
