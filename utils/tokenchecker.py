from extra_streamlit_components import CookieManager

cookies = CookieManager()
# token = cookies.get("token")

def getcookie(cookie):
    return cookies.get(cookie)
