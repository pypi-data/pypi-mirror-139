from wsnasa.entity.abclass.abcrover import ABCRover


class Opportunity(ABCRover):

    def __init__(self):
        self.__name = self.__class__.__name__
        super().__init__(self.__name)
