from models.base import Ad


class PetAd(Ad):
    """Хранит информацию о животных"""

    def __init__(self, author: str, category: str, color: str, breed: str, pet_name: str):
        super().__init__(author, category, color)
        self.breed = breed
        self.pet_name = pet_name

    def __str__(self):
        return f"[Животное] Категория: {self.category}, Кличка: {self.pet_name}, Порода: {self.breed}"

    def get_search_text(self):
        return f"{self.category} {self.color} {self.breed} {self.pet_name}"

    def match(self, other_ad: 'Ad') -> bool:
        """Ищет совпадения по категории и породе"""
        if not super().match(other_ad):
            return False

        other_breed = getattr(other_ad, 'breed', None)
        return self.breed == other_breed
