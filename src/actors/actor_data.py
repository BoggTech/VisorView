from direct.actor.Actor import Actor


class ActorData:
    """Base class for VisorView actors. These do not store the actor at any point, rather, store information on how
    to generate them at any given moment, as well as a method to do just that.
    """
    _actor_type = ""        # variable that tracks the instances name; this can be overriden where appropriate.
    _special_nodes = {}     # dictionary that keeps track of any 'special nodes' the actor has, i.e:
                            # "head": "**/head**" OR "shadow": "**/shadow**"

    def __init__(self):
        """Initializes the ActorData instance."""
        self.__data = {}    # private dict for storing data
        self.__name = ""    # name of this ActorData instance

    def add_data(self, key, data):
        """Adds data to the ActorData instance's 'data' dictionary.

        :param key: The key to add to the 'data' dictionary.
        :type key: str
        :param data: The data to add to the 'data' dictionary.
        """
        self.__data[key] = data

    def get_data(self, key):
        """Retrieves data from the ActorData instance's 'data' dictionary.

        :param key: The key to retrieve data from.
        :type key: str
        :return: Data from the given key, None if the key does not exist."""
        return self.__data[key] if key in self.__data else None

    def set_name(self, name):
        """Sets the name of this ActorData instance.

        :param name: The name to set.
        :type name: str"""
        self.__name = name

    def get_name(self):
        """Retrieves the name of this ActorData instance."""
        return self.__name

    def get_special_node(self, key):
        """Method that returns a path to a special node given a key. If no node exists, it will return None

        :param key: The name of the node"""
        return self._special_nodes[key] if key in self._special_nodes else None

    def generate_actor(self):
        """Returns an actor based on the data within this class."""
        pass

    def get_animation_names(self):
        """Returns a list of valid animations for the actor."""
        pass

    def get_type(self):
        """Returns the type of the actor.

        :return: The type of the actor.
        :rtype: str"""
        return self._actor_type
