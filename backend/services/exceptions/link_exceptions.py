class LinkError(Exception):
    """Базовое исключение для всех ошибок с ссылками."""


class InvalidLinkError(LinkError):
    """Ссылка некорректна или отсутствует payload."""


class GroupNotFoundError(LinkError):
    """Группа не найдена или неактивна."""


class AlreadyInGroupError(LinkError):
    """Пользователь уже состоит в группе."""


class GroupJoinError(LinkError):
    """Ошибка при добавлении пользователя в группу."""
