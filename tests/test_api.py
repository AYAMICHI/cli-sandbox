from fastapi.testclient import TestClient
from cli_sandbox.main_api import app

client = TestClient(app)

def test_greet_api():
    response = client.get("/greet", params={"name": "太郎", "repeat": 2})
    assert response.status_code == 200
    data = response.json()
    assert data["messages"] == [
        "こんにちは, 太郎さん！",
        "こんにちは, 太郎さん！"
    ]