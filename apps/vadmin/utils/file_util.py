import os


def get_all_files(targetDir):
    files = []
    listFiles = os.listdir(targetDir)
    for i in range(0, len(listFiles)):
        path = os.path.join(targetDir, listFiles[i])
        if os.path.isdir(path):
            files.extend(get_all_files(path))
        elif os.path.isfile(path):
            files.append(path)
    return files


def remove_empty_dir(path):
    for root, dirs, files in os.walk(path, topdown=False):
        if not files and not dirs:
            os.rmdir(root)


def delete_files(delete_list: list):
    for file_path in delete_list:
        try:
            os.remove(file_path)
        except(FileNotFoundError):
            pass
