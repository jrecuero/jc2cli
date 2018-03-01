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
from jc2cli.argo_types import CliType
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
MODULE = 'BUILTIN.argos'
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
            return super(Prefix, self).get_help_str()
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
            return super(Int, self).get_help_str()
        else:
            return 'Enter a number'

    def validate(self, value):
        """validate method returns if value entered by the user is valid for
        argument type.
        """
        try:
            int(value)
            return True, ''
        except ValueError:
            return False, 'Value is not an integer'

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
            return super(Str, self).get_help_str()
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
            return super(Constant, self).get_help_str()
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

    def validate(self, value):
        """validate method returns if value entered by the user is valid for
        argument type.

        Validation should be called before value is stored in Argument
        instance.
        """
        return value == self.argo.name, 'Value does not match constant'


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
            return super(Enum, self).get_help_str()
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

    def validate(self, value):
        """validate method returns if value entered by the user is valid for
        argument type.

        Validation should be called before value is stored in Argument
        instance.
        """
        return value in self.values, 'Value is not in enumeration'


# -----------------------------------------------------------------------------
#
class Range(Str):
    """Range class is the class for any enumeration argument.
    """

    def __init__(self, values, **kwargs):
        super(Range, self).__init__(**kwargs)
        self.values = values

    def get_help_str(self):
        """get_help_str method returns default string to be displayed as help.

        Returns:
            str : string with default help.
        """
        if self.help_str:
            return super(Range, self).get_help_str()
        else:
            result = ''
            for _range in self.values:
                if len(_range) == 2:
                    result += '{} - {}, '.format(_range[0], _range[1])
                else:
                    result += '{}'.format(', '.join([str(x) for x in _range]))
            return result

    def validate(self, value):
        """validate method returns if value entered by the user is valid for
        argument type.

        Validation should be called before value is stored in Argument
        instance.
        """
        try:
            value = int(value)
        except ValueError:
            return False, 'Value is not an integer'
        for _range in self.values:
            if len(_range) != 2:
                if value in _range:
                    return True, ''
            elif _range[0] <= value <= _range[1]:
                return True, ''
        return False, 'Value is not in range'


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
        return '=' in value, 'Value does not contain "="'


# -----------------------------------------------------------------------------
#
class Lista(Str):
    """Lista class is the class for list arguments.
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
        self.argo.value = value.split(',')


# -----------------------------------------------------------------------------
#
class Vector2D(Str):
    """Vector2D class is the class for 2D-vector arguments.
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
        value_list = value.split(',')
        if len(value_list) == 1:
            value += ',0'
        self.argo.value = [int(x) for x in value.split(',')]

    def validate(self, value):
        """validate method returns if value entered by the user is valid for
        argument type.
        """
        value_list = value.split(',')
        if len(value_list) > 2:
            return False, 'Too many values for a Vector2D'
        try:
            for x in value_list:
                int(x)
            return True, ''
        except ValueError:
            return False, 'Value "{}"is not an integer'.format(x)


# -----------------------------------------------------------------------------
#
class Vector3D(Str):
    """Vector3D class is the class for 3D-vector arguments.
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
        value_list = value.split(',')
        if len(value_list) == 1:
            value += ',0,0'
        elif len(value_list) == 2:
            value += ',0'
        self.argo.value = [int(x) for x in value.split(',')]

    def validate(self, value):
        """validate method returns if value entered by the user is valid for
        argument type.
        """
        value_list = value.split(',')
        if len(value_list) > 3:
            return False, 'Too many values for a Vector2D'
        try:
            for x in value_list:
                int(x)
            return True, ''
        except ValueError:
            return False, 'Value "{}"is not an integer'.format(x)


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
