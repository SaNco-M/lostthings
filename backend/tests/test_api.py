from backend.app.models import PetAdModel, UserModel


async def test_search_ads_simple(client):
    response = await client.get("/search")

    assert response.status_code == 200

    data = response.json()

    assert isinstance(data, list)


async def test_create_ad(client, db_session):
    test_user = UserModel(name="TestUser", contact_info="@test_user")
    db_session.add(test_user)
    await db_session.commit()

    response = await client.post(
        "/ads",
        json={
            "user_id": test_user.id,
            "category": "Кошка",
            "color": "Черный",
            "ad_type": "pet",
            "breed": "Сибирская"

        }
    )

    assert response.status_code == 200

    data = response.json()

    db_ad = await db_session.get(PetAdModel, data["id"])

    assert data["category"] == "Кошка"
    assert data["color"] == "Черный"
    assert db_ad.breed == "Сибирская"

