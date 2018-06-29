Feature: Support conversational dialog
    To support conversational dialog, the WeChat server should cache dialog concontext to Redis.

    Background: Define users, WeChat account and conversation expire time
        Given User1 with id "abcd1234" login WeChat
        And users subscribe account "aiyizheziyi"
        And the conversation expired time is "15" seconds

    Scenario: User's question in expired time should be considered as the same conversation
        Given User1 send a message "question1"
        When User1 send a message "question2" after "5" seconds
        Then Redis server should cache User1 data '[{"dialog_number":1,"question":"question1","coreference":"question1","intention":"other","answer":"answer1"},{"dialog_number":2,"question":"question2","coreference":"question2","intention":"other","answer":"answer2"}]'

    Scenario: User's question out of expired time should not be considered as the same conversation
        Given User1 send a message "question1"
        When User1 send a message "question2" after "20" seconds
        Then Redis server should cache User1 data '[{"dialog_number":2,"question":"question2","coreference":"question2","intention":"other","answer":"answer2"}]'

    Scenario: When user send a message with in expire time, the expire timer should reset
        Given User1 send a message "question1"
        Given User1 send a message "question2" after "10" seconds
        When User1 send a message "question3" after "10" seconds
        Then Redis server should cache User1 data '[{"dialog_number":1,"question":"question1","coreference":"question1","intention":"other","answer":"answer1"},{"dialog_number":2,"question":"question2","coreference":"question2","intention":"other","answer":"answer2"},{"dialog_number":3,"question":"question3","coreference":"question3","intention":"other","answer":"answer3"}]'

    Scenario: Another user's question should not be considered as the same conversation
        Given User2 with id "dcba4321" login WeChat
        When User1 send a message "question1"
        When User2 send a message "question2"
        Then Redis server should cache User1 data '[{"dialog_number":1,"question":"question1","coreference":"question1","intention":"other","answer":"answer1"}]'
        And Redis server should cache User2 data '[{"dialog_number":1,"question":"question1","coreference":"question1","intention":"other","answer":"answer1"}]'

    Scenario: User's no more than 5 privious question in the same conversation should be cached
        Given User1 send a message "question1"
        And User1 send a message "question2"
        And User1 send a message "question3"
        And User1 send a message "question4"
        When User1 send a message "question5" after "5" seconds
        Then Redis server should cache User1 data '[{"dialog_number":1,"question":"question1","coreference":"question1","intention":"other","answer":"answer1"},{"dialog_number":2,"question":"question2","coreference":"question2","intention":"other","answer":"answer2"},{"dialog_number":3,"question":"question3","coreference":"question3","intention":"other","answer":"answer3"},{"dialog_number":4,"question":"question4","coreference":"question4","intention":"other","answer":"answer4"},{"dialog_number":5,"question":"question5","coreference":"question5","intention":"other","answer":"answer5"}]'

    Scenario: User's more than 5 privious question in the same conversation will not be cached
        Given User1 send a message "question1"
        And User1 send a message "question2"
        And User1 send a message "question3"
        And User1 send a message "question4"
        And User1 send a message "question5"
        When the user ask question "question6" after "5" seconds
        Then Redis server should cache User1 data '[{"dialog_number":2,"question":"question2","coreference":"question2","intention":"other","answer":"answer2"},{"dialog_number":3,"question":"question3","coreference":"question3","intention":"other","answer":"answer3"},{"dialog_number":4,"question":"question4","coreference":"question4","intention":"other","answer":"answer4"},{"dialog_number":5,"question":"question5","coreference":"question5","intention":"other","answer":"answer5"},{"dialog_number":6,"question":"question6","coreference":"question6","intention":"other","answer":"answer6"}]'