from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_run_python_code():
    response = client.post("/run", json={
        "language": "python",
        "code": "print('Hi')",
        "stdin": ""
    })
    assert response.status_code == 200
    assert "Hi" in response.json()["output"]

def test_save_and_get_code():
    code_data = {
        "language": "python",
        "code": "print('Saved code')"
    }
    save_response = client.post("/save", json=code_data)
    assert save_response.status_code == 200
    code_id = save_response.json()["code_id"]

    get_response = client.get(f"/code/{code_id}")
    assert get_response.status_code == 200
    assert get_response.json()["code"] == "print('Saved code')"

def test_ai_hint():
    response = client.post("/ai/hint", json={
        "language": "python",
        "code": "print('hello')"
    })
    assert response.status_code == 200
    assert "hint" in response.json()
