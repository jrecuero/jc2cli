from jc2cli.syntax.cli.command import cli

if __name__ == '__main__':
    cli().import_commands('jc2cli/syntax/cli/commands')
    for c in cli().commands:
        kwargs = {}
        for a in c.argos:
            kwargs[a] = a
        print(c.dn)
        c.cb(**kwargs)
