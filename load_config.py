import ConfigParser


class Config:
    def __init__(self):
        config = ConfigParser.ConfigParser()
        config.read("conf.ini")
        self.config = config

    def get_option(self, option):
        try:
            if option == "location":
                return self.config.get("Settings", option)
            elif option == "separate":
                return self.config.getboolean("Settings", option)
            else:
                print "One or more options are missing from conf.ini"
                exit(1)
        except ConfigParser.NoOptionError:
            print "Option " + option + " is missing from conf.ini"
            exit(1)
        except ValueError:
            print "Wrong value of " + option + "."
            exit(1)
