class TimeHandler:
    available_time = ["bullet", "blitz", "quick"]

    def __call__(self, value):
        if value not in self.available_time:
            raise ValueError
        else:
            return value

time_handler = TimeHandler()
