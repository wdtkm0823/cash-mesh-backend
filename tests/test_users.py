from fastapi import status


def test_create_user(client):
    """ユーザー作成のテスト"""
    response = client.post(
        "/api/v1/users/",
        json={"email": "test@example.com", "username": "testuser"}
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["email"] == "test@example.com"
    assert data["username"] == "testuser"
    assert "id" in data
    assert "created_at" in data
    assert "updated_at" in data


def test_create_user_duplicate_email(client):
    """重複メールアドレスでエラーのテスト"""
    # 1人目のユーザー作成
    client.post(
        "/api/v1/users/",
        json={"email": "test@example.com", "username": "testuser1"}
    )

    # 同じメールアドレスで2人目を作成
    response = client.post(
        "/api/v1/users/",
        json={"email": "test@example.com", "username": "testuser2"}
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"] == "Email already registered"


def test_create_user_duplicate_username(client):
    """重複ユーザー名でエラーのテスト"""
    # 1人目のユーザー作成
    client.post(
        "/api/v1/users/",
        json={"email": "test1@example.com", "username": "testuser"}
    )

    # 同じユーザー名で2人目を作成
    response = client.post(
        "/api/v1/users/",
        json={"email": "test2@example.com", "username": "testuser"}
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.json()["detail"] == "Username already taken"


def test_get_user(client):
    """ユーザー取得のテスト"""
    # ユーザー作成
    create_response = client.post(
        "/api/v1/users/",
        json={"email": "test@example.com", "username": "testuser"}
    )
    user_id = create_response.json()["id"]

    # ユーザー取得
    response = client.get(f"/api/v1/users/{user_id}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == user_id
    assert data["email"] == "test@example.com"
    assert data["username"] == "testuser"


def test_get_user_not_found(client):
    """存在しないユーザー取得で404のテスト"""
    response = client.get("/api/v1/users/9999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "User not found"


def test_get_users(client):
    """ユーザー一覧取得のテスト"""
    # 複数ユーザー作成
    client.post(
        "/api/v1/users/",
        json={"email": "test1@example.com", "username": "testuser1"}
    )
    client.post(
        "/api/v1/users/",
        json={"email": "test2@example.com", "username": "testuser2"}
    )

    # 一覧取得
    response = client.get("/api/v1/users/")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 2
    assert data[0]["email"] == "test1@example.com"
    assert data[1]["email"] == "test2@example.com"


def test_update_user(client):
    """ユーザー更新のテスト"""
    # ユーザー作成
    create_response = client.post(
        "/api/v1/users/",
        json={"email": "test@example.com", "username": "testuser"}
    )
    user_id = create_response.json()["id"]

    # ユーザー更新
    response = client.put(
        f"/api/v1/users/{user_id}",
        json={"email": "updated@example.com", "username": "updateduser"}
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["email"] == "updated@example.com"
    assert data["username"] == "updateduser"


def test_update_user_not_found(client):
    """存在しないユーザー更新で404のテスト"""
    response = client.put(
        "/api/v1/users/9999",
        json={"email": "test@example.com", "username": "testuser"}
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "User not found"


def test_delete_user(client):
    """ユーザー削除のテスト"""
    # ユーザー作成
    create_response = client.post(
        "/api/v1/users/",
        json={"email": "test@example.com", "username": "testuser"}
    )
    user_id = create_response.json()["id"]

    # ユーザー削除
    response = client.delete(f"/api/v1/users/{user_id}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["message"] == "User deleted successfully"

    # 削除確認
    get_response = client.get(f"/api/v1/users/{user_id}")
    assert get_response.status_code == status.HTTP_404_NOT_FOUND


def test_delete_user_not_found(client):
    """存在しないユーザー削除で404のテスト"""
    response = client.delete("/api/v1/users/9999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "User not found"
