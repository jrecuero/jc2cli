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
from prompt_toolkit.completion import Completer, Completion


# -----------------------------------------------------------------------------
#
#   ___ ___  _ __  ___| |_ __ _ _ __ | |_ ___
#  / __/ _ \| '_ \/ __| __/ _` | '_ \| __/ __|
# | (_| (_) | | | \__ \ || (_| | | | | |_\__ \
#  \___\___/|_| |_|___/\__\__,_|_| |_|\__|___/
#
# -----------------------------------------------------------------------------
#
MODULE = 'CLI.completer'
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
class CliCompleter(Completer):

    def __init__(self, cli):
        self._node_path = None
        self._cli = cli

    def reset(self):
        self._node_path = None

    def get_completions(self, document, complete_event):
        matches = None
        line_str = document.text.lstrip()
        word_before_cursor = document.get_word_before_cursor(WORD=True)
        if ' ' not in line_str:
            matches = [m for m in self._cli.commands.keys() if m.startswith(word_before_cursor)]
            for m in matches:
                yield Completion(m, start_position=-len(word_before_cursor))
        else:
            line_as_list = line_str.split()
            if len(line_as_list) == 0:
                return
            last_token = line_as_list[-1] if line_str[-1] != ' ' else ' '
            command_label = line_as_list[0]
            node = self._cli.context.root.get_node(command_label)
            if not node:
                return
            command = node.command
            if command is not None:
                root = command.syntax_root
                cli_args = command.get_cli_args(" ".join(line_as_list[1:]))
                node_path = None
                children_nodes = None
                try:
                    node_path = root.find_path(cli_args)
                    logger.debug('cli_args: {0}, node_path: {1}'.format(cli_args, node_path))
                except Exception as ex:
                    logger.error('{0}, {1} | {2}'.format(ex, ex.__traceback__.tb_lineno, self._node_path))

                if not node_path and self._node_path is None:
                    # if there is not path being found and there is not any
                    # previous path, just get the completion under the root.
                    self._node_path = [root, ]
                elif node_path and line_str[-1] == ' ':
                    # if there is a path found and the last character
                    # entered is a space, use that path.
                    self._node_path = node_path

                if self._node_path:
                    # Get children from the path found or the the last path
                    children_nodes = self._node_path[-1].get_children_nodes() if self._node_path[-1] else None
                else:
                    # if there was not path or any last path, get children
                    # from the root.
                    children_nodes = root.get_children_nodes()

                if children_nodes:
                    helps = [c.completer.help(last_token) for c in children_nodes]
                    self._cli.toolbar_str = " | ".join(helps)
                    for child in children_nodes:
                        logger.debug('child is: {0}'.format(child.label))
                        matches = child.completer.complete(document, last_token)
                        if matches is None:
                            continue
                        for i, m in enumerate(matches):
                            yield Completion(m, start_position=-len(word_before_cursor))

                # TODO: Trace and debug information to be removed or optimized.
                logger.debug('matches: {0}'.format(matches))
                logger.debug('doc.text: "{0}", last-doc.text: "{1}" command: {2}'.format(document.text, line_as_list[-1], command))
                logger.debug('children_nodes: {}'.format(children_nodes))
                if children_nodes:
                    logger.debug('              : {}'.format([x.name for x in children_nodes]))
                logger.debug('node_path: {}'.format(node_path))
                if node_path:
                    logger.debug('         : {}'.format([x.name for x in node_path]))
                if self._node_path and self._node_path[-1] is not None:
                    logger.debug('self._node_path: {}'.format(self._node_path))
                    logger.debug('               : {}'.format([x.name for x in self._node_path]))
