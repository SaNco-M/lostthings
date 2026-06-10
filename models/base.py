from config import AD_LIMIT, DEFAULT_STATUS


class Ad:
    """Хранит и выводит информацию об объявлении"""
    total_ads = 0
    __slots__ = (
        'author', 'category', 'color', '__is_verified', '__status', 'metadata'
    )

    def __init__(self, author: str, category: str, color: str, **kwargs):
        self.author = author
        self.category = category
        self.color = color
        self.__is_verified = False
        self.__status = DEFAULT_STATUS
        self.metadata = kwargs

        if Ad.total_ads >= AD_LIMIT:
            raise ValueError("Вы создали слишком много объявлений")

        Ad.total_ads += 1

    def __str__(self):
        return (
            f"Описание:"
            f" {self.category},"
            f" {self.color}"
            f" (Автор: {self.author})"
        )

    @property
    def status(self):
        return self.__status

    def verify(self):
        self.__is_verified = True

    def publish(self):
        if not self.__is_verified:
            raise ValueError("Объявление не проверено")
        self.__status = "published"

    def get_search_text(self):
        return f"{self.category} {self.color} {self.author}"

    def match(self, other_ad: 'Ad') -> bool:
        """Ищет совпадения по категории"""
        return self.category == other_ad.category
