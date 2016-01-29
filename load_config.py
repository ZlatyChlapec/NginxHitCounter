import ConfigParser
import json
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
            elif option == "files":
                location = self.get_option("location")
                files = json.loads(self.config.get("Settings", option))
                if len(files) == 1:
                    while os.path.isfile(location + files[0] + "." + str(len(files))):
                        files.append(files[0] + "." + str(len(files)))
                elif len(files) > 1:
                    for file in files:
                        if not os.path.isfile(location + file):
                            print "One or more log files weren't found."
                            exit(1)
                else:
                    print "You didn't specify file names in required format."
                    exit(1)
                return files
            elif option == "separate":
                return self.config.getboolean("Settings", option)
            elif option == "page":
                return self.config.get("Settings", option)
            elif option == "domain":
                return self.config.get("Settings", option)
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
