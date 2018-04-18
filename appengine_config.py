import os
from google.appengine.ext import vendor

vendor.add(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'lib'))
vendor.add(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'g'))