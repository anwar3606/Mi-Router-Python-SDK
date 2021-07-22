import os
from pprint import pprint

from api import MiRouterAPI

if __name__ == '__main__':
    api = MiRouterAPI(os.environ['mi_pass'])

    data = api.misystem_status()

    pprint(data.cpu)
    pprint(data.mem)
