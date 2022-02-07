from abc import abstractmethod


class IWSQueries:
    """
    This interface provides a commons set of database databases used by the CRUD
    operations. For each query class which implements this interface, each
    method is intended to return a query which is specific to the database
    being used.

    This interface has the potential to be modified by developers during a
    projects life cycle.
    """

    @abstractmethod
    def set_query_device(self, device):
        pass

    @abstractmethod
    def verify_device(self, device):
        pass

    @abstractmethod
    def get_device_id(self, location):
        pass

    @abstractmethod
    def list_locations(self):
        pass

    @abstractmethod
    def location_info(self, device):
        pass

    @abstractmethod
    def location_measurements(self, device):
        pass

    @abstractmethod
    def location_measurement_records(self, params, device):
        pass

    @abstractmethod
    def process_query_options(self, options, measurement):
        pass

    @abstractmethod
    def set_attribute(self, attribute: str, value):
        pass

    @abstractmethod
    def submit_device_data(self, query_data):
        pass

    @abstractmethod
    def submission_validation_params(self):
        pass

    @abstractmethod
    def client_details_request(self, username=None, email=None):
        pass

    @abstractmethod
    def create_new_client(self, username, email, password):
        pass

    @abstractmethod
    def retrieve_client_tokens(self, username):
        pass

    @abstractmethod
    def add_client_token(self, username, app_name, token):
        pass

    @abstractmethod
    def search_for_token(self, token):
        pass
