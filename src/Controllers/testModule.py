from lib.halicea.HalRequestHandler import HalRequestHandler as hrh

class TestHandler(hrh):
    
    def index(self):
        return {}