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
MODULE = 'CLI.errors'
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
class CliException(Exception):
    """CliException class is the base class for any exception to be raised by the application.
    """

    def __init__(self, module, message, _type, exc_message=None, *args, **kwargs):
        """CliException class initialization method.

        Args:
            module (str) : Module raising the exception.
            message (str) : Message with the exception information.
            exc_message (str) : System exception that caused this app exception.
        """
        logger.error("[{}] {} {} {}".format(module,
                                            _type,
                                            '<{}>'.format(exc_message) if exc_message else '',
                                            message))
        super(CliException, self).__init__(message, *args, **kwargs)
        self.message = message
        self.type = _type


class CliError(CliException):
    """CliError class is the base class for any exception to be raised by the application.
    """

    def __init__(self, module, message, exc_message=None, *args, **kwargs):
        super(CliError, self).__init__(module, message, 'CliError', exc_message, *args, **kwargs)


class CliValidationError(CliException):
    """CliValidationError class is the base class for any exception to be raised for
    a type validation error.
    """

    def __init__(self, module, message, exc_message=None, *args, **kwargs):
        super(CliError, self).__init__(module, message, 'CliError', exc_message, *args, **kwargs)
