from tenda4g09 import Tenda4G09

tenda = Tenda4G09("192.168.0.1")
if tenda.login("somepassword"):
    print(tenda.status())