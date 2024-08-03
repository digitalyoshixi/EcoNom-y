import os
import supabase


class SupabaseAPI:
    database: supabase.Client

    def __init__(self, project_url: str, api_key: str):
        self.database = supabase.create_client(project_url, api_key)


if __name__ == "__main__":
    import load_env

    project_url: str = os.environ["SUPABASE_PROJECT_URL"]
    api_key: str = os.environ["SUPABASE_API_KEY"]

    supabase_api = SupabaseAPI(project_url, api_key)
    