from extra_streamlit_components import CookieManager


def getcookie(cookie_name):
    cookies = CookieManager()
    return cookies.get(cookie_name)
