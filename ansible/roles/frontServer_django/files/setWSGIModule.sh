#!/bin/bash
touch /etc/httpd/conf.modules.d/mod_wsgi.conf
mod_wsgi-express module-config > /etc/httpd/conf.modules.d/mod_wsgi.conf


documentRoot='/usr/local/django/codingTest'
projectName='codingTest'
envPath='/usr/local/env'

echo "ServerName localhost" >> /etc/httpd/conf/httpd.conf

touch /etc/httpd/conf.d/vhost.conf
cat << EOF > /etc/httpd/conf.d/vhost.conf
<VirtualHost *:80>

	ServerName localhost
	DocumentRoot $documentRoot

	Alias /robots.txt $documentRoot/robots.txt
	Alias /favicon.ico $documentRoot/favicon.ico

	Alias /media/ $documentRoot/media/
	Alias /static/ $documentRoot/static/

	<Directory $documentRoot>
		<IfVersion < 2.4>
			Order allow,deny
			Allow from all
		</IfVersion>
		<IfVersion >= 2.4>
			Require all granted
		</IfVersion>
	</Directory>

	<Directory $documentRoot/media>
		<IfVersion < 2.4>
			Order allow,deny
			Allow from all
		</IfVersion>
		<IfVersion >= 2.4>
			Require all granted
		</IfVersion>
	</Directory>

	<Directory $documentRoot/static>
		<IfVersion < 2.4>
			Order allow,deny
			Allow from all
		</IfVersion>
		<IfVersion >= 2.4>
			Require all granted
		</IfVersion>
	</Directory>

	<Directory $documentRoot/media>
		<IfVersion < 2.4>
			Order allow,deny
			Allow from all
		</IfVersion>
		<IfVersion >= 2.4>
			Require all granted
		</IfVersion>
	</Directory>

	<Directory $documentRoot/static>
		<IfVersion < 2.4>
			Order allow,deny
			Allow from all
		</IfVersion>
		<IfVersion >= 2.4>
			Require all granted
		</IfVersion>
	</Directory>

	WSGIDaemonProcess $projectName python-home=$envPath/$projectName python-path=$documentRoot
	WSGIProcessGroup $projectName

	WSGIScriptAlias / $documentRoot/$projectName/wsgi.py

	<Directory $documentRoot/$projectName>
		<IfVersion < 2.4>
			Order allow,deny
			Allow from all
		</IfVersion>
		<IfVersion >= 2.4>
			Require all granted
		</IfVersion>
	</Directory>
</VirtualHost>
EOF
