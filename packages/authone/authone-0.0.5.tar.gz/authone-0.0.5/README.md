# AuthOne-Python
AuthOne Python SDK

```bash
pip install authone
```


## Quick Start

```python
from authone import AuthOneClient


auth = AuthOneClient(app_id, app_secret='<YOUR_APP_SECRET>')

resp = auth.SocialUser.get_userinfo_by_token('token')

respdata = resp.data
print(respdata["user_id"], respdata["user_name"], respdata["email"])
# Read the docs to learn more!
```
