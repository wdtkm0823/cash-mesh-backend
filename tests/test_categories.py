from fastapi import status


def test_create_category(client):
    """カテゴリー作成のテスト"""
    response = client.post(
        "/api/v1/categories/",
        json={"name": "食費"}
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["name"] == "食費"
    assert "id" in data
    assert "user_id" in data
    assert "created_at" in data
    assert "updated_at" in data


def test_get_category(client):
    """カテゴリー取得のテスト"""
    # カテゴリー作成
    create_response = client.post(
        "/api/v1/categories/",
        json={"name": "食費"}
    )
    category_id = create_response.json()["id"]

    # カテゴリー取得
    response = client.get(f"/api/v1/categories/{category_id}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == category_id
    assert data["name"] == "食費"


def test_get_category_not_found(client):
    """存在しないカテゴリー取得で404のテスト"""
    response = client.get("/api/v1/categories/9999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Category not found"


def test_get_categories(client):
    """カテゴリー一覧取得のテスト"""
    # 複数カテゴリー作成
    client.post(
        "/api/v1/categories/",
        json={"name": "食費"}
    )
    client.post(
        "/api/v1/categories/",
        json={"name": "交通費"}
    )

    # 一覧取得
    response = client.get("/api/v1/categories/")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 2
    assert data[0]["name"] == "食費"
    assert data[1]["name"] == "交通費"


def test_update_category(client):
    """カテゴリー更新のテスト"""
    # カテゴリー作成
    create_response = client.post(
        "/api/v1/categories/",
        json={"name": "食費"}
    )
    category_id = create_response.json()["id"]

    # カテゴリー更新
    response = client.put(
        f"/api/v1/categories/{category_id}",
        json={"name": "食費（更新）"}
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["name"] == "食費（更新）"


def test_update_category_not_found(client):
    """存在しないカテゴリー更新で404のテスト"""
    response = client.put(
        "/api/v1/categories/9999",
        json={"name": "食費"}
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Category not found"


def test_delete_category(client):
    """カテゴリー削除のテスト"""
    # カテゴリー作成
    create_response = client.post(
        "/api/v1/categories/",
        json={"name": "食費"}
    )
    category_id = create_response.json()["id"]

    # カテゴリー削除
    response = client.delete(f"/api/v1/categories/{category_id}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["message"] == "Category deleted successfully"

    # 削除確認
    get_response = client.get(f"/api/v1/categories/{category_id}")
    assert get_response.status_code == status.HTTP_404_NOT_FOUND


def test_delete_category_not_found(client):
    """存在しないカテゴリー削除で404のテスト"""
    response = client.delete("/api/v1/categories/9999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Category not found"
