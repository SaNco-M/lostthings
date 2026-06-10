from models.items import ItemAd
from models.animals import PetAd
from models.base import Ad


class User:
    """Хранит информацию о юзере и создает/получает объявление"""
    __slots__ = (
        'user_id', 'name', '_contact_info', '__my_ads'
    )

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

    @property
    def contact_info(self):
        return self._contact_info

    @contact_info.setter
    def contact_info(self, person_info: str) -> None:
        if "@" not in person_info and "+" not in person_info:
            raise ValueError("Добавьте + или @")
        self._contact_info = person_info

    def create_ad(self, ad_class, **kwargs) -> None:
        new_ad = ad_class(author=self.name, **kwargs)
        self.__my_ads.append(new_ad)

    def get_ads(self):
        return self.__my_ads


class Admin(User):
    def __init__(self, user_id: int, name: str, contact_info: str):
        super().__init__(user_id, name, contact_info)
        self.role = "Admin"

    def moderate_ad(self, ad: Ad) -> None:
        ad.verify()
        ad.publish()
