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
    2. GET /api/budgets/status/?month=7&year=2025
        Authorization: Bearer <your-access-token>
        You will get response as For eg:
            {
                "month and year": "7/2025",
                "budget_amount": 1000.0,
                "income_total": 900.0,
                "expense_total": 500.0,
                "net_savings": 400.0,
                "remaining_budget": 500.0
            }
