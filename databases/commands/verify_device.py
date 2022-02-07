from Interface_command import ICommand
from ..interface_dbentity import Interface_DbEntity, QueryObj, DBSchema


class CommandVerifyDevice(ICommand):
    
    def __init__(self, reciever: Interface_DbEntity) -> None:
        super().__init__(reciever)

    def exec(self, device):
        
        # the schema provides lookups for storage 
        # location names (tables or collections) on a databases
        schema = self.reciever.schema 
        self.reciever.open_db_connection()
        query = self.reciever.query(
            schema.device_locations,
            QueryObj(
                schema.device_id, 
                device
                )
            )     
        self.reciever.close_db_connection()