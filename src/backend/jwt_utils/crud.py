from src.backend.jwt_utils import utils as auth_utils
from src.backend.schemas import UserSchema

john = UserSchema(
    username='john',
    password=auth_utils.hash_password('qwerty'),
    email='john@mail.ru',
)
sam = UserSchema(
    username='sam',
    password=auth_utils.hash_password('password'),
)
users_db: dict[str, UserSchema] = {
    john.username: john,
    sam.username: sam,
}
