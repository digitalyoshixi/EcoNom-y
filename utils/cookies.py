import streamlit as st
from datetime import datetime
from extra_streamlit_components import CookieManager

cookie_manager = None


def get_cookie_manager():
    global cookie_manager
    if cookie_manager == None:
        cookie_manager = CookieManagerAPI()
    return cookie_manager


class CookieManagerAPI:
    def __init__(self):
        self.cookie_manager = CookieManager()

    def getcookie(self, cookie_name: str):
        return st.context.cookies.get(cookie_name)

    def setcookie(self, cookie_name: str, value: str, expires_at: datetime):
        return self.cookie_manager.set(cookie_name, value, expires_at=expires_at)
