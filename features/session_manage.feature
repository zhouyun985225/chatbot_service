Feature: Support conversational dialog
    To support conversational dialog, the WeChat server should cache dialog concontext to Redis.

    Background: Define users, WeChat account and conversation expire time
        Given User1 with id "abcd1234" login WeChat
        And users subscribe account "aiyizheziyi"
        And the conversation expired time is "5" seconds

    Scenario: User's question in expired time should be considered as the same conversation
        Given User1 send a message "question1"
        When User1 send a message "question2" after "2" seconds
        Then Redis server should cache User1 data "question1,question2"

    Scenario: User's question out of expired time should not be considered as the same conversation
        Given User1 send a message "question1"
        When User1 send a message "question2" after "10" seconds
        Then Redis server should cache User1 data "question2"

    Scenario: When user send a message with in expire time, the expire timer should reset
        Given User1 send a message "question1"
        Given User1 send a message "question2" after "3" seconds
        When User1 send a message "question3" after "3" seconds
        Then Redis server should cache User1 data "question1,question2,question3"

    Scenario: Another user's question should not be considered as the same conversation
        Given User2 with id "dcba4321" login WeChat
        When User1 send a message "question1"
        When User2 send a message "question2"
        Then Redis server should cache User1 data "question1"
        And Redis server should cache User2 data "question2"

    Scenario: User's no more than 5 previous question in the same conversation should be cached
        Given User1 send a message "question1"
        And User1 send a message "question2"
        And User1 send a message "question3"
        And User1 send a message "question4"
        When User1 send a message "question5" after "2" seconds
        Then Redis server should cache User1 data "question1,question2,question3,question4,question5"

    Scenario: User's more than 5 previous question in the same conversation will not be cached
        Given User1 send a message "question1"
        And User1 send a message "question2"
        And User1 send a message "question3"
        And User1 send a message "question4"
        And User1 send a message "question5"
        When User1 send a message "question6" after "2" seconds
        Then Redis server should cache User1 data "question2,question3,question4,question5,question6"