from core.engine import LostAndFound
from exceptions.errors import IdError
from models.animals import PetAd
from models.items import ItemAd
from models.users import User


def main():
    system = LostAndFound()

    # -------------------
    # Регистрация users
    # -------------------
    try:
        system.register_user(1, "Alex", "tg:@alex")
        system.register_user(2, "Bob", "tg:@bob")
        system.register_user(3, "Kate", "tg:@kate")
    except IdError:
        print("Ошибка регистрации пользователя")

    # -------------------
    # Создание объявлений
    # -------------------
    try:
        system.post_ad_to_user(
            2,
            ad_class=PetAd,
            category="Собака",
            breed="Овчарка",
            color="Черный",
            pet_name="Бобик",
            reward=5000
        )

        system.post_ad_to_user(
            1,
            ad_class=PetAd,
            category="Кошка",
            breed="Сибирская",
            color="Серая",
            pet_name="Мурка"
        )

        system.post_ad_to_user(
            3,
            ad_class=ItemAd,
            category="Ключ",
            color="Серый",
            value=100
        )

    except IdError:
        print("Ошибка создания объявления")

    # -------------------
    # Демонстрация + (User + Ad)
    # -------------------
    tom = User(4, "Том", "ВК@gas")
    ad_tom = PetAd("Том", "Собака", "Желтый", "хаски", "Бобик")

    tom + ad_tom
    print("Объявления Тома:", tom.get_ads())

    # -------------------
    # Модерация
    # -------------------
    system.verify_user_ad(1, 0)
    system.verify_user_ad(2, 0)
    system.verify_user_ad(3, 0)

    # -------------------
    # Публикация
    # -------------------
    system.bulk_publish(1)
    system.bulk_publish(2)
    system.bulk_publish(3)

    # -------------------
    # Статистика
    # -------------------
    print("Статистика:", system.get_system_stats())

    # -------------------
    # Итерация (__iter__)
    # -------------------
    print("\nВсе объявления в системе:")
    print(*(ad for ad in system), sep="\n")

    # -------------------
    # Поиск через __call__
    # -------------------
    lost_cat = PetAd("Кошка", "Кошка", "Серая", "Сибирская", "Савок")
    print("\nСовпадения для потерянной кошки:")
    print(system(lost_cat))


if __name__ == "__main__":
    main()