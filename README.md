## Portal_tools
As the name suggests, this helps looting as much courses as you can (if u happen to be an APCS student in HCMUS?)

### Disclaimer
This script assumes that you're registering courses on porta.. *cough cough.
And also it's not likely that the format of cookies or body format will change, but if it does, gimme an issue plz

### How to use
- Run `pip install -r requirements.txt`, or just make sure that `requests` library is installed
- Cookies: Use a cookie viewer extension to copy or
  - Login to portal, turn on Devtools (F12)
  - Click into any request named `portal.ctdb.hcmus.edu.vn`, scroll down to `Request Headers`, copy all contents in `Cookie` section (remember to remove the `"Cookie: "` part)

  Once the cookie content is retrieved, paste to a file named cookie.txt

- To loot all subjects, run `python3 main.py dkhp`
- To get scores of ur archenemy, or ur crush, run `python3 main.py score`
- Answer some self-explained promts and we're good to go
