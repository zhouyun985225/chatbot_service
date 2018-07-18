Feature: Support conversational dialog
    To support conversational dialog, the WeChat server should cache dialog concontext to Redis.

    Background: Define users, WeChat account and conversation expire time
        Given User "abcd1234" login WeChat
        And a WeChat service "aiyizheziyi"
        And a Redis service
        And the conversation expired time is "5" seconds

    Scenario: User's question in expired time should be considered as the same conversation
        Given User "abcd1234" already sent messages "question1" to WeChat service
        When User "abcd1234" send a message "question2" to WeChat service after "2" seconds
        Then The Redis should be able to read user "abcd1234" data "question1,question2"

    Scenario: User's question out of expired time should not be considered as the same conversation
        Given User "abcd1234" already sent messages "question1" to WeChat service
        When User "abcd1234" send a message "question2" to WeChat service after "6" seconds
        Then The Redis should be able to read user "abcd1234" data "question2"

    Scenario: When user send a message with in expire time, the expire timer should reset
        Given User "abcd1234" already sent messages "question1" to WeChat service
        When User "abcd1234" send a message "question2" to WeChat service after "3" seconds and send a message "question3" to WeChat service after "3" seconds
        Then The Redis should be able to read user "abcd1234" data "question1,question2,question3"

    Scenario: Another user's question should not be considered as the same conversation
        Given User "dcba4321" login WeChat
        And User "abcd1234" already sent messages "question1" to WeChat service
        When User "dcba4321" send a message "question2" to WeChat service after "2" seconds
        Then The Redis should be able to read user "dcba4321" data "question2"

    Scenario: User's no more than 5 previous question in the same conversation should be cached
        Given User "abcd1234" already sent messages "question1,question2,question3,question4" to WeChat service
        When User "abcd1234" send a message "question5" to WeChat service after "2" seconds
        Then The Redis should be able to read user "abcd1234" data "question1,question2,question3,question4,question5"

    Scenario: User's more than 5 previous question in the same conversation will not be cached
        Given User "abcd1234" already sent messages "question1,question2,question3,question4,question5" to WeChat service
        When User "abcd1234" send a message "question6" to WeChat service after "2" seconds
        Then The Redis should be able to read user "abcd1234" data "question2,question3,question4,question5,question6"