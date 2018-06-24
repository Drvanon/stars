import yaml

SETTINGS_FILE = 'settings.yaml'

print('Loading settings from {}'.format(SETTINGS_FILE))
settings = {}
with open(SETTINGS_FILE, 'r') as f:
    data = yaml.load(f)
    settings = data

