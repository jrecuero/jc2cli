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
import time
from flask import Flask, request
from jc2cli.namespace import Handler
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
MODULE = 'SERVER.main'
logger = loggerator.getLoggerator(MODULE)
HOST_NAME = "0.0.0.0"
PORT_NUMBER = 5001


# -----------------------------------------------------------------------------
#       _                     _       __ _       _ _   _
#   ___| | __ _ ___ ___    __| | ___ / _(_)_ __ (_) |_(_) ___  _ __  ___
#  / __| |/ _` / __/ __|  / _` |/ _ \ |_| | '_ \| | __| |/ _ \| '_ \/ __|
# | (__| | (_| \__ \__ \ | (_| |  __/  _| | | | | | |_| | (_) | | | \__ \
#  \___|_|\__,_|___/___/  \__,_|\___|_| |_|_| |_|_|\__|_|\___/|_| |_|___/
#
# -----------------------------------------------------------------------------
#
class CliServer(Flask):

    def __init__(self, module, **kwargs):
        super(CliServer, self).__init__(module, **kwargs)
        self.namespace = None

    def set_new_namespace(self, namespace, module):
        self.module = module if module else namespace
        self.namespace = namespace
        try:
            __import__(self.module)
            h = Handler()
            self.ns_handler = h.get_ns_handler_after_create_and_switch(self.namespace)
            logger.display('Namespace initialized for {}...'.format(self.namespace))
            import sys
            logger.display('sys.modules {}...'.format(sys.modules))
            return True
        except ModuleNotFoundError:
            return False


# -----------------------------------------------------------------------------
#
#   ___ ___  _ __  ___| |_ __ _ _ __ | |_ ___
#  / __/ _ \| '_ \/ __| __/ _` | '_ \| __/ __|
# | (_| (_) | | | \__ \ || (_| | | | | |_\__ \
#  \___\___/|_| |_|___/\__\__,_|_| |_|\__|___/
#
# -----------------------------------------------------------------------------
#
app = CliServer(__name__)


# -----------------------------------------------------------------------------
#            _                     _   _
#  ___ _   _| |__  _ __ ___  _   _| |_(_)_ __   ___  ___
# / __| | | | '_ \| '__/ _ \| | | | __| | '_ \ / _ \/ __|
# \__ \ |_| | |_) | | | (_) | |_| | |_| | | | |  __/\__ \
# |___/\__,_|_.__/|_|  \___/ \__,_|\__|_|_| |_|\___||___/
#
# -----------------------------------------------------------------------------
#
def execute_command(command):
    result = ''
    if command:
        result += '<p>Run command: {}'.format(command)
        result += '<p>Result: {}'.format(str(app.ns_handler.cli.exec_user_input(command)))
    else:
        result += 'None'
    return str(result)


@app.before_first_request
def app_before_first_request():
    return True


@app.route('/cli/commands')
def app_commands():
    if app.namespace:
        result = ''
        for cmd in app.ns_handler.context.root.command_tree().keys():
            result += '<p>{}'.format(cmd)
        return result
    else:
        return 'namespace: None\n'


@app.route('/cli/ns')
def app_get_namespace():
    return app.namespace


@app.route('/cli/ns/<namespace>')
def app_set_namespace(namespace):
    module = request.args.get('module', None)
    if app.set_new_namespace(namespace, module):
        return app.namespace
    else:
        return 'Module {} not found\n'.format(namespace)


# @app.route('/cli')
# def app_cli():
#     if app.namespace:
#         command = request.args.get('command', None)
#         return execute_command(command)
#     else:
#         return 'namespace: None\n'


@app.route('/cli/command/<command>')
def app_cli_command(command):
    if app.namespace:
        return execute_command(command)
    else:
        return 'namespace: None\n'


# -----------------------------------------------------------------------------
#                  _
#  _ __ ___   __ _(_)_ __
# | '_ ` _ \ / _` | | '_ \
# | | | | | | (_| | | | | |
# |_| |_| |_|\__,_|_|_| |_|
#
# -----------------------------------------------------------------------------
#
if __name__ == '__main__':
    logger.display('{0} Server Starts - {1}:{2}'.format(time.asctime(), HOST_NAME, PORT_NUMBER))
    app.run(host=HOST_NAME, port=PORT_NUMBER)
    logger.display('\n{0} Server Stops - {1}:{2}'.format(time.asctime(), HOST_NAME, PORT_NUMBER))
