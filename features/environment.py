from behave import *
import time
import os
from environments import *

def before_feature(context, feature):
    context.users = {}

def before_scenario(context, scenario):
    time.sleep(REDIS_EXPIRE_TIME)