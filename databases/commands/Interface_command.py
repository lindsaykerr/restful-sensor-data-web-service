from ..interface_dbentity import Interface_DbEntity

class ICommand:
    def __init__(self, reciever:Interface_DbEntity) -> None:
        self.reciever = reciever
    def exec(self):
        pass