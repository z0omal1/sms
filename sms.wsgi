#!/usr/bin/python2.6
import sys
import pprint
import logging

logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/var/www/sms/sms")
pprint.pprint(sys.path)
from main import app as application
