from api import api
from typing import List
from typing import Dict


async def load_users_info(users: List[int], fields: List[str]) -> List[Dict]:
    # Подготавливаем
    user_ids = ','.join(list(map(str, users)))
    user_fields = ','.join(fields)

    # Отправляем запрос
    info = await api.users.get(user_ids, user_fields)

    return [inf.dict() for inf in info]


def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]
