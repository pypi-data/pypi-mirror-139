import requests, hashlib

class Tenda4G09:

    def __init__(self, host):
        self._host = host
        self._session = requests.Session()
        self._loggedIn = False

    def _request(self, method, url, data=None, headers=None, allow_redirects=False):
        if data is None:
            data = {}
        if headers is None:
            headers = {}

        # Auth cookie
        if self._loggedIn:
            headers["Cookie"] = f"password={self._password}"

        req = requests.Request(method, url, headers=headers, data=data)
        
        return self._session.send(req.prepare(), allow_redirects=allow_redirects)

    def login(self, password):
        self.logout()
        password = hashlib.md5(str.encode(password)).hexdigest()
        url = f"http://{self._host}/login/Auth"
        headers = {
                "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:97.0) Gecko/20100101 Firefox/97.0",
                "Accept": "*/*",
                "Accept-Language": "de-DE,en-US;q=0.8,en;q=0.5,fr-FR;q=0.3",
                "Accept-Encoding": "gzip, deflate",
                "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
                "X-Requested-With": "XMLHttpRequest",
                "Origin": f"http://{self._host}",
                "DNT": "1",
                "Referer": f"http://{self._host}/login.html",
                "Pragma": "no-cache",
                "Cache-Control": "no-cache",
                "Connection": "keep-alive"
        }
        data = {"username": "admin", "password": password}

        r = self._request("POST", url, headers=headers, data=data)

        if r.status_code == 302 and r.headers["Location"] == f"http://{self._host}/main.html" and "Set-Cookie" in r.headers and "password" in r.headers["Set-Cookie"]:
            print("Login success!")
            self._password = self._session.cookies.get("password")
            self._session.cookies.clear()
            self._loggedIn = True
            return True
        else:
            print("Login error!")
            self._password = ""
            self._loggedIn = False
            return False

    def logout(self):
        url = f"http://{self._host}/goform/exit"
        self._request("GET", url)

    def status(self):
        if not self._loggedIn:
            return False, None

        url = f"http://{self._host}/goform/GetRouterStatus"
        r = self._request("GET", url)

        if r.status_code != 200:
            return False, None
            
        return True, r.json()

    def reboot(self):
        url = f"http://{self._host}/goform/SysToolReboot"
        r = self._request("POST", url, data={"action": "0"})
        return r.status_code == 302 and r.headers["Location"] == f"http://{self._host}/redirect.html?3"