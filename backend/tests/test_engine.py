import pytest
from backend.app.core.engine import LostAndFound
from backend.app.exceptions.errors import IdError
from backend.app.models import Ad
from models.animals import PetAd
from models.items import ItemAd


@pytest.fixture
def system_with_users():
    system = LostAndFound()
    user1 = system.register_user(1, "Ivan", "TG: @asd")
    user2 = system.register_user(2, "Petya", "@VKgh")
    return system, user1, user2


def test_error(system_with_users):
    system, user1, user2 = system_with_users
    with pytest.raises(IdError):
        system.register_user(1, "Anna", "LAD+")


def test_match(system_with_users):
    system, user1, user2 = system_with_users
    system.post_ad_to_user(
        1,
        ad_class=PetAd,
        category="Кошка",
        breed="Сибирская",
        color="Серая",
        pet_name="Мурка",
    )
    system.bulk_publish(1)

    lost_ad = PetAd("Иван", "Кошка", "Черная", "Сибирская", "Башмак")
    assert len(system(lost_ad)) == 1


@pytest.mark.parametrize("invalid_contact", ["простотекст", "", "12345"])
def test_parametrize(system_with_users, invalid_contact):
    system, user1, user2 = system_with_users
    with pytest.raises(ValueError):
        system.register_user(3, "Bad name", invalid_contact)


lo_ad = PetAd(
    author="Alex", category="Кошка", color="Серая", breed="Сибирская", pet_name="Мурка"
)
fir_ad = PetAd(
    author="Bob", category="Кошка", color="Черная", breed="Сибирская", pet_name="Багира"
)
sec_ad = PetAd(
    author="Bob", category="Кошка", color="Серая", breed="Сфинкс", pet_name="Лысый"
)
th_ad = ItemAd(author="Bob", category="Ключ", color="Серый", value=500)


@pytest.fixture(autouse=True)
def clean_ad():
    Ad.total_ads = 0


@pytest.mark.parametrize(
    "lost_ad, found_ad, expected_result",
    [
        (lo_ad, fir_ad, True),
        (lo_ad, sec_ad, False),
        (lo_ad, th_ad, False),
    ],
)
def test_ad_matching(lost_ad, found_ad, expected_result):
    assert lost_ad.match(found_ad) == expected_result
