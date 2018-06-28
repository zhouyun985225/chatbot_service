from behave import *
from letterchecker import *

@given('a letter checker')
def step_impl(context):
    letterchecker = letter_checker()
    context.checker = letterchecker

@when('the letter is "{letter}"')
def step_impl(context, letter):
    context.letter = letter

@then('the letter checker should output "{result}"')
def step_impl(context, result):
    rs = context.checker.check_letter_is_y(context.letter)
    assert(rs==result)