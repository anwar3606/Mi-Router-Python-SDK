from pprint import pprint

from api import MiRouterAPI

if __name__ == '__main__':
    router_api = MiRouterAPI('your_pass')
    data = router_api.misystem_status()

    pprint(data['cpu'])
    pprint(data['mem'])
