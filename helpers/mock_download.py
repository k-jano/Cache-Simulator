import time
import yaml

config = yaml.safe_load(open("./config.yml"))

bandwith = (config['simulator']['bandwith'] * 1024 * 1024) / 8
delay = config['simulator']['delay']

def mock_download(file_size):
    time.sleep(file_size / bandwith + delay)
