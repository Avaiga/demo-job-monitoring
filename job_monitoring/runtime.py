from taipy import run


class App:
    """A singleton class that provides the Taipy runtime objects."""

    def __new__(cls):
        if not hasattr(cls, "instance"):
            cls.instance = super(App, cls).__new__(cls)
        return cls.instance

    @property
    def gui(self):
        return self.__gui

    @property
    def core(self):
        return self.__core

    @gui.setter
    def gui(self, gui):
        self.__gui = gui

    @core.setter
    def core(self, core):
        self.__core = core

    def start(self, **kwargs):
        # Starts the app by calling `taipy.run` on the core and gui objects:
        run(self.__gui, self.__core, **kwargs)
