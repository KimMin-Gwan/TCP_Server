from view import *
from controller import *
from model import *


class Main():
    def __init__(self):
        self.model = Master_Model()
        self.controller = Master_Controller(self.model)
        self.app_server = AppServer(self.controller)
        
    def start_system(self):
        print("SYSTEM_CALL||RUN_SYSTEM")
        self.app_server.run_system()
        
    
if __name__ == "__main__":
    main = Main()
    main.start_system()

