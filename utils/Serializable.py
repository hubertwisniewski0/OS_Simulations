class Serializable:
    """
    Interface which makes a class JSON-serializable (using Encoder class)
    """
    def serialize(self):
        """
        Returns a serializable representation of an object
        :return: (In)directly JSON-serializable object
        """
        raise NotImplementedError()
