import time
import re


class FileReader:
    def __init__(self):
        pass

    @staticmethod
    def get_uniq_ips(location, file_names, separate, page="", domain=""):
        """
        Retrieves unique ips from logs. If access logs for each sub/domain are in separate files it works perfectly BUT
        if there are access logs for more than one sub/domain (``separate`` == False), in one log file it will count IP
        only, if there was also any resource loaded from that IP, also it won't count if ip with ``page`` and resource
        loading line are in different files.

        Example:
            89.177.128.126 - - [24/Jan/2016:23:37:25 +0100] "GET / HTTP/1.1"... < here is connection to ``page``
            ...                                                                 < here can be anything or nothing
            89.177.128.126..."://domain"...                                     < this is resource loading line

        Also this works with default nginx log scheme, if you are using custom one you may have to create new custom
        regexes.

        :param location: Location of folder in which files are located.
        :param file_names: List of the file names with access records.
        :param separate: Separated log files or not.
        :param page: Page for which you want to count hits. Default is / and index.
        :param domain: Domain name for which you want to count hits.
        :return: All unique ips which were found.
        """
        # if index was changed, escape ``page``
        if page == "":
            page = "/ |/index\."
        else:
            page = re.escape(page)
        if domain == "" and separate is False:
            print "You've set separate to False but you didn't specify domain for which you want to count hits."
            exit(1)

        uniq_ips = set()
        time_parsing_ips = 0
        time_verifying_ips = 0

        for name in file_names:
            pattern = re.compile('(?:\n|^)(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}).+"GET (' + page + ')')
            # save content of file to ``cfile`` since well be using it twice
            cfile = FileReader.read_file(location + name)
            cfile_ips = set()
            remove_ips = set()
            # go and find all unique ids from ``cfile``
            time_parsing_ips_start = time.clock()
            for (ip, page) in re.findall(pattern, cfile):
                cfile_ips.add(ip)
            time_parsing_ips += time.clock() - time_parsing_ips_start

            if not separate:
                # for each unique IP in ``cfile`` check if there is also IP with sub/domain name
                time_verifying_ips_start = time.clock()
                for ip in cfile_ips - uniq_ips:
                    pattern = re.compile('(?:\n|^)(' + re.escape(ip) + ').+(://' + re.escape(domain) + ').*')
                    if not pattern.search(cfile):
                        remove_ips.add(ip)
                time_verifying_ips += time.clock() - time_verifying_ips_start

            uniq_ips |= cfile_ips - remove_ips

        print "Parsing files for %.2fs" % time_parsing_ips
        print "Verifying files for %.2fs" % time_verifying_ips
        return uniq_ips

    @staticmethod
    def read_file(path_to_file):
        """
        Opens the file and returns content.
        :param path_to_file: Name of the file we want to open.
        :return: Content of file.
        """
        try:
            file = open(path_to_file, "r")
        except IOError as e:
            print e
            exit(1)
        else:
            with file as log:
                data = log.read()
            return data
