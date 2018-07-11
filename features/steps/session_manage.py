from behave import *
from chatbot import *
from redis_dao import *
import time
import os
from environments import *

@given('User1 with id "{id}" login WeChat')
def step_impl(context, id):
    context.user1 = id

@given('User2 with id "{id}" login WeChat')
def step_impl(context, id):
    context.user2 = id

@given('users subscribe account "{service_id}"')
def step_impl(context, service_id):
    context.service_id = service_id

@given('the conversation expired time is "{expire_time}" seconds')
def step_impl(context, expire_time):
    print (expire_time)
    REDIS_EXPIRE_TIME = expire_time

@given('User1 send a message "{question}"')
def step_impl(context, question):
    handle_question_from_user(context.user1, context.service_id, question)
    
@given('User1 send a message "{question}" after "{wait_time}" seconds')
def step_impl(context, question, wait_time):
    time.sleep(int(wait_time))
    handle_question_from_user(context.user1, context.service_id, question)

@when('User1 send a message "{question}"')
def step_impl(context, question):
    handle_question_from_user(context.user1, context.service_id, question)
    session_id = cache_dao.get_session_id(context.user1, context.service_id)
    print (session_id)
    context.session_id = session_id

@when('User1 send a message "{question}" after "{wait_time}" seconds')
def step_impl(context, question, wait_time):
    time.sleep(int(wait_time))
    handle_question_from_user(context.user1, context.service_id, question)
    session_id = cache_dao.get_session_id(context.user1, context.service_id)
    context.session_id = session_id

@when('User2 send a message "{question}"')
def step_impl(context, question):
    handle_question_from_user(context.user2, context.service_id, question)
    session_id = cache_dao.get_session_id(context.user2, context.service_id)
    print (session_id)
    context.session_id_2 = session_id


def compose_question_array(questions):
    array = questions.split(',')
    return array

def map_function(item):
    return item['question']
    

@then('Redis server should cache User1 data "{questions}"')
def step_impl(context, questions):
    data = cache_dao.get_cached_data(context.session_id)
    dialogs = data['dialogs']
    cached_questions = list(map(map_function, dialogs))
    varify_questions = compose_question_array(questions)
    print (REDIS_EXPIRE_TIME)
    print (cached_questions)
    print (varify_questions)
    assert(cached_questions == varify_questions)

@then('Redis server should cache User2 data "{questions}"')
def step_impl(context, questions):
    data = cache_dao.get_cached_data(context.session_id_2)
    dialogs = data['dialogs']
    cached_questions = list(map(map_function, dialogs))
    varify_questions = compose_question_array(questions)
    print (cached_questions)
    print (varify_questions)
    assert(cached_questions == varify_questions)