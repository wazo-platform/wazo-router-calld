from .common import get_app_and_client


@get_app_and_client
def test_create_tenant(app=None, client=None):
    response = client.post("/tenants/", json={"name": "fabio"})
    assert response.status_code == 200
    assert response.json() == {"id": 1, "name": "fabio"}


@get_app_and_client
def test_create_duplicated_tenant(app=None, client=None):
    from wazo_router_calld.database import SessionLocal
    from wazo_router_calld.models.tenant import Tenant

    session = SessionLocal(bind=app.engine)
    session.add(Tenant(name='fabio'))
    session.commit()
    #
    response = client.post("/tenants/", json={"name": "fabio"})
    assert response.status_code == 400


@get_app_and_client
def test_get_tenant(app=None, client=None):
    from wazo_router_calld.database import SessionLocal
    from wazo_router_calld.models.tenant import Tenant

    session = SessionLocal(bind=app.engine)
    session.add(Tenant(name='fabio'))
    session.commit()
    #
    response = client.get("/tenants/1")
    assert response.status_code == 200
    assert response.json() == {"id": 1, "name": "fabio"}


@get_app_and_client
def test_get_tenant_not_found(app=None, client=None):
    response = client.get("/tenants/1")
    assert response.status_code == 404


@get_app_and_client
def test_get_tenants(app=None, client=None):
    from wazo_router_calld.database import SessionLocal
    from wazo_router_calld.models.tenant import Tenant

    session = SessionLocal(bind=app.engine)
    session.add(Tenant(name='fabio'))
    session.commit()
    #
    response = client.get("/tenants/")
    assert response.status_code == 200
    assert response.json() == [{'id': 1, 'name': 'fabio'}]


@get_app_and_client
def test_update_tenant(app=None, client=None):
    from wazo_router_calld.database import SessionLocal
    from wazo_router_calld.models.tenant import Tenant

    session = SessionLocal(bind=app.engine)
    session.add(Tenant(name='fabio'))
    session.commit()
    #
    response = client.put("/tenants/1", json={'name': 'alex'})
    assert response.status_code == 200
    assert response.json() == {'id': 1, 'name': 'alex'}


@get_app_and_client
def test_update_tenant_not_found(app=None, client=None):
    response = client.put("/tenants/1", json={'name': 'alex'})
    assert response.status_code == 404
