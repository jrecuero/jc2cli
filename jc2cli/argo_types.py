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
from jc2cli.error_handler import CliValidationError
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
        self.help_str = kwargs.get('help', '')
        self.complete_list = kwargs.get('complete_list', None)

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

    def get_help_str(self):
        """get_help_str method returns default string to be displayed as help.

        Returns:
            str : string with default help.
        """
        return self.help_str

    def help(self, text):
        """help method returns the help for the given argument.

        Args:
            text (str): last token in the line being entered.

        Returns:
            str : string with help to send to the display.
        """
        return self.get_help_str()

    def get_complete_list(self, document, text):
        """get_complete_list method gets a list with all possible options to
        be included in complete.

        Args:
            document (object) : document object with command line input data.
            text (str): last token in the line being entered.

        Returns:
            list : list with possible complete options
        """
        return self.complete_list

    def complete(self, document, text):
        """complete method returns the completion for the given argument.

        Args:
            document (object) : document object with command line input data.
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

    def get_the_value(self, value):
        """get_the_value method types any value as CliType.

        Args:
            value (object): value to be typed as CliType.

        Returns:
            str : String with the typed value.
        """
        return str(value)

    def get_value(self, value):
        """get_value method types any value as CliType.

        Args:
            value (object): value to be typed as CliType.

        Returns:
            str : String with the typed value.
        """
        if not self.validate(value):
            raise CliValidationError(MODULE, 'Validation Error: {}'.format(value))
        return self.get_the_value(value)

    def type(self):
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

    def get_help_str(self):
        """get_help_str method returns default string to be displayed as help.

        Returns:
            str : string with default help.
        """
        if self.help_str:
            return super(Prefix, self).get_help()
        else:
            return '-{0}'.format(self.label)

    def get_complete_list(self, document, text):
        """get_complete_list method gets a list with all possible options to
        be included in complete.

        Args:
            document (object) : document object with command line input data.
            text (str): last token in the line being entered.

        Returns:
            list : list with possible complete options
        """
        if self.complete_list:
            return super(Prefix, self).get_complete_list()
        else:
            return ['-{0}'.format(self.label), ]

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


# -----------------------------------------------------------------------------
#
class Int(CliType):
    """Int class is the class for any integer argument.
    """

    def get_help_str(self):
        """get_help_str method returns default string to be displayed as help.

        Returns:
            str : string with default help.
        """
        if self.help_str:
            return super(Int, self).get_help()
        else:
            return 'Enter a number'

    def validate(self, value):
        """validate method returns if value entered by the user is valid for
        argument type.
        """
        try:
            int(value)
            return True
        except ValueError:
            return False

    def get_the_value(self, value):
        """get_the_value method types any value as CliType.

        Args:
            value (object): value to be typed as integer.

        Returns:
            int : Integer with the typed value.
        """
        return int(value)

    def type(self):
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

    def get_help_str(self):
        """get_help_str method returns default string to be displayed as help.

        Returns:
            str : string with default help.
        """
        if self.help_str:
            return super(Str, self).get_help()
        else:
            return 'Enter a string'


# -----------------------------------------------------------------------------
#
class Constant(Str):
    """Constant class is the class for any string constant argument.
    """

    def get_help_str(self):
        """get_help_str method returns default string to be displayed as help.

        Returns:
            str : string with default help.
        """
        if self.help_str:
            return super(Constant, self).get_help()
        else:
            return 'Enter "{}"'.format(self.argo.name)

    def get_complete_list(self, document, text):
        """get_complete_list method gets a list with all possible options to
        be included in complete.

        Args:
            document (object) : document object with command line input data.
            text (str): last token in the line being entered.

        Returns:
            list : list with possible complete options
        """
        if self.complete_list:
            return super(Constant, self).get_complete_list()
        else:
            return [self.argo.name, ]


# -----------------------------------------------------------------------------
#
class Enum(Str):
    """Enum class is the class for any enumeration argument.
    """

    def __init__(self, values, **kwargs):
        super(Enum, self).__init__(**kwargs)
        self.values = values

    def get_help_str(self):
        """get_help_str method returns default string to be displayed as help.

        Returns:
            str : string with default help.
        """
        if self.help_str:
            return super(Enum, self).get_help()
        else:
            return '{}'.format(", ".join(self.values))

    def get_complete_list(self, document, text):
        """get_complete_list method gets a list with all possible options to
        be included in complete.

        Args:
            document (object) : document object with command line input data.
            text (str): last token in the line being entered.

        Returns:
            list : list with possible complete options
        """
        if self.complete_list:
            return super(Enum, self).get_complete_list()
        else:
            return self.values


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
    """Line class is the class for any full line argument.

    A full line argument is a argument that will receive all data entered by
    the user.
    """

    def is_lined(self):
        """is_lined method returns if the argument type process the whole line
        entered by the user.
        """
        return True


# -----------------------------------------------------------------------------
#
class End(Str):
    """End class is the class for the End node, which marks the end for a
    command syntax.
    """

    def __init__(self, **kwargs):
        super(End, self).__init__(**kwargs)
        self.help_str = 'Type <CR>'
