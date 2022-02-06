import os


def create_directory_if_not_exists(full_path):
    paths = full_path.split('/')
    for i_path in range(1, len(paths)):
        path = "/".join(paths[:i_path + 1])
        if not os.path.exists(path):
            os.mkdir(path)


def save_file(file, data_path):
    create_directory_if_not_exists(data_path)
    with open(data_path + file.filename, "wb") as buffer:
        buffer.write(file.file.read())
