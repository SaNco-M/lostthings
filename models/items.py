from models.base import Ad


class ItemAd(Ad):
    """Хранит информацию о вещах"""
    def __init__(self, author, category, color, value):
        super().__init__(author, category, color)
        self.value = value

    def __str__(self):
        return f"[Вещь] Категория: {self.category}, Цвет: {self.color}, Примерная стоимость: {self.value}"

    def get_search_text(self):
        return f"{self.category} {self.color} {self.value}"

    def match(self, other_ad: 'Ad') -> bool:
        """Ищет совпадения по категории и цене +- 20%"""
        if not super().match(other_ad):
            return False

        other_value = getattr(other_ad, 'value', None)
        if other_value is None:
            return False
        return 0.8 * other_value <= self.value <= 1.2 * other_value