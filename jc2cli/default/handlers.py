from jc2cli.tree import Tree


def handler(command_name, *args, **kwargs):
    return Tree.run(command_name, *args, **kwargs)


def handler_instance(command_name, instance, *args, **kwargs):
    return Tree.run_instance(command_name, instance, *args, **kwargs)


def handler_mode(command_name, *args, **kwargs):
    node = Tree.get_node(command_name)
    result = Tree.run(command_name, *args, **kwargs)
    if node.is_mode() and result:
        Tree.switch_to(node.command.namespace)
    return result
