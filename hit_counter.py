from file_manager import FileReader
from load_config import Config
import time


# ToDo: Save somewhere number from first run and later parse just newest file and keep updating this number.
# ToDo: Try to make change of regexes possible without editing of code.
# ToDo: Progress bar when parsing files.
# ToDo: Add support for .gz files.
# ToDo: Add bot filtration option.

start_time = time.clock()

config = Config()
config.load_config()
print "\nFor domain '" + config.domain + "' page '" + config.page + "', there are %s unique IPs in your logs." % \
            len(FileReader.get_uniq_ips(config.location, config.files, config.separate, config.page, config.domain))

print "It took %.2fs to figure it out." % (time.clock() - start_time)
