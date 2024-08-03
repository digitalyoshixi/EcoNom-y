import os
from supabase import create_client, Client


class SupabaseAPI:
    project_url: str
    api_key: str
    database: Client

    def __init__(self, project_url: str, api_key: str):
        self.project_url = project_url
        self.api_key = api_key
        self.database = create_client(url, key)


if __name__ == "__main__":
    import load_env

    project_url: str = os.environ["SUPABASE_PROJECT_URL"]
    api_key: str = os.environ["SUPABASE_API_KEY"]
