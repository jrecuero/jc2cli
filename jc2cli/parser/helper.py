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
MODULE = 'CLI.journal'
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
class Journal(object):
    """Journal class that provides a container with all matching required for
    checking if the commmand syntax is valid and napping arguments entered in
    the command line with command arguments.
    """

    def __init__(self):
        """Journal class initialization method.
        """
        self.path = list()
        self.argos = dict()
        self.traverse_node = None
        self.root = None
        self.__cache = {}

    def get_from_cache(self, key):
        """Retreives some data to the cache.

        Args:
            key (object) : key for the cached data to be retrieved.

        Returns:
            object : data found in cache, None if key is not found.
        """
        return self.__cache.get(key, None)

    def set_to_cache(self, key, value):
        """Adds cache data for the given key.

        If the key already exits, the data is being overwritten.

        Args:
            key (object) : key for the data to be cached.
            value (object) : data being cached.
        """
        self.__cache[key] = value

    def add_node(self, node):
        """Method that adds a new node.

        Args:
            node (Node): node instance to be added.
        """
        if node:
            self.path.append(node)
            self.argos.update(node.argo)
            self.traverse_node = node
