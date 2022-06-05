class AlertSetup:
    def __init__(self, chat_id, gas_threshold_gwei=None, cooldown_seconds=None):
        self.chat_id = chat_id
        self.gas_threshold_gwei = gas_threshold_gwei
        self.cooldown_seconds = cooldown_seconds

    def try_parse_gas_threshold(self, input):
        # tries to parse gas threshold and returns if gwei if success, returns "False if not"
        lower_bound_gwei = 1
        upper_bound_gwei = 9999
        try:
            gwei_threshold = int(float(input))
            if not lower_bound_gwei <= gwei_threshold <= upper_bound_gwei:
                return False
            self.gas_threshold_gwei = gwei_threshold
            return gwei_threshold
        except:
            return False

    def try_parse_cooldown(self, input):
        # tries to parse cooldown hours. returns cd seconds if success, returns "False" if not
        lower_bound_hours = 1
        upper_bound_hours = 9999
        try:
            cooldown_hours = int(float(input))
            if not lower_bound_hours <= cooldown_hours <= upper_bound_hours:
                return False
            cooldown_seconds = cooldown_hours * 3600
            self.cooldown_seconds = cooldown_seconds
            return cooldown_seconds
        except:
            return False
