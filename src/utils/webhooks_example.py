schema_extra = {
    "event_type": "payment_approved",
    "webhook_name": "payment_approved",
    "occurred_at": 1690898390,
    "content": {
        "payment_id": 125068,
        "subscription_id": 125069,
        "payment_type": "pago_inicial",
        "user_id": 18212,
        "payment_status": "Aprobado",
        "totals": {
            "sub_total": 59900,
            "shipping": "0",
            "discounts": "0",
            "total": "59900.00",
        },
        "billing": {
            "first_name": "Dima",
            "last_name": "Prueba 3",
            "document": "44444444",
            "email": "dima3@hunty.com",
            "address_1": "GGGGGG",
            "address_2": "",
            "country": "CO",
            "state": "AMZ",
            "city": "Leticia",
            "phone": "3333333333",
            "phone_country_code": "+57",
            "zip_code": "05000001",
        },
        "shipping": "null",
        "items": [
            {
                "name": "Hunty Pro Trimestral UP.",
                "sku": "",
                "id": 123954,
                "quantity": 1,
                "subtotal": "59900",
                "total": "59900",
            }
        ],
        "fees": "null",
        "currency": "COP",
        "payment_gateway": "null",
        "payment_gateway_name": "null",
        "payment_method": "null",
        "meta_data": "null",
        "subscription_renewal_type": "manual",
    },
    "signature": "efd8ee39240a5a4b0c176a2bf31d0596ba2168e3ff7893d6f2d3acededec93a8",
}


subscription_canceled = {
    "event_type": "subscription_canceled",
    "webhook_name": "process_subscription",
    "occurred_at": 1691006533,
    "content": {
        "subscription_id": 123983,
        "customer": {
            "first_name": "Dima",
            "last_name": "Prueba 2",
            "document": "1222222222",
            "email": "dimappplpp3@hunty.com",
            "phone": "3333333333",
            "user_id": 18081,
        },
    },
}

get_active_subscription_response = {
    "user_id": "068c0210-31c9-41a9-bd16-c89d02a38911",
    "users_subscription_status": "Aprobado",
    "item_name": "Hunty Pro Semestral",
    "next_payment_date": "2021-08-31T00:00:00.000Z",
    "type_subscription": "Hunty Pro Semestral",
}
