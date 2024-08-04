from extra_streamlit_components import CookieManager


# token = cookies.get("token")


def getcookie(cookie):
    cookies = CookieManager()  # yes, we need to make a new one each time to update it
    return cookies.get(cookie)
