import textwrap


def profile_workers(work):
    """
    param: текст для профиля воркера
    return: возращает текст воркера
    """

    return textwrap.dedent(f'''
            🔰id worker: {work.worker_id}\n
            🏡имя worker: {work.worker_name}\n
            📗описание worker: {work.worker_description}\n\n
            🚀уровень worker: {work.worker_status}\n
            💲баланс worker: {work.worker_balance}\n
            📌рейтинг worker: {work.worker_rate}'''
            )


def open_task(task):
    """
    param: текст для открытия задачи
    return: возращает текст открытия задачи
    """

    return textwrap.dedent(f'''
            📌Вы хотите взять задание {task.task_id}?\n\n
            📗Мин. тз: {task.min_tz}\n
            📙Полное тз: {task.max_tz}\n
            💲Цена: {task.price}'''
            )


def open_task_user(task, work):
    """
    param: текст для открытия задачи
    return: возращает текст открытия задачи
    """

    return textwrap.dedent(f'''
            📌Ваше задание взял: {work.worker_name}!\n\n
            📗Рейтинг исполнителя: {work.worker_rate}\n
            📙Описание исполнителя: {task.max_tz}'''
            )

def new_application(tasks, data, user_id):
    """
    param: текст для новой заявки
    param: tasks
    param: data
    param: user_id
    return: возвращает текст нового заявки
    """

    return textwrap.dedent(f'''
            📝 Новая заявка! 📝\n\n
            📋 Задание № {tasks.task_id}\n
            👤 Заказчик: {user_id}\n\n
            🏷️ Категория: {data["task_1"]}\n
            🏢 Подразделение: {data["task_2"]}\n
            📄 Минимальное описание: {data["min_tz"]}\n
            📄 Максимальное описание: {data["max_tz"]}\n\n
            💰 Цена: {data["price"]}'''
            )


def channel_task(task):
    """
    param: текст для канала заданий
    param: task
    return: возвращает текст канала заданий
    """

    return textwrap.dedent(f"""
        <b>💎Новое задание💎</b>\n\n
        <b>📝Категория: {task.category}</b>\n
        <b>📘Мин. тз</b>: {task.min_tz}\n
        <b>📒Полное тз</b>: {task.max_tz}\n
        <b>🔰Цена заказа</b>: {task.price}
        {str(task.task_id)}"""
    )


def desc_mytask(task):
    """
    param: текст для описания моего задания
    param: task
    return: возвращает текст описания моего задания
    """

    return textwrap.dedent(f"""
        <b>🔰Статус задания</b>: {task.status}\n\n
        <b>📝Категория: {task.category}</b>\n
        <b>📝Под-категория</b>: {task.podcategory}\n\n
        <b>📘Мин. тз</b>: {task.min_tz}\n
        <b>📒Полное тз</b>: {task.max_tz}\n\n
        <b>🔰Цена заказа</b>: {task.price}\n
        <b>📅Дата заказа</b>: {task.time}\n\n
        <b>💎Исполнитель:</b> {task.worker_id_task}\n"""
    )


def desc_mytask_worker(task):
    """
    param: текст для описания моего задания
    param: task
    return: возвращает текст описания моего задания
    """

    return textwrap.dedent(f"""
        <b>🔰Статус задания</b>: {task.status}\n\n
        <b>📝Категория: {task.category}</b>\n
        <b>📝Под-категория</b>: {task.podcategory}\n\n
        <b>📘Мин. тз</b>: {task.min_tz}\n
        <b>📒Полное тз</b>: {task.max_tz}\n\n
        <b>🔰Цена заказа</b>: {task.price}\n
        <b>📅Дата заказа</b>: {task.time}\n\n
        <b>💎Заказчик:</b> {task.user_id_task}\n"""
    )
