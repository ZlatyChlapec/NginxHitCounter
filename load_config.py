import ConfigParser
import os.path


class Config:
    def __init__(self):
        if os.path.isfile("conf.ini"):
            config = ConfigParser.SafeConfigParser()
            config.read("conf.ini")
            self.config = config
        else:
            print "`conf.ini` file is missing.\n Please visit " \
                  "https://github.com/ZlatyChlapec/NginxHitCounter/blob/master/conf.ini to get the idea how one " \
                  "should look like."
            exit(1)

    def get_option(self, option):
        try:
            if option == "location":
                return self.config.get("Settings", option)
            elif option == "separate":
                return self.config.getboolean("Settings", option)
            else:
                print "One or more options are missing from conf.ini"
                exit(1)
        except ConfigParser.NoSectionError:
            print "At the start of file there have to be section named `Settings`."
            exit(1)
        except ConfigParser.NoOptionError:
            print "Option " + option + " is missing from conf.ini"
            exit(1)
        except ValueError:
            print "Wrong value of " + option + "."
            exit(1)
