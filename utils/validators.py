from models.base import Ad
from core.engine import LostAndFound


class SystemValidator:
    """Проверка работы системы"""

    def __init__(self, system: LostAndFound):
        self.system = system

    def run_diagnostic(self):
        report = []

        count_ads = sum(len(user.get_ads()) for user in self.system.get_list_users())

        if Ad.total_ads == count_ads:
            report.append("1. Проверка лимитов: OK")
        else:
            report.append("1. Проверка лимитов: ОШИБКА")

        try:
            user = self.system.get_list_users()[0]
            self.system.post_ad_to_user(user.user_id, '', '', '')
            report.append("2. Тест дурака: ОШИБКА (пустые данные приняты)")
        except ValueError as e:
            report.append(f"2. Тест дурака: OK ({str(e)})")

        try:
            user = self.system.get_list_users()[0]

            for i in range(10):
                self.system.post_ad_to_user(user.user_id, 'as', 'asd', 'asd')

            report.append("3. Лимит: ОШИБКА (не сработал)")
        except ValueError as e:
            report.append(f"3. Лимит: ОК {str(e)} ")

        user = self.system.get_list_users()[0]
        errors = self.system.bulk_publish(user.user_id)

        if errors:
            report.append(f"4. Массовая публикация: ошибки -> {errors}")
        else:
            report.append("4. Массовая публикация: OK")

        return report
