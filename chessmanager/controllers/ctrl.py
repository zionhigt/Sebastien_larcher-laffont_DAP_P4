def compute_available_action(rules):
    def watcher(this):
        base_actions = rules(this)
        actions = filter(lambda x: not x[1], base_actions)
        return list(actions)
    return watcher


class Ctrl:
    def __init__(self, view):
        self.view = view

    @staticmethod
    def exit():
        return False

    def show_actions(self, actions_available, callbacks):
        user_choice = self.view.show(actions_available)
        try:
            if int(user_choice) in range(len(callbacks)):
                action_index = int(user_choice)
            else:
                raise IndexError

            callback_name = actions_available[action_index][2]
            callback_methode = callbacks[callback_name]
            callback_methode()

        except IndexError:
            self.view.print_error("Action impossible")
            self.show_actions(actions_available, callbacks)
        return
