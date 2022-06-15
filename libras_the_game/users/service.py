# Pip imports
from werkzeug.security import check_password_hash, generate_password_hash

# Internal imports
from libras_the_game.common.errors import InvalidCredentialsError
from libras_the_game.users.models import User
from libras_the_game.users.repository import UsersRepository


def does_user_exist(email: str) -> bool:
    repository = UsersRepository()
    return repository.find_one_by({"email": email}) is not None


def create_user(user: User) -> User:
    if does_user_exist(user.email):
        return False

    repository = UsersRepository()
    user.password = generate_password_hash(user.password)
    repository.save(user)
    return user


def get_user(email: str, password: str) -> User:
    repository = UsersRepository()
    user = repository.find_one_by({"email": email})
    if not user:
        raise InvalidCredentialsError

    if not check_password_hash(user.password, password):
        raise InvalidCredentialsError

    return user


def get_user_by_id(id: str) -> User:
    repository = UsersRepository()
    return repository.find_one_by_id(id)
