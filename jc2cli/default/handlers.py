from jc2cli.tree import Tree


def handler(command, *args, **kwargs):
    return Tree.run(command, *args, **kwargs)


def handler_instance(command, instance, *args, **kwargs):
    return Tree.run_instance(command, instance, *args, **kwargs)
