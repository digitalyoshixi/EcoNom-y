import os
import supabase
import datetime
import bcrypt
import jwt


class SupabaseAPI:
    database: supabase.Client
    jwt_secret_key: str

    def __init__(self, project_url: str, api_key: str, jwt_secret_key: str) -> None:
        self.database = supabase.create_client(project_url, api_key)

        self.jwt_secret_key = jwt_secret_key

    def select(self, table, columns):
        return self.database.table(table).select(columns).execute()

    def selectspecific(self, table, columns, eqcol, eqval):
        return (
            self.database.table(table)
            .select(columns)
            .eq(eqcol, eqval)
            .execute()
        )

    def insert(self, table, keymap):
        self.database.table(table).insert(keymap).execute()

    def add_user(self, username, password, numfamily):
        result = (
            self.database.table("profiles")
            .select("id")
            .order("id", desc=True)
            .limit(1)
            .execute()
        )
        max_id = result.data[0]["id"] if result.data else 0
        self.insert(
            "profiles",
            {
                "profile": username,
                "password": self.hash_password(password),
                "family_members": numfamily,
                "id": max_id + 1,
            },
        )

    def add_token(self, username, token, expiration):
        self.insert(
            "tokens", {"token": token,
                       "profile": username, "expiry": expiration}
        )

    def add_recipe(self, recipeName, ingredientList, imageURL, portionMultiplier, recipeURL):
        self.insert(
            "recipes",
            {
                "recipeName": recipeName,
                "ingredientList": ingredientList,
                "imageURL": imageURL,
                "portionMultiplier": portionMultiplier,
                "recipeURL": recipeURL,
            },
        )

    def hash_password(self, password):
        return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, password, hashed_password):
        return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

    def create_jwt_token(self, user_id):
        expiration = str(datetime.datetime.utcnow() +
                         datetime.timedelta(hours=1))
        payload = {"user_id": user_id, "exp": expiration}
        token = jwt.encode(
            payload, self.jwt_secret_key, algorithm="HS256")
        return token, expiration

    def verify_token(self, token):
        try:
            decoded = jwt.decode(
                token, self.jwt_secret_key, algorithms=["HS256"])
            return decoded["user_id"]
        except jwt.ExpiredSignatureError:
            return None
        except jwt.InvalidTokenError:
            return None


supabase_api = None


def get_supabase_api():
    global supabase_api
    if supabase_api is None:
        project_url = os.environ["SUPABASE_PROJECT_URL"]
        api_key = os.environ["SUPABASE_API_KEY"]
        jwt_secret_key = os.environ["JWT_SECRET_KEY"]
        supabase_api = SupabaseAPI(project_url, api_key, jwt_secret_key)

    return supabase_api
