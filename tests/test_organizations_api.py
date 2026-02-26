HEADERS = {"X-API-Key": "API_SECRET_KEY"}


def test_get_by_id(client):
    response = client.get("/organizations/by-id/1", headers=HEADERS)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert "name" in data


def test_get_by_name_partial_match(client):
    response = client.get("/organizations/by-name/ООО", headers=HEADERS)
    assert response.status_code == 200
    items = response.json()
    assert len(items) >= 1
    assert any("ООО" in org["name"] for org in items)


def test_get_by_activity_tree(client):
    response = client.get("/organizations/by-activity/Автомобили", headers=HEADERS)
    assert response.status_code == 200
    items = response.json()
    assert len(items) >= 1


def test_get_in_radius(client):
    response = client.get(
        "/organizations/in-radius/55.5833/38.1788/1.0", headers=HEADERS
    )
    assert response.status_code == 200
    items = response.json()
    assert len(items) >= 1


def test_get_by_building_address(client):
    response = client.get(
        "/organizations/by-building-address/Москва, ул. Блюхера, д. 16",
        headers=HEADERS,
    )
    assert response.status_code == 200
    data = response.json()
    assert data["building"]["address"] == "Москва, ул. Блюхера, д. 16"


def test_get_by_id_not_found(client):
    response = client.get("/organizations/by-id/9999", headers=HEADERS)
    assert response.status_code == 404

