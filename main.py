from gevent import monkey

monkey.patch_all()
from tests.test_ import __text__

if __name__ == '__main__':
    __text__()
