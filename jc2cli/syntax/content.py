class Content:

    #staticmethod
    def get_label_from_content(content):
        if content is None:
            return '<None>'
        return content.label

    def __init__(self, label, help, completer):
        self.label = label
        self.help = help
        self.completer = comleter
        self..matchable = True

    def validate(self, val):
        return True

    def __str__(self):
        return self.label

    def is_command(self):
        return False

    def is_node(self):
        return False

    def is_argument(self):
        return False

    def is_joint(self):
        return False

    def get_str_type(self):
        return 'X'
