import os
import supabase
import uuid

# -- Create a global variable for the supabase API so all files can use it
supabase_api = None
def get_supabase_api():
    global supabase_api
    if supabase_api is None:
        import load_env
        project_url: str = os.environ["SUPABASE_PROJECT_URL"]
        api_key: str = os.environ["SUPABASE_API_KEY"]
        supabase_api = SupabaseAPI(project_url, api_key)
    return supabase_api

class SupabaseAPI:
    database: supabase.Client

    def __init__(self, project_url: str, api_key: str):
        self.database = supabase.create_client(project_url, api_key)

    def select(self, table, columns):
        return supabase_api.database.table(table).select(columns).execute()

    def insert(self, table, keymap):
        supabase_api.database.table(table).insert(keymap).execute()

    def add_user(self, username, password, numfamily):
        result = supabase_api.database.table("profiles").select("id").order("id", desc=True).limit(1).execute()
        max_id = result.data[0]['id'] if result.data else 0
        supabase_api.insert("profiles",{
            "profile" : username,
            "password" : password,
            "family_members" : numfamily,
            "id" : max_id+1
        })
    #def verify_user(self, username, password):


if __name__ == "__main__":
    import load_env

    project_url: str = os.environ["SUPABASE_PROJECT_URL"]
    api_key: str = os.environ["SUPABASE_API_KEY"]

    supabase_api = SupabaseAPI(project_url, api_key)
    #print(supabase_api.database.table("profiles").select("*").execute())
   
    supabase_api.insert("profiles",{
        "profile" : "daniel",
        "password" : "password123",
        "family_members" : 20,
        "id" : max_id+1
       })