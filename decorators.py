from functools import wraps
from tree import Tree


def command(syntax, namespace=None):

    def command_wrapper(f):

        @wraps(f)
        def _wrapper(*args, **kwargs):
            return f(*args, **kwargs)

        print('called for {0}'.format(syntax))
        node = Tree.fnode(f, _wrapper)
        node.command.syntax = syntax
        if namespace:
            Tree().rename_node(node.name, '{0}.{1}'.format(namespace, f.__qualname__))
        return _wrapper
    return command_wrapper


def argo(argo_name, argo_type, argo_default=None):

    def argo_wrapper(f):

        @wraps(f)
        def _wrapper(*args, **kwargs):
            return f(*args, **kwargs)

        print('called for {0}'.format(argo_name))
        node = Tree.fnode(f, _wrapper)
        node.command.add_param(argo_name, (argo_name, argo_type, argo_default))
        return _wrapper
    return argo_wrapper
