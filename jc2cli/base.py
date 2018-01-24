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

    def __init__(self):
        pass

    def run(self):
        history = InMemoryHistory()
        completer = WordCompleter(['hello', 'bye', 'open', 'close',
                                   'card'], ignore_case=True)

        while True:
            text = prompt('> ',
                          history=history,
                          style=DocumentStyle,
                          completer=completer)
            print('You entered: {}'.format(text))
            if text == 'bye':
                break

        print('GoodBye!')


if __name__ == '__main__':
    base = Base()
    base.run()
