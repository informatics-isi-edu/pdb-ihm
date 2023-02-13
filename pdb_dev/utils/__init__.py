env = None
DEV = 'dev'
STAGING = 'staging'
WWW = 'www'

def set_env(host, catalog_id):
    global env

    if host == "data.pdb-dev.org":
        env = 'www'
    elif "catalog_id" == 50:
        env = 'staging'
    else:
        env = 'dev'
