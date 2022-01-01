import psutil as psutil


def get_cpu_info():

    pass


def get_memory_info():

    pass


def get_disk_info():

    pass


def get_cpu_used_percent():

    try:
        return float(psutil.cpu_percent(0.1))
    except:
        pass


def get_memory_used_percent():
    try:
        memory_info = psutil.virtual_memory()
        return float(memory_info.percent)
    except:
        pass


def get_disk_used_percent():
    print(psutil.disk_partitions())
    try:
        return float(psutil.disk_usage("/").percent)
    except:
        pass


if __name__ == '__main__':
    get_disk_used_percent()
