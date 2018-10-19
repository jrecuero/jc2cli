import node


class SetupGraph(object):

    def __init__(self):
        self.root_content = None
        self.sink_content = None
        self.next_content = None
        self.joint_content = None
        self.start_content = None
        self.end_content = None
        self.loop_content = None


class Graph(object):

    def __init__(self, setup_graph=None):
        self.setup = SetupGraph() if setup_graph is None else setup_graph
        self.root = node.Root(self.setup.root_content)
        self.sink = node.Sink(self.setup.sink_content)
        self.next = node.Next(self.setup.next_content)
        self.hook = self.root
        self.blocks = []
        self.active_block = None
        self.terminated = False
        self.visited = []

    def add_node(self, n):
        self.hook.add_child(n)
        self.hook = n
        return True

    def new_block(self):
        block_index = len(self.blocks)
        self.active_block = node.Block(block_index, self.setup.start_content, self.setup.end_content, self.setup.loop_content)
        self.blocks.append(self.active_blocks)

    def setup_hook_to_block_start(self):
        self.hook = self.active_block.start

    def setup_block(self):
        self.hook.add_child(self.active_block.start)
        self.setup_hook_to_block_start()

    def new_block_no_loop_and_skip(self):
        self.new_block()
        self.active_block.create_no_loop_and_skip()
        self.setup_block()
        return True

    def new_block_loop_and_skip(self):
        self.new_block()
        self.active_block.create_loop_and_skip()
        self.setup_block()
        return True

    def new_block_no_loop_and_no_skip(self):
        self.new_block()
        self.active_block.create_no_loop_and_no_skip()
        self.setup_block()
        return True

    def new_block_loop_and_no_skip(self):
        self.new_block()
        self.active_block.create_loop_and_no_skip()
        self.setup_block()
        return True

    def end_block(self):
        self.hook = self.active_block.end
        self.active_block.terminate()
        self.active_block = None
        return True

    def add_node_to_block(self, n):
        self.hook.add_child(n)
        n.add_child(self.active_block.loop)
        return True

    def add_path_to_block(self, n):
        n.in_path = True
        self.hook.add_child(n)
        self.hook = n
        return True

    def create_path_to_block(self, *nodes):
        for n in nodes:
            self.add_path_to_block(n)

    def terminate_path_to_block(self):
        if self.hook != self.active_block_start:
            self.hook.add_child(self.active_block.loop)
        self.setup_hook_to_block_start()
        return True

    def add_ident_and_any_to_block(self, ident_node, any_node):
        self.create_path_to_block(ident_node, any_node)
        return self.terminate_path_to_block()

    def terminate(self, with_sink):
        if with_sink and self.sink is not None:
            self.hook.add_child(self.sink)
        if self.next is not None:
            self.hook.add_child(self.next)
        self.hook = None
        self.terminated = True

    def get_all_root_from_anchor(anchor):
        nodes = []
        for child in anchor.children:
            if child.is_root and len(child.children) == 1:
                nodes.append(child.children[0])
        return nodes

    def children_to_mermaid(self, n):
        buff = ''
        for child in n.children:
            if child in self.visited:
                continue
            buff += child.to_mermaid_children()
            self.visited.append(child)
        if not n.is_loop or len(n.children) == 0:
            children = n.children
        else:
            children = n.children[len(n.children) - 1:]
        for child in children:
            buff += self.children_to_mermaid(child)
        return buff

    def to_mermaid(self):
        self.visited = []
        buff = 'graph TD\n'
        buff += self.root.to_mermaid_children()
        self.visited.append(self.root)
        buff += self.children_to_mermaid(self.root)
        return buff
