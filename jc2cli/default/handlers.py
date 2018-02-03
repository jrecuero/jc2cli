from jc2cli.tree import Tree


def handler(command_name, *args, **kwargs):
    return Tree.run(command_name, *args, **kwargs)


def handler_instance(command_name, instance, *args, **kwargs):
    return Tree.run_instance(command_name, instance, *args, **kwargs)


def handler_none(command_name, *args, **kwargs):
    return Tree.run_instance(command_name, None, *args, **kwargs)


def handler_mode(cli_handler, command_name, *args, **kwargs):
    node = Tree.get_node(command_name)
    result = Tree.run(command_name, *args, **kwargs)
    active_namespace = Tree.active_namespace()
    if node.is_mode() and result:
        cli_handler.switch_and_run(*args, **kwargs)
        Tree.switch_to(active_namespace)
    return result
