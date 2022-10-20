## DKHP_looter
As the name suggests, this helps looting as much courses as you can (if u happen to be an APCS student in HCMUS?)

### How to use
- Run `pip install -r requirements.txt`, or just make sure that `requests` library is installed
- Cookies: Use a cookie viewer extension to copy or
  - Login to portal, turn on Devtools (F12)
  - Click into any request named `portal.ctdb.hcmus.edu.vn`, scroll down to `Request Headers`, copy all contents in `Cookie` section (remember to remove the `"Cookie: "` part)

  Once the cookie content is retrieved, paste to a file named cookie.txt

- Fire up the script as usual, respond to some promt messages, and enjoy ;)