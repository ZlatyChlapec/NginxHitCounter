from file_manager import FileReader
from load_config import Config
import time


# ToDo: Make it so first time run will be special: Program will parse all files and save obtained number of accesses to
#       file and for next iterations program will be just raising this number also program won't be checking all files
#       but just most updated one and it shall do so on every change.
# ToDo: Make it so in first time run you'll be asked to configure program.
# ToDo: Try to make change of regexes possible without editing of code.
# ToDo: Progress bar when parsing files.
# ToDo: Add support for .gz files.
# ToDo: Add bot filtration option.

start_time = time.clock()

config = Config()
config.load_config()
print "\nThere are %s unique IPs in your logs." % len(FileReader.get_uniq_ips(config.location,
                                                                            config.files,
                                                                            config.separate,
                                                                            config.page,
                                                                            config.domain))

print "It took %.2fs to figure it out." % (time.clock() - start_time)
