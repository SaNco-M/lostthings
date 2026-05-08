from models.items import ItemAd
from models.animals import PetAd
from models.base import Ad


class User:
    """Хранит информацию о юзере и создает/получает объявление"""

    def __init__(self, user_id: int, name: str, contact_info: str):
        self.user_id = user_id
        self.name = name
        self.contact_info = contact_info
        self.__my_ads = []

    def __getitem__(self, index: int) -> Ad:
        return self.__my_ads[index]

    def __len__(self) -> int:
        return len(self.__my_ads)

    def __add__(self, other):
        if not isinstance(other, Ad):
            raise TypeError('Правый элемент должен быть объявлением')

        self.__my_ads.append(other)
        return self

    def create_ad(self, ad_class, **kwargs) -> None:
        if ad_class == PetAd:
            required = ["category", "color", "breed", "pet_name"]
            missing = []
            for i in required:
                if i not in kwargs:
                    missing.append(i)
            if missing:
                raise ValueError("Вы ввели неправильные данные")
            else:
                new_ad = ad_class(author=self.name, **kwargs)
                self.__my_ads.append(new_ad)


        elif ad_class == ItemAd:
            required = ["category", "color", "value"]
            missing = []
            for i in required:
                if i not in kwargs:
                    missing.append(i)
            if missing:
                raise ValueError("Вы ввели неправильные данные")
            else:
                new_ad = ad_class(author=self.name, **kwargs)
                self.__my_ads.append(new_ad)

    def get_ads(self):
        return self.__my_ads


class Admin(User):
    def __init__(self, user_id: int, name: str, contact_info: str):
        super().__init__(user_id, name, contact_info)
        self.role = "System Admin"

    def moderate_ad(self, ad: Ad) -> None:
        ad.verify()
        ad.publish()
