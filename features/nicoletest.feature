Feature: Chatbot testing
    Test multiple conversations with chatbot

    Background: Users login weChat and add the subscriptions account
        Given User1 login weChat
        And Add the subscriptions account "AI医者自医"

    Scenario: User1 send a message in the knowledge
        Given User1 open the subscriptions account "AI医者自医"
        When User1 send a message "直肠癌放疗中，应该吃什么类型的食物？"
        Then the subscriptions account response a message "直肠癌应该以高蛋白、高维生素、低脂、易消化的食物为主。如适当增加瘦肉、新鲜蔬菜水果等。以保证在治疗期间的营养需求，有利于组织的修复。鼓励多钦茶水，减轻放射线的辐射损伤，减轻放疗反应。"

    Scenario: User1 send another message in the knowledge
        Given User1 open the subscriptions account "AI医者自医"
        When User1 send a message "面颈部淋巴瘤放疗中，胃纳差、腹泻者吃什么食物？"
        Then the subscriptions account response a message "胃纳差、腹泻者应以易消化，清淡，低纤维食物为主，少食油腻食物；"

    Scenario: User1 send a message is not in the knowledge
        Given User1 open the subscriptions account "AI医者自医"
        When User1 send a message "放疗"
        Then the subscriptions account response a message "请问需要咨询什么类型的放疗呢？"

    Scenario: User1 send multi message with 2 hours
        Given User1 open the subscriptions account "AI医者自医"
        When User1 send a message "得了直肠癌怎么办呢？"
        Then the subscriptions account response a message "应该采取直肠癌放疗"
        When User1 send a message "放疗中应该穿什么衣服？" after "30" seconds
        Then the subscriptions account response a message "衣着要选择柔软、宽大、吸湿性强的棉织品。画放射野的液体会污染衣物，一旦沾污又很难洗净，应考虑放射期间穿较旧的衣服。"
        When User1 send a message "午饭吃什么食物？" after "30" seconds
        Then the subscriptions account response a message "直肠癌应该以高蛋白、高维生素、低脂、易消化的食物为主。如适当增加瘦肉、新鲜蔬菜水果等。以保证在治疗期间的营养需求，有利于组织的修复。鼓励多钦茶水，减轻放射线的辐射损伤，减轻放疗反应。"

    Scenario: User1 send multi messages more than 2 hours
        Given User1 open the subscriptions account "AI医者自医"
        When User1 send a message "得了直肠癌怎么办呢？"
        Then the subscriptions account response a message "应该采取直肠癌放疗"
        When User1 send a message "应该吃什么食物呢？" after "7200" seconds
        Then the subscriptions account response a message "请问是什么类型的放疗呢？"

    Scenario: User1 and User2 send multi messages within 2 hours
        Given User1 open the subscriptions account "AI医者自医"
        And  User2 open the subscriptions account "AI医者自医"
        When User1 send a message "得了直肠癌怎么办呢？"
        Then the subscriptions account response a message "应该采取直肠癌放疗"
        When User1 send a message "应该吃什么食物？"
        Then the subscriptions account response a message "以高蛋白、高维生素、低脂、易消化的食物为主。如适当增加瘦肉、新鲜蔬菜水果等。以保证在治疗期间的营养需求，有利于组织的修复。鼓励多钦茶水，减轻放射线的辐射损伤，减轻放疗反应。"
        When User2 send a message "得了面颈部淋巴瘤怎么办呢？"
        Then the subscriptions account response a message "建议进行面颈部淋巴瘤放疗"
        When User2 send a message "应该吃什么食物？"
        Then the subscriptions account response a message "胃纳差、腹泻者应以易消化，清淡，低纤维食物为主，少食油腻食物；"