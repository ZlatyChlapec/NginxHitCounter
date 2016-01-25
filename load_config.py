import ConfigParser


class Config:
    def __init__(self):
        config = ConfigParser.ConfigParser()
        config.read("conf.ini")
        self.config = config

    def get_path(self):
        if self.config.get("Settings", "system") == "linux":
            return self.config.get("Settings", "location") + "/"
        else:
            return self.config.get("Settings", "location") + "\\"
