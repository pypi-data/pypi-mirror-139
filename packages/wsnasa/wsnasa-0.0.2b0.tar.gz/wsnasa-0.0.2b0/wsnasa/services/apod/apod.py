from wsnasa.entity.abclass.abcapod import AbcAPOD


class APOD(AbcAPOD):

    def __init__(self):
        self.__name = self.__class__.__name__
        super().__init__()
