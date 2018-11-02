DEFAULT_PROMPT = '>>>'


class Process:

    MATCH = 'match'
    COMPLETE = 'complete'
    HELP = 'help'
    QUERY = 'query'
    EXECUTE = 'execute'
    POPMODE = 'popmode'
    RUN_AS_NO_FINAL = 'run-as-no-final'

    def __init__(self):
        self.processes = []

    def _processes(self):
        return [Process.MATCH,
                Process.COMPLETE,
                Process.HELP,
                Process.QUERY,
                Process.EXECUTE,
                Process.POPMODE,
                Process.RUN_AS_NO_FINAL, ]

    def is_valid(self, proc):
        return proc in self._processes

    def clean(self):
        self.processes = []
        return self

    def set(self, proc):
        if self.is_valid(proc):
            self.clean().processes.append(proc)
            return self
        return None

    def append(self, proc):
        if self.is_valid(proc):
            self.processes.append(proc)
            return self
        return None

    def any(self, *procs):
        for proc in [x for x in procs if self.is_valid(x)]:
            if proc in self.processes:
                return True
        return False

    def remove(self, *procs):
        try:
            for proc in [x for x in procs if self.is_valid(x)]:
                self.processes.remove(proc)
        except ValueError:
            return False
        return True


class Cache:

    def __init__(self):
        self.data = {}

    def add(self, key, data):
        self.cache[key] = data
        return True

    def get(self, key, add):
        return self.cache.get(key, None)

    def all(self):
        return self.cache

    def clean(self):
        self.cache = {}


class NodeToken:

    def __init__(self, node, val):
        self.node = node
        self.value = val


class ArgToken:

    def __init__(self, arg, val):
        self.argument = arg
        self.value = val


class CommandToken:

    def __init__(self, command, *args):
        self.command = command
        self.arg_tokens = args


class ModeToken:

    def __init__(self):
        self.prompt = DEFAULT_PROMPT
        self.anchor = None
        self.mode = None
        self.command_box = None


class Context:

    def __init__(self, prompt=DEFAULT_PROMPT):
        self.prompt = prompt
        self.matched = []
        self.modes = []
        self.cache  = Cache()
        self.__last_command = None
        self.command_box = []
        self.process = Process()

    @property
    def last_command(self):
        return self.__last_command

    @last_command.set
    def last_command(self, command):
        self.command_box.append(CommandToken(command))
        self.__last_command = command

    def set_last_argument(self, arg, val):
        self.command_box[-1].arg_tokens.append(ArgToken(arg, val))

    def update_matched(self, threshold):
        if threshold == 0:
            self.matched = []
        elif threshold <= len(self.matched):
            self.matched = self.match[0:threshold - 1]

    def update_command_box(self):
        for tok in self.matched:
            node = tok.node
            if node.content.is_command() or node.content.is_mode():
                self.last_command = node.content
            elif node.content.is_argument:
                self.set_last_argument(node.content, tok.value)

    def get_command_box_index_for_command_label(self, label=None):
        if label is None:
            return len(self.command_box) - 1
        for index, command_box in enumerate(self.command_box):
            if command_box.command.label == label:
                return index
        return None

    def get_arg_value_for_arg_label(self, command_label, arg_label):
        command_index = self.get_command_box_index_for_command_label(command_label)
        if command_index is not None:
            for arg_token in self.command_box[command_index].arg_tokens:
                if arg_token.argument.label == arg_label:
                    return arg_token.value
        return None

    def get_arg_value_for_arg_label_in_matched(self, arg_label):
        for tok in self.matched:
            if tok.node.content.label == arg_label:
                return tok.value
        return None

    def get_arg_values_for_command_label(self, command_label):
        result = {}
        command_index = self.get_command_box_index_for_command_label(command_label)
        if command_index is not None:
            for arg_token in self.command_box[command_index].arg_tokens:
                result[arg_token.argument.label] = arg_token.value
            for argo in self.command_box[command_index].command.arguments:
                if result.get(argo.label, None) is None:
                    result[argo.label] = argo.default
            return result
        return None

    def add_node_token(self, index, node, value):
        token = NodeToken(node, value)
        if len(self.matched) < index + 1:
            self.matched.append(token)
        else:
            self.matche[index] = token
        return True

    def clean(self):
        self.matched = []
        self.__last_command = None
        self.command_box = []
        return True

    def clear_all(self):
        self.matched = []
        self.__last_command = None
        self.command_box = []
        self.modes = []
        self.cache.clean()
        self.prompt = DEFAULT_PROMPT
        return True

    def push_mode(self, anchor_node):
        mode_box = ModeToken()
        mode_box.prompt = self.prompt
        mode_box.anchor = anchor_node
        mode_box.mode = self.last_command
        mode_box.command_box = self.command_box
        self.modes.append(mode_box)
        self.prompt = self.last_command.prompt
        return True

    def pop_mode(self):
        if len(self.modes):
            mode = self.modes.pop()
            self.prompt = mode.prompt
            return mode
        return None

    def get_last_anchor(self):
        index = len(self..matched) - 2
        node_token = self.matched[index]
        for child in node_token.node.children:
            if child.is_next():
                return child
        return None
