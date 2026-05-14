import uuid
from contextvars import ContextVar
from typing import Optional

request_id_var: ContextVar[Optional[str]] = ContextVar('request_id', default=None)
user_id_var: ContextVar[Optional[str]] = ContextVar('user_id', default=None)
account_id_var: ContextVar[Optional[str]] = ContextVar('account_id', default=None)


def generate_request_id() -> str:
    return str(uuid.uuid4())


def set_request_id(request_id: Optional[str] = None) -> str:
    if request_id is None:
        request_id = generate_request_id()
    request_id_var.set(request_id)
    return request_id


def get_request_id() -> Optional[str]:
    return request_id_var.get()


def set_user_id(user_id: str) -> None:
    user_id_var.set(user_id)


def get_user_id() -> Optional[str]:
    return user_id_var.get()


def set_account_id(account_id: str) -> None:
    account_id_var.set(account_id)


def get_account_id() -> Optional[str]:
    return account_id_var.get()


def clear_context() -> None:
    request_id_var.set(None)
    user_id_var.set(None)
    account_id_var.set(None)
