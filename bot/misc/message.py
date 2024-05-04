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

def profile_workers(work, ts_1, ts_2, rating_representation, total_reviews, average_rating):
    """
    param: текст для профиля воркера
    return: возращает текст воркера
    """

    return textwrap.dedent(f'''
            <b>🔮Профиль исполнителя</b>\n
            <b>telegram id:</b> {work.worker_id}\n
            <b>┎имя:</b> {work.worker_name}
            <b>┣уровень:</b> {work.worker_status}
            <b>┣баланс:</b> {work.worker_balance}
            <b>┖рейтинг:</b> {rating_representation} ({average_rating}) ({total_reviews})\n
            <b>описание:</b> {work.worker_description}\n
            <b>┎Активных заказов:</b> {ts_1}
            <b>┖Выполненных заказов:</b> {ts_2}
            '''
            )

def profile_user(user, task_1, task_2):
    """
    param: текст для профиля юзера
    return: возращает текст юзера
    """

    return textwrap.dedent(f'''
            <b>🔮Профиль пользователя</b>\n
            <b>telegram id:</b> {user.user_id}\n
            <b>┎имя:</b> {user.username}
            <b>┖баланс:</b> {user.balance}\n
            <b>┎Активных заказов:</b> {task_1}
            <b>┖Выполненных заказов:</b> {task_2}
            '''
            )


def open_task(task):
    """
    param: текст для открытия задачи
    return: возращает текст открытия задачи
    """

    return textwrap.dedent(f'''
            <b>🔔Вы хотите взять задание</b> {task.task_id}?\n
            📗Мин. тз: {task.min_tz}
            📙Полное тз: {task.max_tz}\n
            💰Цена: {task.price}
            '''
            )



def open_task_user(task, work, rating_representation, total_reviews, average_rating):
    """
    param: текст для открытия задачи
    return: возращает текст открытия задачи
    """

    return textwrap.dedent(f'''
            🔔Ваше задание взял: {work.worker_name}!\n
            📗Рейтинг исполнителя: {average_rating} ({rating_representation}) ({total_reviews})\n
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
            🔔 Новая заявка! 🔔\n
            📋 Задание № {tasks.task_id}\n
            👤 Заказчик: {user_id}\n\n
            🏷️ Категория: {data["task_1"]}
            🏢 Под-категория: {data["task_2"]}\n
            📄 Минимальное описание: {data["min_tz"]}
            📄 Максимальное описание: {data["max_tz"]}\n
            💰 Цена: {data["price"]}
            '''
            )

def new_worker(data):
    """
    param: текст для новой заявки
    param: tasks
    param: data
    param: user_id
    return: возвращает текст нового заявки
    """

    return textwrap.dedent(f'''
            🔔 Новая заявка на воркера! 🔔\n
            📋 СТЕК № {data["selected_skills"]}\n
            👤 Заказчик: {data["username"]}\n\n
            📄 Биография: {data["biograf"]}\n
            📄 Работа с API: {data["despt"]}
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
        <b>📘Мин. тз</b>: {task.min_tz}
        <b>📒Полное тз</b>: {task.max_tz}\n
        <b>💰Цена заказа</b>: {task.price}"""
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
        <b>📝Категория: {task.category}</b>
        <b>📝Под-категория</b>: {task.podcategory}\n
        <b>📘Мин. тз</b>: {task.min_tz}
        <b>📒Полное тз</b>: {task.max_tz}\n
        <b>📅Дата заказа</b>: {data[0]}
        <b>📅Время заказа</b>: {data[1]}\n
        <b>💰Цена заказа</b>: {task.price}\n
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
        <b>📝Категория: {task.category}</b>
        <b>📝Под-категория</b>: {task.podcategory}\n
        <b>📘Мин. тз</b>: {task.min_tz}
        <b>📒Полное тз</b>: {task.max_tz}\n
        <b>📅Дата заказа</b>: {data[0]}
        <b>📅Время заказа</b>: {data[1]}\n
        <b>💰Цена заказа</b>: {task.price}\n
        <b>💎Заказчик:</b> {task.user_id_task}"""
    )



def menu_group_text():
    """
    param: текст для меню группы
    return: возвращает текст меню группы
    """
    return textwrap.dedent(f"""
                <b>📝Меню группы</b>\n
                Команды:
                /edit_price [ваша новая цена] - чтобы изменить цену нужно чтобы два участника сделки указали одинаковую цену
                                
                """)
        