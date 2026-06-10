from models.base import Ad


class ItemAd(Ad):
    """Хранит информацию о вещах"""
    __slots__ = (
        'value', 
    )

    def __init__(self, author: str, category: str, color: str, value: int, **kwargs):
        super().__init__(author, category, color, **kwargs)
        self.value = value

    def __str__(self):
        if self.metadata:
            extra_info = ', '.join(f'{k}={v}' for k, v in self.metadata.items())

            return (
                f"[Вещь] Категория: {self.category},"
                f" Цвет: {self.color},"
                f" Примерная стоимость: {self.value}"
                f" Доп. Инф: {extra_info}"
            )

        else:
            return (
                f"[Вещь] Категория: {self.category},"
                f" Цвет: {self.color},"
                f" Примерная стоимость: {self.value}"
            )

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
