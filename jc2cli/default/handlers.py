from jc2cli.tree import Tree


def handler(command_name, *args, **kwargs):
    return Tree.run(command_name, *args, **kwargs)


def handler_instance(command_name, instance, *args, **kwargs):
    return Tree.run_instance(command_name, instance, *args, **kwargs)


def handler_mode(command_name, *args, **kwargs):
    node = Tree.get_node(command_name)
    if node.is_mode():
        if Tree.run(command_name, *args, **kwargs):
            # Do some mode staff here
            return True
        else:
            return None
    else:
        return Tree.run(command_name, *args, **kwargs)
