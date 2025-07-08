# Budget/Expense Tracker

    Budget Tracker API using Django REST Framework

    /admin/ to add,delete,modify category-transaction-budget

    Use application like Postman to test the API.
    1. POST /api/token/
        Body (JSON):
        {
            "username": "testuser",
            "password": "testpass123"
        }
        Use the "access" token from response.
    2. GET /api/budget-status/
        Authorization: Bearer <your-access-token>
        You will get response as For eg:
            {
                "month": "July",
                "budget": 40000,
                "income_total": 30000,
                "expenses_total": 14000,
                "net_savings": 16000,
                "remaining_budget": 26000
            }
