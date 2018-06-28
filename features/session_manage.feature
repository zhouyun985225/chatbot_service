Feature: Support conversational dialog

    Background: Chatbot setting
        Given the conversation expired time is "10" seconds
        Given a user with id "abcd1234"

    Scenario: User's question in expired time should be considered as the same conversation
        Given the user asked a question "导航到北京协和医院"
        When the user ask question "天气如何" after "5" seconds
        Then the user should receive response "北京的天气是 ..."

    Scenario: Another user's question should not be considered as the same conversation
        Given the user asked a question "导航到北京协和医院"
        Given a new user with id "qwerty4321"
        When the user ask question "天气如何" after "5" seconds
        Then the user should receive response "您是问哪个地方的天气？"

    Scenario: User's question out of expired time should not be considered as the same conversation
        Given the user asked a question "导航到北京协和医院"
        When the user ask question "天气如何" after "15" seconds
        Then the user should receive response "您是问哪个地方的天气？"

    Scenario: User's more than 5 privious question in the same conversation will not be considered relevant with current question
        Given the user asked a question "导航到北京协和医院"
        Given the user asked a question "什么是洗鼻？"
        Given the user asked a question "放疗为什么会食欲不振？"
        Given the user asked a question "验血在什么地方？"
        Given the user asked a question "放疗能治疗什么癌症？"
        Given the user asked a question "什么是放疗？"
        When the user ask question "天气如何" after "5" seconds
        Then the user should receive response "您是问哪个地方的天气？"