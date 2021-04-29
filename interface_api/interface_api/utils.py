from sqlalchemy.inspection import inspect
import datetime

class Serialize:
    def serialize(self, excl_list:list = None, incl_list:list = None):
        """Provides serialization for SQLAlchemy models to dictionary to easily convert to JSON.
Takes optional exclusion list and inclusion list arguments."""
        # if there is an inclusion list only serialize the included columns to a dictionary
        if incl_list:
            return {column: getattr(self, column) for column in incl_list}

        # if there is an exclusion list the specified columns are excldued from the serialization
        if excl_list:
            column_list = [x for x in inspect(self).attrs.keys() if x not in excl_list]
        else:
            column_list = [x for x in inspect(self).attrs.keys()]
        # exception to handle sqlite date and time because it returns python datetime object
        return_dict = {column: getattr(self, column) for column in column_list}
        if isinstance(return_dict['date'], datetime.date):
            return_dict['date'] = return_dict['date'].strftime('%Y-%m-%d')
        if isinstance(return_dict['time'], datetime.time):
            return_dict['time'] = return_dict['time'].strftime('%H:%M')
        return return_dict



    @staticmethod
    def serialize_list(list_arg: list, excl_list:list = None, incl_list:list = None):
        """Serializes a list of results to a list of dictionaries"""
        return [element.serialize(excl_list, incl_list) for element in list_arg]

