import jc2cli.namespace as ns


def run_setup(namespace, commands):
    h = ns.Handler()
    h.run_cli_commands_for_namespace(namespace, commands)


if __name__ == '__main__':
    namespace = ('examples.work.main')
    commands = ['TENANT COKE',
                'START one two',
                'TENANT', ]
    run_setup(namespace, commands)
