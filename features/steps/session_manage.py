from behave import *
from chatbot import *
from RedisDAO import *
from User import *
import time
import os
from environments import *

def compose_question_array(questions):
    array = questions.split(',')
    return array

def map_function(item):
    return item['question']

@given('User "{user_id}" login WeChat')
def step_impl(context, user_id):
    user = User(user_id)
    context.users[user_id] = user


@given('a WeChat service "{service_id}"')
def step_impl(context, service_id):
    robot = RobotService(service_id)
    context.robot = robot


@given('a Redis service')
def step_impl(context):
    redis = RedisDAO()
    context.redis = redis

@given('the conversation expired time is "{expire_time}" seconds')
def step_impl(context, expire_time):
    REDIS_EXPIRE_TIME = int(expire_time)

@given('User "{user_id}" already sent messages "{questions}" to WeChat service')
def step_impl(context, user_id, questions):
    user = context.users[user_id]
    robot = context.robot
    question_array = compose_question_array(questions)
    for question in question_array:
        user.send_message_to_robot(question, robot)

@when('User "{user_id}" send a message "{question1}" to WeChat service after "{wait_time1}" seconds and send a message "{question2}" to WeChat service after "{wait_time2}" seconds')
def step_impl(context, user_id, question1, wait_time1, question2, wait_time2):
    user = context.users[user_id]
    robot = context.robot
    time.sleep(int(wait_time1))
    user.send_message_to_robot(question1, robot)
    time.sleep(int(wait_time2))
    user.send_message_to_robot(question2, robot)

@when('User "{user_id}" send a message "{question}" to WeChat service after "{wait_time}" seconds')
def step_impl(context, user_id, question, wait_time):
    time.sleep(int(wait_time))
    user = context.users[user_id]
    robot = context.robot
    user.send_message_to_robot(question, robot)

@then('The Redis should be able to read user "{user_id}" data "{messages}"')
def step_impl(context, user_id, messages):
    user = context.users[user_id]
    robot = context.robot
    redis = context.redis
    data = redis.get_cached_data(user.user_id, robot.service_id)
    dialogs = data['dialogs']
    cached_questions = list(map(map_function, dialogs))
    varify_questions = compose_question_array(messages)
    print (cached_questions)
    print (varify_questions)
    assert(cached_questions == varify_questions)