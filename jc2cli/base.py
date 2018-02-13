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
import json
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
        self.toolbar_str = ''
        self.prompt_str = "> "
        self.rprompt_str = ''
        self.__recording = False
        self.__record_data = []

    @property
    def commands(self):
        return self.ns_handler.commands

    @property
    def handler(self):
        return self.ns_handler.handler

    @property
    def context(self):
        return self.ns_handler.context

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

    def start_recording(self):
        """Starts recording commands input in the command line.

        Returns:
            None
        """
        self.__recording = True

    def stop_recording(self):
        """Stops recording commands input in the command line.

        Returns:
            None
        """
        self.__recording = False
        if self.__record_data:
            del self.__record_data[-1]

    def clear_recording(self, from_record=None, to_record=None):
        """Clears the range of records recorded from the given range.

        Args:
            from_record (int) : First record to clear. Set to 0 if None.

            to_record (int): Last record to clear. Set to last if None
        """
        if from_record is None and to_record is None:
            self.__record_data.clear()
        elif from_record is None and to_record is not None:
            if to_record < len(self.__record_data):
                del self.__record_data[:to_record + 1]
        elif from_record is not None and to_record is None:
            if 0 <= from_record <= len(self.__record_data):
                del self.__record_data[from_record:]
        elif (0 <= from_record <= len(self.__record_data)) and\
                to_record < len(self.__record_data) and\
                from_record <= to_record:
                del self.__record_data[from_record:to_record + 1]
        else:
            pass

    def select_recording(self, from_record=None, to_record=None):
        """Selects the range of records recorded from the given range.

        Args:
            from_record (int) : First record to select. Set to 0 if None.

            to_record (int): Last record to select. Set to last if None

        Returns:
            list : List of selected records.
        """
        if from_record is None and to_record is None:
            return self.__record_data
        elif from_record is None and to_record is not None:
            if to_record < len(self.__record_data):
                return self.__record_data[:to_record + 1]
        elif from_record is not None and to_record is None:
            if 0 <= from_record <= len(self.__record_data):
                return self.__record_data[from_record:]
        elif (0 <= from_record <= len(self.__record_data)) and\
                to_record < len(self.__record_data) and\
                from_record < to_record:
                return self.__record_data[from_record:to_record + 1]
        else:
            return []

    def display_recording(self, from_record=None, to_record=None):
        """Displays the range of records recorded from the given range.

        Args:
            from_record (int) : First record to display. Set to 0 if None.

            to_record (int): Last record to display. Set to last if None

        Returns:
            None
        """
        records = self.select_recording(from_record, to_record)
        for i, record in enumerate(records):
            logger.display('{0}: {1}'.format(i, record))

    def save_recording(self, filename, from_record=None, to_record=None):
        """
        """
        records = self.select_recording(from_record, to_record)
        to_save = []
        for record in records:
            to_save.append({'command': record})
        if to_save:
            with open(filename, 'w') as f:
                json.dump(to_save, f)

    def record_command(self, user_input):
        """Saves in a JSON file the range of records recorded from the given
        range.

        Args:
            from_record (int) : First record to save. Set to 0 if None.

            to_record (int): Last record to save. Set to last if None

        Returns:
            None
        """
        if self.__recording:
            self.__record_data.append(user_input)

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
        self.record_command(line)
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
