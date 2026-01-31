from fastapi.testclient import TestClient

from app.main import app


def test_list_factors():
    client = TestClient(app)
    resp = client.get("/factors")
    assert resp.status_code == 200
    data = resp.json()
    names = {item["name"] for item in data}
    assert {"trend", "xsmom", "lowvol"}.issubset(names)
    for item in data:
        assert isinstance(item["params"], list)
