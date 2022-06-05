from AlertSetup import AlertSetup


class TestAlertSetup:
    def test_init(self):
        alert_setup_1 = AlertSetup(123)
        assert alert_setup_1.chat_id == 123

        alert_setup_2 = AlertSetup(123, 456, 789)
        assert alert_setup_2.chat_id == 123
        assert alert_setup_2.gas_threshold_gwei == 456
        assert alert_setup_2.cooldown_seconds == 789

    def test_try_parse_gas_threshold(self):
        alert_setup_1 = AlertSetup(68976)
        assert alert_setup_1.try_parse_gas_threshold("123") == 123
        assert alert_setup_1.gas_threshold_gwei == 123

        assert alert_setup_1.try_parse_gas_threshold("125.56") == 125
        assert alert_setup_1.gas_threshold_gwei == 125

        assert alert_setup_1.try_parse_gas_threshold("456") == 456
        assert alert_setup_1.gas_threshold_gwei == 456

        alert_setup_1 = AlertSetup(68975)
        assert alert_setup_1.try_parse_gas_threshold("hello my name is 456") == False
        assert alert_setup_1.gas_threshold_gwei == None

        assert alert_setup_1.try_parse_cooldown("4562434") == False
        assert alert_setup_1.cooldown_seconds == None

        assert alert_setup_1.try_parse_cooldown("0") == False
        assert alert_setup_1.cooldown_seconds == None

        assert alert_setup_1.try_parse_cooldown("0.46889769") == False
        assert alert_setup_1.cooldown_seconds == None

    def test_try_parse_cooldown(self):
        alert_setup_1 = AlertSetup(68976)
        expected_result = 442800
        assert alert_setup_1.try_parse_cooldown("123") == expected_result
        assert alert_setup_1.cooldown_seconds == expected_result

        expected_result = 450000
        assert alert_setup_1.try_parse_cooldown("125.56") == expected_result
        assert alert_setup_1.cooldown_seconds == expected_result

        expected_result = 456 * 3600
        assert alert_setup_1.try_parse_cooldown("456") == expected_result
        assert alert_setup_1.cooldown_seconds == expected_result

        alert_setup_1 = AlertSetup(68975)
        assert alert_setup_1.try_parse_cooldown("hello my name is 456") == False
        assert alert_setup_1.cooldown_seconds == None

        assert alert_setup_1.try_parse_cooldown("45612341234") == False
        assert alert_setup_1.cooldown_seconds == None

        assert alert_setup_1.try_parse_cooldown("0") == False
        assert alert_setup_1.cooldown_seconds == None

        assert alert_setup_1.try_parse_cooldown("0.46889769") == False
        assert alert_setup_1.cooldown_seconds == None

        assert alert_setup_1.try_parse_cooldown("safd87asdf") == False
        assert alert_setup_1.cooldown_seconds == None
