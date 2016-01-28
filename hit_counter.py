from file_manager import FileReader
from load_config import Config
import time


# ToDo: Make it so first time run will be special: Program will parse all files and save obtained number of accesses to
#       file and for next iterations program will be just raising this number also program won't be checking all files
#       but just most updated one and it shall do so on every change.
# ToDo: Make domain to be configurable without change of code.
# ToDo: Make it so logs file names can be configurable without change of code.
# ToDo: Make it so in first time run you'll be asked to configure program.
# ToDo: Try to make change of regexes possible without editing of code.
# ToDo: Progress bar when parsing files.
# ToDo: Add support for .gz files.
# ToDo: Add bot filtration option.

start_time = time.clock()

log_list = range(0,34)
for index, log in enumerate(log_list):
    log_list[index] = "access.log" if index == 0 else "access.log." + str(index)

print "There are %s unique IPs in your logs." % len(FileReader.get_uniq_ips("potkany.cz",
                                                                            Config().get_option("location"),
                                                                            log_list,
                                                                            Config().get_option("separate")))

print "It took %.2fs to figure it out." % (time.clock() - start_time)
