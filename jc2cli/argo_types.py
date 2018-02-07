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


# -----------------------------------------------------------------------------
#
#   ___ ___  _ __  ___| |_ __ _ _ __ | |_ ___
#  / __/ _ \| '_ \/ __| __/ _` | '_ \| __/ __|
# | (_| (_) | | | \__ \ || (_| | | | | |_\__ \
#  \___\___/|_| |_|___/\__\__,_|_| |_|\__|___/
#
# -----------------------------------------------------------------------------
#
MODULE = 'CLI.argotypes'
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
class CliType(object):
    """CliType class is the base class for any command argument.
    """

    def __init__(self, **kwargs):
        """CliType class initialization method.

        Keyword Args:
            inpos (boolean) : argument position.
            cte (boolean) : constant argument.
            seq (boolean): argument is a sequence.
            label (str) : label to be used by the type.
        """
        self.argo = kwargs.get('argo', None)
        self.label = kwargs.get('label', None)
        self.help_str = kwargs.get('help', None)

    def is_lined(self):
        """is_lined method returns if the argument type process the whole line
        entered by the user.
        """
        return False

    def store(self, value, matched=False):
        """store method stores a value in the argument for the type.

        Args:
            value (object) : Value to store in the argument.

            matched (bool) : True is argument was already matched and found\
                    in the command line entry.

        Returns:
            None
        """
        if matched:
            if type(self.argo.value) == list:
                self.argo.value.append(value)
            else:
                self.argo.value = [self.argo.value, value]
        else:
            self.argo.value = value

    def _help_str(self):
        """_help_str method returns default string to be displayed as help.

        Returns:
            str : string with default help.
        """
        return ''

    def help(self, text):
        """help method returns the help for the given argument.

        Args:
            text (str): last token in the line being entered.

        Returns:
            str : string with help to send to the display.
        """
        return self.help_str if self.help_str else self._help_str()

    def get_complete_list(self, document, text):
        """get_complete_list method gets a list with all possible options to
        be included in complete.

        Args:
            document (object) : document object with all command line
            input data.

            text (str): last token in the line being entered.

        Returns:
            list : list with possible complete options
        """
        return None

    def complete(self, document, text):
        """complete method returns the completion for the given argument.

        Args:
            document (object) : document object with all command line
            input data.

            text (str): last token in the line being entered.

        Returns:
            str : string with completion to send to the display.
        """
        options = self.get_complete_list(document, text)
        if options:
            if text in [' ', '']:
                return [x for x in options]
            else:
                return [x for x in options if x.startswith(text)]
        return None

    def validate(self, value):
        """validate method returns if value entered by the user is valid for
        argument type.

        Validation should be called before value is stored in Argument
        instance.
        """
        return True

    @staticmethod
    def get_value(value):
        """get_value method types any value as Tenant.

        Args:
            value (object): value to be typed as Tenant.

        Returns:
            str : String with the typed value.
        """
        return str(value)

    @staticmethod
    def type():
        """type method returns the type used for the given argument.

        Returns:
            type : argument type.
        """
        return str


# -----------------------------------------------------------------------------
#
class Prefix(CliType):
    """Prefix class derived from CliType and is the type to be used for prefix
    nodes.
    """

    def store(self, value, matched=False):
        """store method stores a value in the argument for the type.

        Args:
            value (object) : Value to store in the argument.

            matched (bool) : True is argument was already matched and found\
                    in the command line entry.

        Returns:
            None
        """
        pass

    def _help_str(self):
        """_help_str method returns default string to be displayed as help.

        Returns:
            str : string with default help.
        """
        return '-{0}'.format(self.label)

    def help(self, text):
        """help method returns the help for the given argument.

        Args:
            text (str): last token in the line being entered.

        Returns:
            str : string with help to send to the display.
        """
        return self._help_str()

    def complete(self, document, text):
        """complete method returns the completion for the given argument.

        Args:
            document (object) : document object with all command line
            input data.

            text (str): last token in the line being entered.

        Returns:
            str : string with completion to send to the display.
        """
        return ['-{0}'.format(self.label), ]

    @staticmethod
    def get_value(value):
        """get_value method types any value as Tenant.

        Args:
            value (object): value to be typed as Tenant.

        Returns:
            str : Sring with the typed value.
        """
        return str(value)

    @staticmethod
    def type():
        """type method returns the type used for the given argument.

        Returns:
            type : argument type.
        """
        return str


# -----------------------------------------------------------------------------
#
class Int(CliType):
    """Int class is the class for any integer argument.
    """

    def _help_str(self):
        """_help_str method returns default string to be displayed as help.

        Returns:
            str : string with default help.
        """
        return 'Enter a number'

    def validate(self, value):
        """validate method returns if value entered by the user is valid for
        argument type.
        """
        return isinstance(value, int)

    @staticmethod
    def get_value(value):
        """get_value method types any value as Tenant.

        Args:
            value (object): value to be typed as integer.

        Returns:
            int : Integer with the typed value.
        """
        return int(value)

    @staticmethod
    def type():
        """type method returns the type used for the given argument.

        Returns:
            type : argument type.
        """
        return int


# -----------------------------------------------------------------------------
#
class Str(CliType):
    """Str class is the class for any string argument.
    """

    def _help_str(self):
        """_help_str method returns default string to be displayed as help.

        Returns:
            str : string with default help.
        """
        return 'Enter a string'


# -----------------------------------------------------------------------------
#
class Dicta(Str):
    """Dicta class is the class for any dictionary argument.
    """

    def store(self, value, matched=False):
        """store method stores a value in the argument for the type.

        Args:
            value (object) : Value to store in the argument.

            matched (bool) : True is argument was already matched and found\
                    in the command line entry.

        Returns:
            None
        """
        key, val = value.split('=')
        if matched:
            self.argo.value.update({key: val})
        else:
            self.argo.value = {key: val}

    def validate(self, value):
        """validate method returns if value entered by the user is valid for
        argument type.
        """
        return '=' in value


# -----------------------------------------------------------------------------
#
class Line(CliType):

    def is_lined(self):
        """is_lined method returns if the argument type process the whole line
        entered by the user.
        """
        return True
