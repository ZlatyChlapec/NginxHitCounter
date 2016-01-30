import ConfigParser
import json
import os.path


class Config:
    def __init__(self):
        config = ConfigParser.SafeConfigParser()
        self.config = config
        if os.path.isfile("conf.ini"):
            config.read("conf.ini")
            if self.__load_options("first_time"):
                first_time = raw_input("Do you want to go through first time set up?")
                if first_time.lower() == "yes" or first_time.lower() == "y":
                    self.first_time_setup()
                    Config()
        else:
            self.first_time_setup()
            Config()
        self.location = self.__load_options("location")
        self.files = self.__load_options("files")
        self.separate = self.__load_options("separate")
        self.page = self.__load_options("page")
        self.domain = self.__load_options("domain")

    def __load_options(self, option):
        try:
            if option == "first_time":
                return self.config.getboolean("Settings", option)
            elif option == "location":
                return self.config.get("Settings", option)
            elif option == "files":
                location = self.__load_options("location")
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

    def first_time_setup(self):
        self.config.add_section('Settings')
        self.config.set('Settings', 'first_time', 'False')
        self.config.set('Settings', 'location', 'D:\\Temp\\alog\\')
        self.config.set('Settings', 'files', '["access.log"]')
        self.config.set('Settings', 'page', '')
        self.config.set('Settings', 'separate', 'False')
        self.config.set('Settings', 'domain', 'potkany.cz')

        # Writing our configuration file to 'example.cfg'
        with open('conf.ini', 'wb') as configfile:
            self.config.write(configfile)
