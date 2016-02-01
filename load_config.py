import ConfigParser
import json
import os.path
from colors import Colors


class Config:
    def __init__(self):
        config = ConfigParser.SafeConfigParser()
        self.config = config
        self.home_dir = os.path.dirname(os.path.abspath(__file__)) + "/"
        self.location = None
        self.files = None
        self.separate = None
        self.page = None
        self.domain = None

    def load_config(self, file_name="conf.ini"):
        if os.path.isfile(self.home_dir + file_name):
            self.config.read(self.home_dir + file_name)
            size = os.stat(self.home_dir + file_name).st_size
            if size == 0 or self.__load_options("first_time"):
                first_time = raw_input("Do you want to go through first time set up? " + Colors.White + "(e.g. y/n)\n" +
                                       Colors.Red + "All previous settings will be erased!!!" + Colors.End + "\n")
                if first_time.lower() in ["yes", "y"]:
                    if size == 0:
                        self.__first_time_setup(True, file_name)
                    else:
                        self.__first_time_setup(False, file_name)
            else:
                self.location = self.__load_options("location")
                self.files = self.__load_options("files")
                self.separate = self.__load_options("separate")
                self.page = self.__load_options("page")
                self.domain = self.__load_options("domain")
        else:
            self.__first_time_setup(True, file_name)

    def __load_options(self, option):
        try:
            if option == "first_time":
                return self.config.getboolean("Settings", option)
            elif option == "location":
                return self.config.get("Settings", option)
            elif option == "files":
                location = self.__load_options("location")
                files = json.loads(self.config.get("Settings", option))
                return self.__all_files(location, files)
            elif option == "separate":
                return self.config.getboolean("Settings", option)
            elif option == "page":
                return self.config.get("Settings", option)
            elif option == "domain":
                return self.config.get("Settings", option)
            else:
                print Colors.Red + "One or more options are missing from conf.ini" + Colors.End
                exit(1)
        except ConfigParser.NoSectionError:
            print Colors.Red + "At the start of file there have to be section named `Settings`.\nIf you do have " \
                               "section named `Settings` and you are still getting this error check permissions." +\
                  Colors.End
            exit(1)
        except ConfigParser.NoOptionError:
            print Colors.Red + "Option " + option + " is missing from conf.ini" + Colors.End
            exit(1)
        except ValueError:
            print Colors.Red + "Wrong value of " + option + "." + Colors.End
            exit(1)

    def __first_time_setup(self, first_time, file_name):
        if first_time:
            self.config.add_section('Settings')
        self.config.set('Settings', 'first_time', 'False')

        l_hint = "# Path to log files. Linux example: '/var/log/nginx/'. Windows example: 'D:/folder/log/'."
        f_hint = "# Set name of files in which information are. If your files are named 'access.log', 'access.log.1'," \
                 " ... ,'access.log.434'\n# then it's enough to specify just name of the first file. If you have " \
                 "just one file specify his name in format 'file_name'\n# if you happen to have more files specify " \
                 "them like 'file_name',,'second_file'"
        p_hint = "# Specify page for which you want to count hits (e.g. '/about.'. If empty, program will be " \
                 "counting hits for '/ |/index.'"
        s_hint = "# If you have in log file only access logs from one sub/domain, set this to True else False."
        d_hint = "# If separate == False you need to specify domain for which you wish to count hits."

        self.location = raw_input(Colors.White + l_hint + Colors.End + "\nLocation: ")
        self.files = raw_input(Colors.White + f_hint + Colors.End + "\nFiles: ").split(",,")
        self.page = raw_input(Colors.White + p_hint + Colors.End + "\nPage: ")
        self.separate = raw_input(Colors.White + s_hint + Colors.End + "\nSeparate: ").lower() in \
                        ["1", "yes", "true", "on", "True"]
        self.domain = raw_input(Colors.White + d_hint + Colors.End + "\nDomain: ")

        self.config.set('Settings', 'location', self.location)
        self.config.set('Settings', 'files', json.dumps(self.files))
        self.config.set('Settings', 'page', self.page)
        self.config.set('Settings', 'separate', str(self.separate))
        self.config.set('Settings', 'domain', self.domain)

        self.files = self.__all_files(self.location, self.files)

        try:
            file = open(self.home_dir + file_name, 'w')
        except IOError as e:
            print Colors.Red + e + Colors.End
            exit(1)
        else:
            with file as configfile:
                self.config.write(configfile)

    def __all_files(self, location, files):
        if len(files) == 1:
            while os.path.isfile(location + files[0] + "." + str(len(files))):
                files.append(files[0] + "." + str(len(files)))
        elif len(files) > 1:
            for file in files:
                if not os.path.isfile(location + file):
                    print Colors.Red + "One or more log files weren't found." + Colors.End
                    exit(1)
        else:
            print Colors.Red + "You didn't specify file names in required format." + Colors.End
            exit(1)
        return files
