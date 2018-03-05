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
from prompt_toolkit.validation import Validator, ValidationError
from jc2cli.error_handler import CliException
from jc2cli.tree import Tree
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
MODULE = 'CLI.validator'
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
class CliValidator(Validator):

    def __init__(self, cli, **kwargs):
        self._cli = cli

    def validate(self, document):
        line_str = document.text.lstrip()
        line_as_list = line_str.split()
        if line_as_list:
            command_name = line_as_list[0]
            try:
                _, use_args  = Tree.setup_args_for_run_command(command_name, line=" ".join(line_as_list[1:]))
                if use_args is None:
                    logger.error('raise ValidationError: Unknown command {}'.format(command_name))
                    raise ValidationError(message='Unknown command: {}'.format(command_name))
            except CliException as ex:
                logger.error('raise ValidationError: {}'.format(ex.message))
                i = len(line_str)
                if ex.str_at_error:
                    i = line_str.index(ex.str_at_error)
                raise ValidationError(message=ex.message, cursor_position=i)
