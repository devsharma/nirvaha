import requests

BASE_URL = "http://localhost:5050"  # Change if your Flask app runs elsewhere

def test_login(username, password):
    url = f"{BASE_URL}/login"
    payload = {
        "username": username,
        "password": password
    }
    response = requests.post(url, json=payload)
    print(f"Testing login for user '{username}'")
    print("Status Code:", response.status_code)
    try:
        print("Response JSON:", response.json())
    except Exception:
        print("Response Text:", response.text)
    print("-" * 40)
    return response

if __name__ == "__main__":
    # Test with a valid user (ensure this user exists in your DB)
    test_login("admin", "adminSecret1234")
    test_login("dev", "devPass!2024")
    test_login("ops", "Ops12345")
    test_login("jr.ops", "jrOps!789")
    test_login("banker", "BankerPassword123")

    # Test with invalid credentials
    test_login("admin", "wrongpassword")
    test_login("nonexistentuser", "somepassword")
