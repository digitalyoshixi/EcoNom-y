import os
import datetime
import bcrypt
import jwt
import supabase

supabase_api = None


def get_supabase_api():
    global supabase_api
    if supabase_api is None:
        # Create a new connection if it doesn't exist
        project_url: str = os.environ["SUPABASE_PROJECT_URL"]
        api_key: str = os.environ["SUPABASE_API_KEY"]
        jwt_secret_key: str = os.environ["JWT_SECRET_KEY"]
        supabase_api = SupabaseAPI(project_url, api_key, jwt_secret_key)
    return supabase_api


class SupabaseAPI:
    database: supabase.Client
    jwt_secret_key: str

    def __init__(self, project_url: str, api_key: str, jwt_secret_key: str):
        self.database = supabase.create_client(project_url, api_key)

        self.jwt_secret_key = jwt_secret_key

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

    def create_user(self, username, password, numfamily):
        existing_account = (
            supabase_api.database.table("profiles")
            .select("id")
            .eq("username", username)
            .execute()
            .data
        )
        print(existing_account)

        if existing_account:
            raise Exception("An account already exists with this username.")

        hashed_password = self.hash_password(password)
        supabase_api.insert(
            "profiles",
            {
                "username": username,
                "password": hashed_password,
                "family_members": numfamily,
            },
        )

    def add_token(self, username, token, expiration):
        supabase_api.insert(
            "tokens", {"token": token, "profile": username, "expiry": expiration}
        )

    def add_recipe(
        self,
        recipeName,
        ingredientList,
        imageURL,
        portionMultiplier,
        recipeURL,
        username,
    ):
        supabase_api.insert(
            "recipes",
            {
                "recipeName": recipeName,
                "ingredientList": ingredientList,
                "imageURL": imageURL,
                "portionMultiplier": portionMultiplier,
                "recipeURL": recipeURL,
                "username": username,
            },
        )

    def update_cell(self, table, changecol, changeval, querycol, queryval):
        response = (
            supabase_api.database.table(table)
            .update({changecol: changeval})
            .eq(querycol, queryval)
            .execute()
        )

        return response

    def hash_password(self, password):
        return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    def check_password(self, password, hashed_password):
        return bcrypt.checkpw(password.encode("utf-8"), hashed_password.encode("utf-8"))

    def create_jwt_token(self, user_id):
        expiration = datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        payload = {"user_id": user_id, "exp": expiration}
        token = jwt.encode(payload, self.jwt_secret_key, algorithm="HS256")
        return token, expiration

    def verify_token(self, token):
        try:
            decoded = jwt.decode(token, self.jwt_secret_key, algorithms=["HS256"])
            return decoded["user_id"]
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None


if __name__ == "__main__":
    import load_env

    project_url: str = os.environ["SUPABASE_PROJECT_URL"]
    api_key: str = os.environ["SUPABASE_API_KEY"]
    jwt_secret_key: str = os.environ["JWT_SECRET_KEY"]

    supabase_api = SupabaseAPI(project_url, api_key, jwt_secret_key)

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
            "username": "daniel",
            "password": "password123",
            "family_members": 20,
            "id": max_id + 1,
        },
    )
