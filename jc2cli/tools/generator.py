__docformat__ = 'restructuredtext en'

"""generator module contains all information required to generate CLI commands
from JSON format.

Commands are entered in a defined JSON format, and using generator module they
wil be transformed in CLI commands that can be used by any CLI application.

JSON format:
    [
        {
            "name": <command-name>,
            "syntax": <command-syntax>,
            "namespace": <command-namespace>,
            "internal": true/false,
            "help": <command-help>,
            "pyname": <command-cb-name>,
            "arguments": {
                "name": <argument-name>,
                "default": <argument-default-value>,
                "help": <argument-help>,
                "pyname": <argument-python-name>,
                "type": {
                    "name": <type-name>,
                    "module": "builtin"
                }
            }
        },
    ]
"""

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
from jc2cli.tree import Tree
from jc2cli.arguments import Argument


# -----------------------------------------------------------------------------
#
#   ___ ___  _ __  ___| |_ __ _ _ __ | |_ ___
#  / __/ _ \| '_ \/ __| __/ _` | '_ \| __/ __|
# | (_| (_) | | | \__ \ || (_| | | | | |_\__ \
#  \___\___/|_| |_|___/\__\__,_|_| |_|\__|___/
#
# -----------------------------------------------------------------------------
#
MODULE = 'TOOLS.generator'
logger = loggerator.getLoggerator(MODULE)
COMMAND_PATTERN = '@command({}, {})\n'
ICOMMAND_PATTERN = '@icommand({}, {})\n'
MODE_PATTERN = '@mode({}, {})\n'
IMODE_PATTERN = '@imode({}, {})\n'
HELP_PATTERN = '@help({})\n'
ARGO_PATTERN = '@argo({}, {}, {})\n'
COMMAND_CB_PATTERN = 'def {}({}):\n    {}({})'


# -----------------------------------------------------------------------------
#            _                     _   _
#  ___ _   _| |__  _ __ ___  _   _| |_(_)_ __   ___  ___
# / __| | | | '_ \| '__/ _ \| | | | __| | '_ \ / _ \/ __|
# \__ \ |_| | |_) | | | (_) | |_| | |_| | | | |  __/\__ \
# |___/\__,_|_.__/|_|  \___/ \__,_|\__|_|_| |_|\___||___/
#
# -----------------------------------------------------------------------------
#


# -----------------------------------------------------------------------------
#       _                     _       __ _       _ _   _
#   ___| | __ _ ___ ___    __| | ___ / _(_)_ __ (_) |_(_) ___  _ __  ___
#  / __| |/ _` / __/ __|  / _` |/ _ \ |_| | '_ \| | __| |/ _ \| '_ \/ __|
# | (__| | (_| \__ \__ \ | (_| |  __/  _| | | | | | |_| | (_) | | | \__ \
#  \___|_|\__,_|___/___/  \__,_|\___|_| |_|_| |_|_|\__|_|\___/|_| |_|___/
#
# -----------------------------------------------------------------------------
#
class CliGenerator(object):

    def __init__(self):
        pass

    def load_commands_from_json(self, json_data):
        """load_commands_from_json loads CLI commands from a JSON variable.

        Args:
            json_data (json) : Variable with JSON data.

        Returns:
            None
        """
        self.commands = json.loads(json_data)
        return self.commands

    def load_commands_from_file(self, filename):
        """load_commands_from_file loads a file with the given filename with CLI
        commands in JSON format.

        Args:
            filename (str) : String with the filename that contains json data.

        Returns:
            None
        """
        try:
            with open(filename, 'r') as f:
                data = json.load(f)
            self.load_commands_from_json(json.dumps(data))
        except OSError:
            logger.error('File not found {}'.format(filename), out=True)

    def create_argo(self, command, argo):
        """create_argo creates a new argument for the given command.
        """
        node = Tree.node(command.name, command.cb)
        argument = Argument(argo.name, argo.type, default=argo.default)
        node.command.add_argument(argument)
        pass

    def create_command(self, command):
        """create_command creates a new command.
        """
        node = Tree.node(command.name, command.cb)
        node.command.syntax = command.syntax
        node.command.internal = command.internal
        node.command.help = command.help
        if command.namespace:
            Tree().rename_node(node.name, '{0}.{1}'.format(command.namespace, command.name))
        node.command.build_command_parsing_tree()

    def generate_argo(self, command, argo):
        pass

    def generate_command(self, command):
        pass


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
    data = '''[{ "name": "LEAF",
                 "syntax": "LEAF ETH",
                 "internal": false,
                 "help": "leaf command",
                 "pyname": "do_leaf",
                 "arguments":
                     { "name": "ETH",
                       "default": "None",
                       "help": "Ethernet address",
                       "type":
                        { "name": "Str",
                          "module": "builtin"
                        },
                       "pyname": "eth"
                     }
               },
               { "name": "SPINE",
                 "syntax": "SPINE [leaf]?",
                 "internal": false,
                 "help": "spine command",
                 "pyname": "do_spine",
                 "arguments":
                     { "name": "leaf",
                       "default": "None",
                       "help": "Leaf name",
                       "type":
                        { "name": "Str",
                          "module": "builtin"
                        },
                       "pyname": "leaf"
                     }
               }]'''
    g = CliGenerator()
    result = g.load_commands_from_json(data)
    print(result)
