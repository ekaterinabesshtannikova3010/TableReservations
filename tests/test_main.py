import pytest
from httpx import AsyncClient
from main import app  # Ваш FastAPI приложение

@pytest.mark.asyncio
async def test_create_table():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.post("/tables/", json={"name": "Table 1", "seats": 4, "location": "зал у окна"})
        assert response.status_code == 201
        assert response.json()["name"] == "Table 1"

@pytest.mark.asyncio
async def test_get_tables():
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/tables/")
        assert response.status_code == 200
        assert isinstance(response.json(), list)

@pytest.mark.asyncio
async def test_delete_table():
    async with AsyncClient(app=app, base_url="http://test") as client:
        # Сначала создаем столик
        create_response = await client.post("/tables/", json={"name": "Table 2", "seats": 2, "location": "терраса"})
        table_id = create_response.json()["id"]

        # Теперь удаляем его
        delete_response = await client.delete(f"/tables/{table_id}")
        assert delete_response.status_code == 204

        # Проверяем, что столик удален
        get_response = await client.get(f"/tables/{table_id}")
        assert get_response.status_code == 404

@pytest.mark.asyncio
async def test_create_reservation():
    async with AsyncClient(app=app, base_url="http://test") as client:
        # Сначала создаем столик
        table_response = await client.post("/tables/", json={"name": "Table 3", "seats": 4, "location": "зал у окна"})
        table_id = table_response.json()["id"]

        # Создаем бронь
        reservation_response = await client.post("/reservations/", json={
            "customer_name": "John Doe",
            "table_id": table_id,
            "reservation_time": "2023-10-01T18:00:00",
            "duration_minutes": 60
        })
        assert reservation_response.status_code == 201
        assert reservation_response.json()["customer_name"] == "John Doe"

@pytest.mark.asyncio
async def test_conflict_reservation():
    async with AsyncClient(app=app, base_url="http://test") as client:
        # Сначала создаем столик
        table_response = await client.post("/tables/", json={"name": "Table 4", "seats": 4, "location": "терраса"})
        table_id = table_response.json()["id"]

        # Создаем первую бронь
        await client.post("/reservations/", json={
            "customer_name": "Alice",
            "table_id": table_id,
            "reservation_time": "2023-10-01T19:00:00",
            "duration_minutes": 60
        })

        # Пытаемся создать конфликтующую бронь
        conflict_response = await client.post("/reservations/", json={
            "customer_name": "Bob",
            "table_id": table_id,
            "reservation_time": "2023-10-01T19:30:00",
            "duration_minutes": 30
        })
        assert conflict_response.status_code == 400  # Ожидаем ошибку конфликта

@pytest.mark.asyncio
async def test_delete_reservation():
    async with AsyncClient(app=app, base_url="http://test") as client:
        # Сначала создаем столик и бронь
        table_response = await client.post("/tables/", json={"name": "Table 5", "seats": 4, "location": "зал у окна"})
        table_id = table_response.json()["id"]

        reservation_response = await client.post("/reservations/", json={
            "customer_name": "Charlie",
            "table_id": table_id,
            "reservation_time": "2023-10-01T20:00:00",
            "duration_minutes": 60
        })
        reservation_id = reservation_response.json()["id"]

        # Удаляем бронь
        delete_response = await client.delete(f"/reservations/{reservation_id}")
        assert delete_response.status_code == 204

        # Проверяем, что бронь удалена
        get_response = await client.get(f"/reservations/{reservation_id}")
        assert get_response.status_code == 404
