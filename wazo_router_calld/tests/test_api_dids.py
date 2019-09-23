from .common import get_app_and_client


@get_app_and_client
def test_create_did(app=None, client=None):
    response = client.post(
        "/dids/",
        json={
            "did_regex": "^(\+?1)?(8(00|44|55|66|77|88)[2-9]\d{6})$",
            "carrier_trunk_id": 1,
            "tenant_id": 1,
        },
    )
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "did_regex": "^(\+?1)?(8(00|44|55|66|77|88)[2-9]\d{6})$",
        "carrier_trunk_id": 1,
        "tenant_id": 1,
    }


@get_app_and_client
def test_create_duplicated_did(app=None, client=None):
    from wazo_router_calld.database import SessionLocal
    from wazo_router_calld.models.did import DID

    session = SessionLocal(bind=app.engine)
    session.add(
        DID(
            did_regex='^(\+?1)?(8(00|44|55|66|77|88)[2-9]\d{6})$',
            carrier_trunk_id=1,
            tenant_id=1,
        )
    )
    session.commit()
    #
    response = client.post(
        "/dids/",
        json={
            "did_regex": "^(\+?1)?(8(00|44|55|66|77|88)[2-9]\d{6})$",
            "carrier_trunk_id": 1,
            "tenant_id": 1,
        },
    )
    assert response.status_code == 400


@get_app_and_client
def test_get_did(app=None, client=None):
    from wazo_router_calld.database import SessionLocal
    from wazo_router_calld.models.did import DID

    session = SessionLocal(bind=app.engine)
    session.add(
        DID(
            did_regex='^(\+?1)?(8(00|44|55|66|77|88)[2-9]\d{6})$',
            carrier_trunk_id=1,
            tenant_id=1,
        )
    )
    session.commit()
    #
    response = client.get("/dids/1")
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "did_regex": "^(\+?1)?(8(00|44|55|66|77|88)[2-9]\d{6})$",
        "carrier_trunk_id": 1,
        "tenant_id": 1,
    }


@get_app_and_client
def test_get_did_not_found(app=None, client=None):
    response = client.get("/dids/1")
    assert response.status_code == 404


@get_app_and_client
def test_get_dids(app=None, client=None):
    from wazo_router_calld.database import SessionLocal
    from wazo_router_calld.models.did import DID

    session = SessionLocal(bind=app.engine)
    session.add(
        DID(
            did_regex='^(\+?1)?(8(00|44|55|66|77|88)[2-9]\d{6})$',
            carrier_trunk_id=1,
            tenant_id=1,
        )
    )
    session.commit()
    #
    response = client.get("/dids/")
    assert response.status_code == 200
    assert response.json() == [
        {
            "id": 1,
            "did_regex": "^(\+?1)?(8(00|44|55|66|77|88)[2-9]\d{6})$",
            "carrier_trunk_id": 1,
            "tenant_id": 1,
        }
    ]


@get_app_and_client
def test_update_did(app=None, client=None):
    from wazo_router_calld.database import SessionLocal
    from wazo_router_calld.models.did import DID

    session = SessionLocal(bind=app.engine)
    session.add(
        DID(
            did_regex='^(\+?1)?(8(00|44|55|66|77|88)[2-9]\d{6})$',
            carrier_trunk_id=1,
            tenant_id=1,
        )
    )
    session.commit()
    #
    response = client.put(
        "/dids/1",
        json={
            "id": 1,
            "did_regex": "^(\+?1)?(8(00|44|55|66|77|88)[2-9]\d{6})$",
            "carrier_trunk_id": 2,
            "tenant_id": 2,
        },
    )
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "did_regex": "^(\+?1)?(8(00|44|55|66|77|88)[2-9]\d{6})$",
        "carrier_trunk_id": 2,
        "tenant_id": 2,
    }


@get_app_and_client
def test_update_did_not_found(app=None, client=None):
    response = client.put(
        "/dids/1",
        json={
            "did_regex": "^(\+?1)?(8(00|44|55|66|77|88)[2-9]\d{6})$",
            "carrier_trunk_id": 3,
            "tenant_id": 1,
        },
    )
    assert response.status_code == 404
