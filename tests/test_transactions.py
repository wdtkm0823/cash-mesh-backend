from fastapi import status
from datetime import date, timedelta


def test_create_transaction_with_category(client):
    """カテゴリー付き収支作成のテスト"""
    # カテゴリー作成
    category_response = client.post(
        "/api/v1/categories/",
        json={"name": "食費"}
    )
    category_id = category_response.json()["id"]

    # 収支作成
    response = client.post(
        "/api/v1/transactions/",
        json={
            "category_id": category_id,
            "amount": 5000.50,
            "transaction_type": "expense",
            "description": "スーパーで買い物",
            "transaction_date": str(date.today())
        }
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["category_id"] == category_id
    assert data["amount"] == 5000.50
    assert data["transaction_type"] == "expense"
    assert data["description"] == "スーパーで買い物"
    assert "id" in data
    assert "user_id" in data


def test_create_transaction_without_category(client):
    """カテゴリーなし収支作成のテスト"""
    response = client.post(
        "/api/v1/transactions/",
        json={
            "amount": 50000,
            "transaction_type": "income",
            "description": "給料",
            "transaction_date": str(date.today())
        }
    )
    assert response.status_code == status.HTTP_201_CREATED
    data = response.json()
    assert data["category_id"] is None
    assert data["amount"] == 50000
    assert data["transaction_type"] == "income"


def test_create_transaction_with_invalid_category(client):
    """存在しないカテゴリーでエラーのテスト"""
    response = client.post(
        "/api/v1/transactions/",
        json={
            "category_id": 9999,
            "amount": 1000,
            "transaction_type": "expense",
            "transaction_date": str(date.today())
        }
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Category not found"


def test_create_transaction_with_invalid_amount(client):
    """金額が0以下でエラーのテスト"""
    response = client.post(
        "/api/v1/transactions/",
        json={
            "amount": -100,
            "transaction_type": "expense",
            "transaction_date": str(date.today())
        }
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_get_transaction(client):
    """収支取得のテスト"""
    # 収支作成
    create_response = client.post(
        "/api/v1/transactions/",
        json={
            "amount": 3000,
            "transaction_type": "expense",
            "transaction_date": str(date.today())
        }
    )
    transaction_id = create_response.json()["id"]

    # 収支取得
    response = client.get(f"/api/v1/transactions/{transaction_id}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["id"] == transaction_id
    assert data["amount"] == 3000


def test_get_transaction_not_found(client):
    """存在しない収支取得で404のテスト"""
    response = client.get("/api/v1/transactions/9999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json()["detail"] == "Transaction not found"


def test_get_transactions(client):
    """収支一覧取得のテスト"""
    # 複数収支作成
    client.post(
        "/api/v1/transactions/",
        json={"amount": 1000, "transaction_type": "expense", "transaction_date": str(date.today())}
    )
    client.post(
        "/api/v1/transactions/",
        json={"amount": 50000, "transaction_type": "income", "transaction_date": str(date.today())}
    )

    # 一覧取得
    response = client.get("/api/v1/transactions/")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 2


def test_get_transactions_filter_by_type(client):
    """収支タイプでフィルターのテスト"""
    # 収入と支出を作成
    client.post(
        "/api/v1/transactions/",
        json={"amount": 1000, "transaction_type": "expense", "transaction_date": str(date.today())}
    )
    client.post(
        "/api/v1/transactions/",
        json={"amount": 50000, "transaction_type": "income", "transaction_date": str(date.today())}
    )

    # 支出のみ取得
    response = client.get("/api/v1/transactions/?transaction_type=expense")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 1
    assert data[0]["transaction_type"] == "expense"


def test_get_transactions_filter_by_category(client):
    """カテゴリーでフィルターのテスト"""
    # カテゴリー作成
    category_response = client.post(
        "/api/v1/categories/",
        json={"name": "食費"}
    )
    category_id = category_response.json()["id"]

    # カテゴリー付き収支作成
    client.post(
        "/api/v1/transactions/",
        json={
            "category_id": category_id,
            "amount": 1000,
            "transaction_type": "expense",
            "transaction_date": str(date.today())
        }
    )
    # カテゴリーなし収支作成
    client.post(
        "/api/v1/transactions/",
        json={"amount": 2000, "transaction_type": "expense", "transaction_date": str(date.today())}
    )

    # カテゴリーでフィルター
    response = client.get(f"/api/v1/transactions/?category_id={category_id}")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert len(data) == 1
    assert data[0]["category_id"] == category_id


def test_update_transaction(client):
    """収支更新のテスト"""
    # 収支作成
    create_response = client.post(
        "/api/v1/transactions/",
        json={"amount": 1000, "transaction_type": "expense", "transaction_date": str(date.today())}
    )
    transaction_id = create_response.json()["id"]

    # 収支更新
    response = client.put(
        f"/api/v1/transactions/{transaction_id}",
        json={
            "amount": 2000,
            "transaction_type": "expense",
            "description": "更新後",
            "transaction_date": str(date.today())
        }
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert data["amount"] == 2000
    assert data["description"] == "更新後"


def test_delete_transaction(client):
    """収支削除のテスト"""
    # 収支作成
    create_response = client.post(
        "/api/v1/transactions/",
        json={"amount": 1000, "transaction_type": "expense", "transaction_date": str(date.today())}
    )
    transaction_id = create_response.json()["id"]

    # 収支削除
    response = client.delete(f"/api/v1/transactions/{transaction_id}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["message"] == "Transaction deleted successfully"

    # 削除確認
    get_response = client.get(f"/api/v1/transactions/{transaction_id}")
    assert get_response.status_code == status.HTTP_404_NOT_FOUND


def test_category_deleted_sets_transaction_category_to_null(client):
    """カテゴリー削除時にトランザクションのcategory_idがNULLになるテスト"""
    # カテゴリー作��
    category_response = client.post(
        "/api/v1/categories/",
        json={"name": "食費"}
    )
    category_id = category_response.json()["id"]

    # カテゴリー付き収支作成
    transaction_response = client.post(
        "/api/v1/transactions/",
        json={
            "category_id": category_id,
            "amount": 1000,
            "transaction_type": "expense",
            "transaction_date": str(date.today())
        }
    )
    transaction_id = transaction_response.json()["id"]

    # カテゴリー削除
    client.delete(f"/api/v1/categories/{category_id}")

    # トランザクション確認 - category_idがNULLになっているはず
    transaction_response = client.get(f"/api/v1/transactions/{transaction_id}")
    assert transaction_response.status_code == status.HTTP_200_OK
    assert transaction_response.json()["category_id"] is None
