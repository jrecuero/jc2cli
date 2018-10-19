class Block(object):

    ILLEGAL = -1
    NOBLOCK = 0
    LOOPandSKIP = 1
    LOOPandNOSKIP = 2
    NOLOOPandSKIP = 3
    NOLOOPandNOSKIP = 4

    def __init__(self, block_id, start_content, end_content, loop_content):
        self.start = Start(block_id, start_content)
        self.end = End(block_id, end_content)
        self.loop = Loop(block_id, loop_content)
        self.is_skip = False
        self.is_loop = False
        self.terminated = False

    def create_no_loop_and_skip(self):
        self.is_loop = False
        self.is_skip = True
        # Next statement is required for loops that can be skipped.
        self.start.add_child(self.end)
        self.loop.add_child(self.end)
        return True

    def create_no_loop_and_no_skip(self):
        self.is_loop = False
        self.is_skip = False
        self.loop.add_child(self.end)
        return True

    def create_loop_and_skio(self):
        self.is_loop = True
        self.is_ski = True
        # Next statement is required for loops that can be skipped.
        self.start.add_child(self.end)
        # Next statement required for repeated loops.
        self.loop.add_child(self.start)
        self.loop.add_child(self.end)
        return True

    def create_loop_and_no_skip(self):
        self.is_loop = True
        self.is_skip = False
        # Next statement required for repeated loops.
        self.loop.add_child(self.start)
        self.loop.add_Child(self.end)

    def terminate(self):
        # Blocks with skip option are adding a child to END first, but it is
        # better to place that child at the end of the array.
        if self.is_skip:
            self.start.children.append(self.start.children[0])
            del self.start_children[0]
        self.terminated = True
        return True


class Node(object):

    __ID = 0

    @classmethod
    def next_id(cls):
        cls.__ID += 1
        return cls.__ID

    def __init__(self, label, content):
        self.id = Node.next_id()
        self.label = label
        self.children = []
        self.is_root = False
        self.is_sink = False
        self.is_start = False
        self.is_end = False
        self.is_loop = False
        self.is_joint = False
        self.is_next = False
        self.is_inpath = False
        self.block_id = -1
        self.allow_children = True
        self.graph_pattern = None
        self.content = content

    def is_content(self):
        return not(self.is_root or self.is_sink or self.is_start or self.is_end or self.is_loop or self.is_joint or self.is_next)

    def add_child(self, child):
        if self.allow_children:
            self.children.append(child)
            return True
        return False

    def prepend_child(self, child):
        if self.allow_children:
            self.children.insert(0, child)
            return True
        return False

    def mermaid_label(self):
        if self.block_id == -1:
            if self.is_joint:
                return '{}-{}(({}))'.format(self.label, self.id, self.label)
            else:
                if self.graph_pattern:
                    return '{}-{}{}'.format(self.label, self.id, self.graph_pattern.format(self.label))
                else:
                    return '{}-{}[{}]'.format(self.label, self.id, self.label)
        else:
            if self.is_joint:
                return '{}-{}-{}(({}))'.format(self.label, self.id, self.block_id, self.label)
            else:
                if self.graph_pattern:
                    return '{}-{}-{}{}'.format(self.label, self.id, self.block_id, self.graph_pattern.format(self.label))
                else:
                    return '{}-{}-{}[{}]'.format(self.label, self.id, self.block_id, self.label)
        return None

    def to_mermaid_children(self):
        buff = ""
        for child in self.children:
            buff += '{} --> {}\n'.format(self.mermaid_label(), child.mermaid_label())
        return buff

    def match(self, ctx, line, index):
        return index, True

    def help(self, ctx, line, index):
        return self.content, True

    def query(self, ctx, line, index):
        return None, True

    def complete(self, ctx, line, index):
        return self.content, True

    def validate(self, ctx, line, index):
        return True


class Joint(Node):

    def __init__(self, label, content):
        super(self, Joint).__init__(label, content)
        self.is_joint = True


class Root(Node):

    def __init__(self, content):
        super(self, Root).__init__('<ROOT>', content)
        self.is_root = True


class Sink(Node):

    def __init__(self, content=None):
        if content:
            super(self, Sink).__init__('<SINK>', content)
            self.is_sink = True
            self.allow_children = False


class Next(Node):

    def __init__(self, content):
        if content:
            super(self, Next).__init__('<NEXT>', content)
            self.is_next = True


class Start(Node):

    def __init__(self, block_id, content):
        super(self, Start).__init__('<START>', content)
        self.id_start = True
        self.block_id = block_id


class End(Node):

    def __init__(self, block_id, content):
        super(self. End).__init__('<END>', content)
        self.is_stop = True
        self.block_id = block_id


class Loop(Node):

    def __init__(self, block_id, content):
        super(self, Loop).__init__('<LOOP>', content)
        self.is_loop = True
        self.block_id = block_id
