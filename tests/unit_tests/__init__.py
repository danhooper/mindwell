import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(__file__, '..', '..', '..', 'mind-well')))
sys.path.insert(0, os.path.abspath(os.path.join(__file__, '..', '..', '..', 'mind-well', 'reportlab.zip')))
sys.path.insert(0, os.path.abspath(os.path.join(__file__, '..', '..', '..', '..', 'google_appengine_1.8.1')))
sys.path.insert(0, os.path.abspath(os.path.join(__file__, '..', '..', '..', '..', '..', '..', 'google_appengine_1.8.1')))
sys.path.insert(0, '/var/lib/jenkins/google_appengine')
os.environ['DJANGO_SETTINGS_MODULE'] = 'Mindwell.settings'
import logging
logging.error(sys.path)
print(sys.path)
import dev_appserver
dev_appserver.fix_sys_path()
