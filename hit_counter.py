from file_manager import FileReader

log_list = range(0,34)
for index, log in enumerate(log_list):
    log_list[index] = "access.log" if index == 0 else "access.log." + str(index)

print FileReader.get_uniq_ips("potkany.cz", log_list, "\/|index\.")

#(\n|^)(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})(.+"GET \/ )(.*\s.*)(potkany)(.*)