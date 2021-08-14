def compute_available_action(rules):
    def watcher(this):
        base_actions = rules(this) 
        actions = filter(lambda x: not x[1], base_actions)
        return list(actions)
    return watcher


class Ctrl:
    def __init__(self):
        pass

    def exit(self):
        return False

    def show_actions(self, actions_available, callbacks):
        user_choice = self.view.show(actions_available)
        try:
            callback_name = actions_available[int(user_choice)][2]
            callback_methode = callbacks[callback_name]
            callback_methode()

        except ValueError:
            self.show_actions(actions_available, callbacks)
        return