from load_config import Config
import re


class FileReader:
    def __init__(self):
        pass

    @classmethod
    def get_uniq_ips(cls, domain, file_name, separate, page="/ |/index\."):
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

        :param domain: Domain name for which you want to count hits.
        :param file_name: List of the file names with access records.
        :param separate: Separated log files or not.
        :param page: Page for which you want to count hits. Default is / and index.
        :return: All unique ips which were found.
        """
        uniq_ips = set()
        # if index was changed, escape ``page``
        if page != "/ |/index\.":
            page = re.escape(page)
        for name in file_name:
            pattern = re.compile('(?:\n|^)(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}).+"GET (' + page + ')')
            # save content of file to ``cfile`` since well be using it twice
            cfile = cls.read_file(name)
            cfile_ips = set()
            remove_ips = set()
            # go and find all unique ids from ``cfile``
            for (ip, page) in re.findall(pattern, cfile):
                cfile_ips.add(ip)
            if not separate:
                # for each unique IP in ``cfile`` check if there is also IP with sub/domain name
                for ip in cfile_ips:
                    pattern = re.compile('(?:\n|^)(' + re.escape(ip) + ').+(://' + re.escape(domain) + ').*')
                    if not pattern.search(cfile):
                        remove_ips.add(ip)
            # if not separate remove all unique IPs without sub/domain reference line and join ``cfile_ips``
            # with ``uniq_ips``
            uniq_ips |= cfile_ips - remove_ips
        return uniq_ips

    @staticmethod
    def read_file(file_name):
        """
        Opens the file and returns content.
        :param file_name: Name of the file we want to open.
        :return: Content of file.
        """
        try:
            file = open(Config().get_option("location") + file_name, "r")
        except IOError as e:
            print e
            exit(1)
        else:
            with file as log:
                data = log.read()
            return data
