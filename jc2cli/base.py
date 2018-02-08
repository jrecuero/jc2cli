__docformat__ = 'restructuredtext en'

# -----------------------------------------------------------------------------
#  _                            _
# (_)_ __ ___  _ __   ___  _ __| |_ ___
# | | '_ ` _ \| '_ \ / _ \| '__| __/ __|
# | | | | | | | |_) | (_) | |  | |_\__ \
# |_|_| |_| |_| .__/ \___/|_|   \__|___/
#             |_|
# -----------------------------------------------------------------------------
#
import jc2cli.tools.loggerator as loggerator
from jc2cli.completer import CliCompleter
from prompt_toolkit import prompt
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from pygments.style import Style
from pygments.token import Token
from pygments.styles.default import DefaultStyle


# -----------------------------------------------------------------------------
#
#   ___ ___  _ __  ___| |_ __ _ _ __ | |_ ___
#  / __/ _ \| '_ \/ __| __/ _` | '_ \| __/ __|
# | (_| (_) | | | \__ \ || (_| | | | | |_\__ \
#  \___\___/|_| |_|___/\__\__,_|_| |_|\__|___/
#
# -----------------------------------------------------------------------------
#
MODULE = 'CLI.base'
logger = loggerator.getLoggerator(MODULE)


# -----------------------------------------------------------------------------
#       _                     _       __ _       _ _   _
#   ___| | __ _ ___ ___    __| | ___ / _(_)_ __ (_) |_(_) ___  _ __  ___
#  / __| |/ _` / __/ __|  / _` |/ _ \ |_| | '_ \| | __| |/ _ \| '_ \/ __|
# | (__| | (_| \__ \__ \ | (_| |  __/  _| | | | | | |_| | (_) | | | \__ \
#  \___|_|\__,_|___/___/  \__,_|\___|_| |_|_| |_|_|\__|_|\___/|_| |_|___/
#
# -----------------------------------------------------------------------------
#
class DocumentStyle(Style):
    """DocumentStyle class is the style used to decorate the cli completer.
    """
    styles = {
        Token.Menu.Completions.Completion.Current: 'bg:#00aaaa #000000',
        Token.Menu.Completions.Completion: 'bg:#008888 #ffffff',
        Token.Menu.Completions.ProgressButton: 'bg:#003333',
        Token.Menu.Completions.ProfressBar: 'bg:#00aaaa',
        Token.Toolbar: '#ffffff italic bg:#007777',
        Token.RPrompt: 'bg:#ff0066 #ffffff',
    }
    styles.update(DefaultStyle.styles)


class Base(object):
    """Base class is the cli base class.
    """

    def __init__(self, ns_handler):
        """__init__ method is the Base class constructor.
        """
        self.ns_handler = ns_handler
        self.commands = self.ns_handler.commands
        self.handler  = self.ns_handler.handler
        self.context = self.ns_handler.context
        self.toolbar_str = ''
        self.prompt_str = "> "
        self.rprompt_str = ''

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

    def get_bottom_toolbar_tokens(self, cli):
        """Method that provides data and format to be displayed in the ToolBar.

        Args:
            cli (:class:`CommandLineInterface`) : CommandLineInterface instance.

        Returns:
            :any:`list` : list with data to be displayed in the ToolBar.
        """
        return [(Token.Toolbar, '{}'.format(self.toolbar_str)), ]

    def get_prompt_tokens(self, cli):
        """Returns tokens for command line prompt.

        Args:
            cli (:class:`CommandLineInterface`) : CommandLineInterface instance.

        Returns:
            :any:`list` : list with data to be displayed in the prompt.
        """
        return [(Token.Prompt, '{}'.format(self.prompt_str)), ]

    def get_rprompt_tokens(self, cli):
        """Returns tokens for command line right prompt.

        Args:
            cli (:class:`CommandLineInterface`) : CommandLineInterface instance.

        Returns:
            :any:`list` : list with data to be displayed in the right prompt..
        """
        return [(Token.RPrompt, '{}'.format(self.rprompt_str)), ]

    def empty_line(self):
        """empty_line method handles an empty line entered by the user in the
        prompt_toolkit.
        """
        return True

    def handle_line(self, line):
        """handle_line method handles the line entered by the user in the
        prompt_toolkit.
        """
        if not line.strip():
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

    def run_prompt(self, **kwargs):
        """Execute the command line.

        Args:
            prompt (:any:`str` or :any:`function`) : string or callback with prompt value

            toolbar (:any:`str` or :any:`function`) : string or callback with toolbar value.

            rprompt (:any:`str` or :any:`function`) : string or callback with right prompt value.

        Returns:
            str : String with the input entered by the user.
        """
        history = FileHistory('history.txt')
        completer = CliCompleter(self)

        toolbar = kwargs.get('toolbar', 'Enter a valid command')
        self.toolbar_str = toolbar if isinstance(toolbar, str) else toolbar()

        _prompt = kwargs.get('prompt', self.prompt_str)
        self.prompt_str = _prompt if isinstance(_prompt, str) else _prompt()

        rprompt = kwargs.get('rprompt', None)
        if rprompt is not None:
            self.rprompt_str = rprompt if isinstance(rprompt, str) else rprompt()

        user_input = prompt(history=history,
                            auto_suggest=AutoSuggestFromHistory(),
                            style=DocumentStyle,
                            completer=completer,
                            get_bottom_toolbar_tokens=self.get_bottom_toolbar_tokens,
                            get_prompt_tokens=self.get_prompt_tokens,
                            get_rprompt_tokens=self.get_rprompt_tokens,
                            refresh_interval=1)
        # completer.reset()
        return user_input

    def cmd_loop(self, *args, **kwargs):
        """cmd_loop is called to wait for any user input.

        Keyword Args:
            prompt (:any:`str` or :any:`function`) : string or callback with prompt value

            toolbar (:class:`str` or :any:`function`) : string or callback with toolbar value.

            rprompt (:any:`str` or :any:`function`) : string or callback with right prompt value.

            echo (bool) : True is command should be echoed.

            precmd (bool) : True if precmd shoud be called.

            postcmd (bool) : True if postcmd should be called.

        Returns:
            None
        """
        while True:
            user_input = self.run_prompt(*args, **kwargs)
            if not self.handle_line(user_input):
                break

    def run(self, *args, **kwargs):
        """run executes command line interface for the given cli class.

        Keyword Args:
            prompt (:any:`str` or :any:`function`) : string or callback with prompt value

            toolbar (:class:`str` or :any:`function`) : string or callback with toolbar value.

            rprompt (:any:`str` or :any:`function`) : string or callback with right prompt value.

            echo (bool) : True is command should be echoed.

            precmd (bool) : True if precmd shoud be called.

            postcmd (bool) : True if postcmd should be called.

        Returns:
            None
        """
        try:
            self.cmd_loop(*args, **kwargs)
            logger.display('GoodBye!')
        except KeyboardInterrupt:
            logger.display("")
            pass


if __name__ == '__main__':
    base = Base()
    base.run()
