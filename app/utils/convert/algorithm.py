from pyclbr import Function
class Algorithm:
    data=''

    def __init__(self,data):
        self.data=data

    def convertTo(self,convert:Function):
        return convert(self.data)