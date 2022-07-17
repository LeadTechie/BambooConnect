class Base_Connector:
    def __init__(self):
        None

    def initialse_auth(self, *argv):
        None

    def set_query_details(self, *argv):
        None

    def get_raw_data(self):
        return []

    def get_clean_data(self):
        return self.clean_data(self.get_raw_data())

    def default_clean_data(self, data):
        return data

    #Base class, simply return original data
    def clean_data(self, data):
        return data

    @staticmethod
    def curry (prior, *additional):
        def curried(*args):
            return prior(*(args + additional))
        return curried
