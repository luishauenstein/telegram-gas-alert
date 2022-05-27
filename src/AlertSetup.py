class AlertSetup:
    def __init__(self, chat_id, gas_threshold_gwei=None, cooldown_seconds=None):
        self.chat_id = chat_id
        self.gas_threshold_gwei = gas_threshold_gwei
        self.cooldown_seconds = cooldown_seconds
