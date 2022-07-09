class Base_Connector:
    def __init__(self):
        self.clean_data = None # function that will be set for clearning data
    #

    def initialse_auth(self, *argv):
        None

    def set_query_details(self, *argv):
        None

    def get_raw_data(self):
        return []

    def get_clean_data(self):
        return []

    @staticmethod    
    def curry (prior, *additional):
        def curried(*args):
            return prior(*(args + additional))
        return curried
