from jc2cli.namespace import Handler


class RunAsmCli(object):

    def __init__(self):
        module = 'examples.assembler.asm'
        namespace = module
        __import__(module)
        h = Handler()
        h.create_namespace(namespace)
        h.switch_and_run_cli_for_namespace(namespace)


if __name__ == '__main__':
    RunAsmCli()
