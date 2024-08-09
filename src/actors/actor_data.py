from direct.actor.Actor import Actor


class ActorData:
    """Base class for VisorView actors. These do not store the actor at any point, rather, store information on how
    to generate them at any given moment, as well as a method to do just that.
    """
    """Class attribute that holds special nodes the actor has, e.g. shadow or head
    example usage when overriding:
    special_nodes = {"shadow": "**/shadow**", 
                     "head": "**/head**"}
    """
    _actor_type = ""
    _special_nodes = {}

    def __init__(self):
        self.__data = {}
        self.__name = ""

        # Special data that describes if specific nodes should be colored/scaled, i.e.:
        # "scale_nodes": {"**/head": 0.75} OR "color_nodes": {"**/head": (0, 1, 0.75, 1)}
        self.add_data("color_nodes", {})
        self.add_data("scale_nodes", {})

    def add_data(self, key, data):
        self.__data[key] = data

    def get_data(self, key):
        return self.__data[key] if key in self.__data else None

    def set_name(self, name):
        self.__name = name

    def get_name(self):
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
        return self._actor_type
