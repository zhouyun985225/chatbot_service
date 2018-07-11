from behave import *
import time
import os
from environments import *

def before_scenario(context, scenario):
    time.sleep(REDIS_EXPIRE_TIME)