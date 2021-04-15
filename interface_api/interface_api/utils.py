from sqlalchemy.inspection import inspect

class Serialize:
    def serialize(self, excl_list=None, incl_list=None):
        """Provides serialization for SQLAlchemy models to dictionary to easily convert to JSON.
Takes optional exclusion list and inclusion list arguments."""
        # if there is an inclusion list only serialize the included columns to a dictionary
        if incl_list:
            return {column: getattr(self, column) for column in incl_list}

        # if there is an exclusion list the specified columns are excldued from the serialization
        if excl_list:
            column_list = [x for x in inspect(self.attrs.key()) if x not in excl_list]
            return {column: getattr(self, column) for column in column_list}

        # if there are no optional arguments then return all columns serialized to a dictionary
        return {column: getattr(self, column) for column in inspect(self.attrs.key())}

    @staticmethod
    def serialize_list(list_arg):
        """Serializes a list of results to a list of dictionaries"""
        return [element.serialize() for element in list_arg]
