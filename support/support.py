import os

def get_cache_path():
    return os.environ['BAMBOO_CACHE_PATH']

if __name__ == '__main__':
    print(get_cache_path())
