all: test

cleanup_coverage:
	-rm -f htmlcov/*
	-rm -f .coverage*
	-rm -f coverage.xml
	-rm -f coverage_files

unit_test:
	nosetests -v --with-xunit --xunit-file nose_unit_tests.xml --with-coverage -w tests/unit_tests --cover-package=Mindwell
	mv .coverage .coverage.unit_test

altsystem_test: secret_passphrase
	-kill `ps | grep python | sed 's/pts\/*\w*.*//'`
	python2.7 /usr/local/lib/python2.7/dist-packages/coverage/__main__.py run ~/google_appengine/dev_appserver.py mind-well --port 9000 --clear_datastore --skip_sdk_update_check &
	sleep 5
	/usr/bin/nosetests-2.7 --with-xunit -w tests/selenium_tests
	-kill `ps | grep python | sed 's/pts\/*\w*.*//'`
	sleep 5
	mv .coverage .coverage.system_test


system_test: secret_passphrase
	-kill `ps | grep python | sed 's/pts\/*\w*.*//'`
	/usr/bin/python2.7 /usr/local/lib/python2.7/dist-packages/coverage/__main__.py run /var/lib/jenkins/google_appengine/dev_appserver.py mind-well --port 9000 --admin_port 8001 --clear_datastore --datastore_path=./datastore --skip_sdk_update_check &
	sleep 5
	/usr/bin/nosetests -v --with-xunit -w tests/selenium_tests
	-kill `ps | grep python | sed 's/pts\/*\w*.*//'`
	sleep 5
	mv .coverage .coverage.system_test

coverage:
	coverage combine
	coverage html --omit=/*google_appengine/*,mind-well/reportlab.zip/*,/*/pyshared/*,/*/dist-packages/*

alttest: cleanup_coverage unit_test altsystem_test coverage

test: cleanup_coverage unit_test system_test coverage

secret_passphrase:
	if test -f mind-well/Mindwell/Client/secret_info.py; \
	then echo exists; \
	else echo "secret_passphrase='1234567812345678'"     > mind-well/Mindwell/Client/secret_info.py; \
	fi

altrun:
	python2.7 ~/google_appengine/dev_appserver.py mind-well --host 0.0.0.0 --port 9000

run:
	/usr/bin/python2.7 /usr/lib/python2.7/dist-packages/coverage/__main__.py run /var/lib/jenkins/google_appengine/dev_appserver.py mind-well --admin_host 0.0.0.0 --host 0.0.0.0 --port 9000 --clear_datastore --datastore_path=./datastore &

upload_data:
	echo 'XX' | python ~/workspace/google_appengine/appcfg.py upload_data --url http://localhost:9000/remote_api --file=/home/dhooper/mindwell_backups/mindwell_backup_2013_10_06.bin --application=dev~mindwellonline -e test@example.com --passin

stop:
	-kill `ps | grep python | sed 's/pts\/*\w*.*//'`

