from parser import Client
from gsh_upload import upload


if __name__ == '__main__':
    parser = Client()
    parser.run()
    upload()
