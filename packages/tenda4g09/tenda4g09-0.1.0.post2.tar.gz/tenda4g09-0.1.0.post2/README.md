<h1 align="center">
py-tenda4g09
</h1>
<p align="center">
    <a href="https://www.gnu.org/licenses/agpl-3.0">
        <img src="https://img.shields.io/badge/License-AGPL%20v3-blue.svg" />
    </a>
    <a href="https://github.com/dorianim/py-tenda4g09/actions/workflows/publish-to-pypi.yml">
        <img src="https://github.com/dorianim/py-tenda4g09/actions/workflows/publish-to-pypi.yml/badge.svg" />
    </a>
</p>

Simple Python lib for the tenda4g09 router.

# Features
- Login to the Tenda4G09 LTE router
- Get the current status of the router
- Reboot the router
- ...More could be added quite easily
# Install
```
pip3 install tenda4g09
```

# Usage
```py
from tenda4g09 import Tenda4G09

tenda = Tenda4G09("192.168.0.1")
if tenda.login("somepassword"):
    print(tenda.status())
```