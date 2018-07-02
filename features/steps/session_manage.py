from behave import *
from chatbot import *
from redis_dao import *
import time
import os

@given('User1 with id "{id}" login WeChat')
def step_impl(context, id):
    context.user1 = id

@given('User2 with id "{id}" login WeChat')
def step_impl(context, id):
    context.user2 = id

@given('users subscribe account "{service_id}"')
def step_impl(context, service_id):
    context.service_id = service_id

@given('the conversation expired time is {expire_time} seconds')
def step_impl(context, expire_time):
    os.putenv('REDIS_EXPIRE_TIME', expire_time)

@given('User1 send a message "{question}"')
def step_impl(context, question):
    handle_question_from_user(context.user1, context.service_id, question)
    
@given('User1 send a message "{question}" after {wait_time} seconds')
def step_impl(context, question, wait_time):
    time.sleep(wait_time)
    handle_question_from_user(context.user1, context.service_id, question)

@when('User1 send a message "{question}"')
def step_impl(context, question):
    handle_question_from_user(context.user1, context.service_id, question)

@when('User1 send a message "{question}" after {wait_time} seconds')
def step_impl(context, question, wait_time):
    time.sleep(wait_time)
    handle_question_from_user(context.user1, context.service_id, question)

@when('User2 send a message "{question}"')
def step_impl(context, question):
    pass


@then('Redis server should cache User1 data \'question1,question2\'')
def step_impl(context):
    pass
