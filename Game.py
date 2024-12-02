import random
import time
import threading


# Функция для обратного отсчета времени
def count_down(t, event):
    while t > 0:
        if event.is_set():
            return  # Если ответ дан, выходим из функции
        mins, secs = divmod(t, 60)
        timer = '{:02d}:{:02d}'.format(mins, secs)
        print(f'\rОсталось времени: {timer}', end="")
        time.sleep(1)
        t -= 1
    event.set()  # Устанавливаем событие, если время истекло


# Функция для разгадывания загадки
def solve_riddle():
    while True:
        print("Разгадайте загадку, чтобы получить ключ.")
        print("Что не имеет длины, глубины, ширины, высоты, а можно измерить?")
        answer = input("Ваш ответ: ").strip().lower()
        if answer == "температура":
            print("Вы разгадали загадку и получили ключ!")
            return True
        else:
            print("Неправильный ответ, попробуйте снова.")


# Функция для визуализации здоровья персонажа
def visual_health(hero_hp, goblin_hp):
    print(f"\nВаше здоровье: {hero_hp}HP | Здоровье гоблина: {goblin_hp}HP")


# Функция для вывода информации о боях
def log_battle_info(hero_hp, goblin_hp, damage_done, damage_received):
    print(f"В этом бою вы нанесли {damage_done} урона гоблину и получили {damage_received} урона.")


# Функция для загадок после победы над гоблином
def ghost_riddles():
    riddles = [
        {
            "question": "Сколько месяцев в году имеют 28 дней?",
            "answer": "все"
        },
        {
            "question": "Собака была привязана к десятиметровой веревке, а прошла по прямой двести метров. Как ей это удалось?",
            "answer": "веревка не была ни к чему не привязана"
        },
        {
            "question": "Что можно видеть с закрытыми глазами?",
            "answer": "сны"
        }
    ]

    for riddle in riddles:
        while True:
            print(f"\nЗагадка от призрака: {riddle['question']}")
            answer = input("Ваш ответ: ").strip().lower()
            if answer == riddle['answer']:
                print("Вы разгадали загадку!")
                break
            else:
                print("Неправильный ответ, попробуйте снова.")


# Функция для боя с гоблином
def fight_goblin():
    hero_hp = 100
    goblin_hp = 100
    time_limit = 10  # секунд

    while hero_hp > 0 and goblin_hp > 0:
        visual_health(hero_hp, goblin_hp)  # Визуализация здоровья

        # Генерация задачи
        num1 = random.randint(1, 10)
        num2 = random.randint(1, 10)
        correct_answer = num1 + num2

        print(f"Решите задачу: {num1} + {num2} = ? (У вас есть {time_limit} секунд)")

        event = threading.Event()  # Событие, чтобы проверить, получен ли ответ
        timer_thread = threading.Thread(target=count_down, args=(time_limit, event))
        timer_thread.start()

        # Получение ответа от пользователя
        try:
            user_answer = int(input())
            event.set()  # Если ответ дан, устанавливаем событие
        except ValueError:
            user_answer = None
            event.set()  # Устанавливаем событие, чтобы остановить таймер

        # Проверяем, истекло ли время
        damage_done = 0
        damage_received = 0

        if timer_thread.is_alive() and user_answer is not None:
            if user_answer == correct_answer:
                damage_done = random.randint(10, 80)
                goblin_hp -= damage_done
                print(f"Вы правильно ответили! Наносите гоблину {damage_done} урона.")
            else:
                damage_received = random.randint(10, 80)
                hero_hp -= damage_received
                print(f"Неправильный ответ! Гоблин наносит вам {damage_received} урона.")
        else:
            # Время истекло
            damage_received = random.randint(10, 80)
            hero_hp -= damage_received
            print(f"\nВремя истекло! Гоблин наносит вам {damage_received} урона.")

        # Логирование информации о бою
        log_battle_info(hero_hp, goblin_hp, damage_done, damage_received)

        # Завершение таймера, если он еще работает
        if timer_thread.is_alive():
            timer_thread.join(timeout=0)  # Ждем завершения потока

    if hero_hp <= 0:
        print("Вы проиграли! Гоблин победил.")
    else:
        print("Вы победили гоблина и прошли дальше!")
        ghost_riddles()  # Встреча с призраком и решение загадок

# Функция для приветствия игрока
def greet_player():
    print("Добро пожаловать в игрулю где надо думать!")
    print(" В каждой комнате вам нужно решить задачу, чтобы продвинуться дальше.")

# Функция для окончания игры
def end_game():
    print("Спасибо за игру! До новых встреч!")
    exit()

def game_loop():
    greet_player()  # Приветствие игрока
    if solve_riddle():
        fight_goblin()
    end_game()  # Завершение игры

if __name__ == "__main__":
    game_loop()
