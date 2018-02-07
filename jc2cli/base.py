from prompt_toolkit import prompt
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.contrib.completers import WordCompleter
from pygments.style import Style
from pygments.token import Token
from pygments.styles.default import DefaultStyle


class DocumentStyle(Style):
    """DocumentStyle class is the style used to decorate the cli completer.
    """
    styles = {
        Token.Menu.Completions.Completion.Current: 'bg:#00aaaa #000000',
        Token.Menu.Completions.Completion: 'bg:#008888 #ffffff',
        Token.Menu.Completions.ProgressButton: 'bg:#003333',
        Token.Menu.Completions.ProfressBar: 'bg:#00aaaa',
    }
    styles.update(DefaultStyle.styles)


class Base(object):
    """Base class is the cli base class.
    """

    def __init__(self, namespace, commands, handler):
        """__init__ method is the Base class constructor.
        """
        self.namespace = namespace
        self.commands = commands
        self.handler  = handler

    @staticmethod
    def get_command_from_line(line):
        """get_command_from_line method retrieves the command label from a
        line entered by the user in the prompt_toolkit. It returns the rest
        of the line too.
        """
        if len(line):
            lista = line.split()
            return lista[0], ' '.join(lista[1:])
        return None, None

    def empty_line(self):
        """empty_line method handles an empty line entered by the user in the
        prompt_toolkit.
        """
        return True

    def handle_line(self, line):
        """handle_line method handles the line entered by the user in the
        prompt_toolkit.
        """
        if not line:
            if self.empty_line():
                return True
            else:
                return False

        print('You entered: {}'.format(line))
        command, params = Base.get_command_from_line(line)
        result = self.handler(command, line=params)
        if result is None:
            print('Unknown command: {}'.format(line))
        elif not result:
            return False
        return True

    def run(self, *args, **kwargs):
        """run method calls the prompt from the prompt_roolkit.
        """
        history = FileHistory('history.txt')
        completer = WordCompleter(self.commands.keys(), ignore_case=True)

        while True:
            line = prompt('> ',
                          history=history,
                          auto_suggest=AutoSuggestFromHistory(),
                          style=DocumentStyle,
                          completer=completer)
            if not self.handle_line(line):
                break

        print('GoodBye!')


if __name__ == '__main__':
    base = Base()
    base.run()
