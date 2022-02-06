from time import sleep
from PIL import Image

data_path = "./data/"


def main(file_name, points, iterations, k):
    # This function receives the file name of an image already saved on src/data directory and the corresponding parameters.
    # The function process the image already saved and then save it with the name output-<file_name> where file_name is the file name of the file, example: output-lena.png.
    sleep(5)
    img = Image.open(data_path + file_name).convert('L')
    img.save(data_path + f'output-{file_name}')
