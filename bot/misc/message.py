import textwrap

def main_text():
    """
    Возвращает текст главного меню.
    """
    return textwrap.dedent('''
        Приветствуем вас в главном меню нашего бота, центра выполнения заказов от заказчиков в сфере программирования – <b>🏡WorkHouse!</b>\n\n
        🚀Здесь вы можете как создать свой индивидуальный заказ, который будет выполнен опытными кодерами из нашего проекта, так и устроиться в команду кодеров, успешно прошедших собеседование.\n\n
        📌Выберите интересующий вас раздел, чтобы начать свой путь в мире разработки и реализации идей вместе с нами!
    ''')

def profile_workers(work, ts_1, ts_2):
    """
    param: текст для профиля воркера
    return: возращает текст воркера
    """

    return textwrap.dedent(f'''
            <b>🔰telegram id:</b> {work.worker_id}\n
            <b>🏡имя:</b> {work.worker_name}\n
            <b>📗описание:</b> {work.worker_description}\n\n
            <b>🚀уровень:</b> {work.worker_status}\n
            <b>💲баланс:</b> {work.worker_balance}\n
            <b>📌рейтинг:</b> {work.worker_rate}\n
            <b>Активных заказов:</b> {ts_1}\n
            <b>Выполненных заказов:</b> {ts_2}
            '''
            )

def profile_user(user, task_1, task_2):
    """
    param: текст для профиля юзера
    return: возращает текст юзера
    """

    return textwrap.dedent(f'''
            <b>🔰telegram id:</b> {user.user_id}\n
            <b>🏡имя:</b> {user.username}\n
            <b>💲баланс:</b> {user.balance}\n
            <b>Активных заказов:</b> {task_1}\n
            <b>Выполненных заказов:</b> {task_2}
            '''
            )


def open_task(task):
    """
    param: текст для открытия задачи
    return: возращает текст открытия задачи
    """

    return textwrap.dedent(f'''
            <b>📌Вы хотите взять задание</b> {task.task_id}?\n\n
            📗Мин. тз: {task.min_tz}\n
            📙Полное тз: {task.max_tz}\n
            💲Цена: {task.price}
            '''
            )


def open_task_user(task, work):
    """
    param: текст для открытия задачи
    return: возращает текст открытия задачи
    """

    return textwrap.dedent(f'''
            📌Ваше задание взял: {work.worker_name}!\n\n
            📗Рейтинг исполнителя: {work.worker_rate}\n
            📙Описание исполнителя: {task.max_tz}
            '''
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
            📝 Новая заявка! 📝\n
            📋 Задание № {tasks.task_id}\n
            👤 Заказчик: {user_id}\n\n
            🏷️ Категория: {data["task_1"]}\n
            🏢 Под-категория: {data["task_2"]}\n
            📄 Минимальное описание: {data["min_tz"]}\n
            📄 Максимальное описание: {data["max_tz"]}\n\n
            💰 Цена: {data["price"]}
            '''
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
        <b>🔰Цена заказа</b>: {task.price}"""
    )


def desc_mytask(task):
    """
    param: текст для описания моего задания
    param: task
    return: возвращает текст описания моего задания
    """
    data = task.time
    data = data.split("|")
    return textwrap.dedent(f"""
        <b>🔰Статус задания</b>: {task.status}\n
        <b>📝Категория: {task.category}</b>\n
        <b>📝Под-категория</b>: {task.podcategory}\n
        <b>📘Мин. тз</b>: {task.min_tz}\n
        <b>📒Полное тз</b>: {task.max_tz}\n
        <b>🔰Цена заказа</b>: {task.price}\n
        <b>📅Дата заказа</b>: {data[0]}\n
        <b>📅Время заказа</b>: {data[1]}\n
        <b>💎Исполнитель:</b> {task.user_id_task}"""
    )


def desc_mytask_worker(task):
    """
    param: текст для описания моего задания
    param: task
    return: возвращает текст описания моего задания
    """
    data: list = task.time.split("|")
    return textwrap.dedent(f"""
        <b>🔰Статус задания</b>: {task.status}\n
        <b>📝Категория: {task.category}</b>\n
        <b>📝Под-категория</b>: {task.podcategory}\n
        <b>📘Мин. тз</b>: {task.min_tz}\n
        <b>📒Полное тз</b>: {task.max_tz}\n
        <b>🔰Цена заказа</b>: {task.price}\n
        <b>📅Дата заказа</b>: {data[0]}\n
        <b>📅Время заказа</b>: {data[1]}\n
        <b>💎Заказчик:</b> {task.user_id_task}"""
    )
