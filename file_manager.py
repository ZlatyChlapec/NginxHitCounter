from load_config import Config
import re


class FileReader:
    def __init__(self):
        pass

    @classmethod
    def get_uniq_ips(cls, domain, file_name, page="/ |/index\."):
        """
        If you are a smart boy and have accesses for each website in separate file I advise to cut regex after this
        group (.+"GET ' + page + ' ).

        If you have access from multiple domains loged in one file you can use current regex but it won't count accesses
        which happend at almost same time. Since in that case following line doesn't have to be one with domain name.


        :param file_name: List of the file names with access records.
        :param page: Page for which you want to count hits. Default is / or index. Don't forget to escape special chars.
        :param domain: Domain name for which you want to count hits.
        :return:
        """
        uniq_ips = []
        if not page == "/ |/index\.":
            page = re.compile(page)
        for name in file_name:
            pattern = re.compile('(?:\n|^)(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}).+"GET (' + page + ')')
            cfile = cls.get_file(name)
            for (ip, page) in re.findall(pattern, cfile):
                uniq_ips.append(ip)
                uniq_ips = list(set(uniq_ips))
                if uniq_ips[-1] == ip:
                    if not Config().get_separate() == True:
                        pattern = re.compile('(?:\n|^)(' + re.escape(ip) + ').+(://' + re.escape(domain) + ').*')
                        if not pattern.search(cfile):
                            uniq_ips.remove(ip)
        return len(uniq_ips)

    @staticmethod
    def get_file(file_name):
        with open(Config().get_path() + file_name, "r") as log:
            data = log.read()
        return data
