class Enum:
    def __init__(self, init: int):
        self.__value = init
    def GetRawValue(self)->int:
        return self.__value
    def SetRawValue(self, value: int)->None:
        self.__value = value
    def __eq__(self , other):
        return self.GetRawValue() == other.GetRawValue()
    def __ne__(self , other):
        return self.GetRawValue() != other.GetRawValue()

class Tick:
    def __init__(self, waitFrame: int):
        self.__waitFrame = waitFrame
        self.__current = 0
    def Reset(self)->None:
        self.__current = 0
    def Trigger(self)->bool:
        self.__current = (self.__current + 1) % (self.__waitFrame)
        if self.__current == 0:
            return True
        else:
            return False
        

class Vector2D:
    def __init__(self, x: int | float, y: int| float):
        self.x = x
        self.y = y
    def __add__(self, other):
        return Vector2D(self.x + other.x, self.y + other.y)
    def __sub__(self, other):
        return Vector2D(self.x - other.x, self.y - other.y)
    def __eq__(self, other):
        if self.x == other.x and self.y == other.y:
            return True
        return False
    def __ne__(self, other):
        if self.x == other.x and self.y == other.y:
            return False
        return True