import os
import supabase
import uuid


supabase_api = None


def get_supabase_api():
    global supabase_api
    if supabase_api is None:
        # Create a new connection if it doesn't exist
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

    def selectspecific(
        self, table, columns, eqcol, eqval
    ):  # SELECT <column> from <table> where <eqcol> = <eqval>
        return (
            supabase_api.database.table(table)
            .select(columns)
            .eq(eqcol, eqval)
            .execute()
        )

    def insert(self, table, keymap):
        supabase_api.database.table(table).insert(keymap).execute()

    def add_user(self, username, password, numfamily):
        result = (
            supabase_api.database.table("profiles")
            .select("id")
            .order("id", desc=True)
            .limit(1)
            .execute()
        )
        max_id = result.data[0]["id"] if result.data else 0
        supabase_api.insert(
            "profiles",
            {
                "profile": username,
                "password": password,
                "family_members": numfamily,
                "id": max_id + 1,
            },
        )

    def add_token(self, username, token, expiration):
        supabase_api.insert(
            "tokens", {"token": token, "profile": username, "expiry": expiration}
        )

    def add_recipe(
        self, recipeName, ingredientList, imageURL, portionMultiplier, recipeURL
    ):
        supabase_api.insert(
            "recipes",
            {
                "recipeName": recipeName,
                "ingredientList": ingredientList,
                "imageURL": imageURL,
                "portionMultiplier": portionMultiplier,
                "recipeURL": recipeURL,
            },
        )


if __name__ == "__main__":
    import load_env

    project_url: str = os.environ["SUPABASE_PROJECT_URL"]
    api_key: str = os.environ["SUPABASE_API_KEY"]

    supabase_api = SupabaseAPI(project_url, api_key)
    # print(supabase_api.database.table("profiles").select("*").execute())
    result = (
        supabase_api.database.table("profiles")
        .select("id")
        .order("id", desc=True)
        .limit(1)
        .execute()
    )
    max_id = result.data[0]["id"] if result.data else 0

    supabase_api.insert(
        "profiles",
        {
            "profile": "daniel",
            "password": "password123",
            "family_members": 20,
            "id": max_id + 1,
        },
    )
