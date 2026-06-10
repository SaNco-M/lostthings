from models.base import Ad


class PetAd(Ad):
    """Хранит информацию о животных"""
    __slots__ = (
        'breed', 'pet_name'
    )

    def __init__(self, author: str, category: str, color: str, breed: str, pet_name: str, **kwargs):
        super().__init__(author, category, color, **kwargs)
        self.breed = breed
        self.pet_name = pet_name

    def __str__(self) -> str:
        if self.metadata:
            extra_info = ', '.join(f'{k}={v}' for k, v in self.metadata.items())

            return (
                f"[Животное] Категория: {self.category},"
                f" Кличка: {self.pet_name},"
                f" Порода: {self.breed},"
                f" Доп. Инф: {extra_info}"
            )

        else:
            return (
                f"[Животное] Категория: {self.category},"
                f" Кличка: {self.pet_name},"
                f" Порода: {self.breed},"
            )

    def get_search_text(self):
        return f"{self.category} {self.color} {self.breed} {self.pet_name}"

    def match(self, other_ad: 'Ad') -> bool:
        """Ищет совпадения по категории и породе"""
        if not super().match(other_ad):
            return False

        other_breed = getattr(other_ad, 'breed', None)
        return self.breed == other_breed
