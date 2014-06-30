import sys
import os
curr_dir = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(curr_dir, '..', '..', 'google_appengine')))
sys.path.insert(0, os.path.abspath(os.path.join(curr_dir, '..', '..', 'mind-well')))
sys.path.insert(0, os.path.abspath(os.path.join(curr_dir, '..', '..', 'mind-well', 'reportlab.zip')))
sys.path.insert(0, '/var/lib/jenkins/google_appengine')
os.environ['DJANGO_SETTINGS_MODULE'] = 'Mindwell.settings'
import logging
logging.error(sys.path)
print(sys.path)
import dev_appserver
dev_appserver.fix_sys_path()
