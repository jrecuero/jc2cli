from prompt_toolkit import prompt
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.contrib.completers import WordCompleter
from pygments.style import Style
from pygments.token import Token
from pygments.styles.default import DefaultStyle


class DocumentStyle(Style):
    styles = {
        Token.Menu.Completions.Completion.Current: 'bg:#00aaaa #000000',
        Token.Menu.Completions.Completion: 'bg:#008888 #ffffff',
        Token.Menu.Completions.ProgressButton: 'bg:#003333',
        Token.Menu.Completions.ProfressBar: 'bg:#00aaaa',
    }
    styles.update(DefaultStyle.styles)


class Base(object):

    def __init__(self, namespace, commands, handler):
        self.namespace = namespace
        self.commands = commands
        self.handler  = handler

    @staticmethod
    def get_command_from_line(line):
        if len(line):
            lista = line.split()
            return lista[0], ' '.join(lista[1:])
        return None, None

    def run(self, *args, **kwargs):
        history = InMemoryHistory()
        completer = WordCompleter(self.commands.keys(), ignore_case=True)

        while True:
            line = prompt('> ',
                          history=history,
                          style=DocumentStyle,
                          completer=completer)
            print('You entered: {}'.format(line))
            command, params = Base.get_command_from_line(line)
            result = self.handler(command, line=params)
            if result is None:
                print('Unknown command: {}'.format(line))
            elif not result:
                break

        print('GoodBye!')


if __name__ == '__main__':
    base = Base()
    base.run()
