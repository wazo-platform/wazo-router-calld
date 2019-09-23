from .common import get_app_and_client


@get_app_and_client
def test_create_domain(app=None, client=None):
    response = client.post(
        "/domains/", json={"domain": "testdomain.com", "tenant_id": 1}
    )
    assert response.status_code == 200
    assert response.json() == {"id": 1, "domain": "testdomain.com", "tenant_id": 1}


@get_app_and_client
def test_create_duplicated_domain(app=None, client=None):
    from wazo_router_calld.database import SessionLocal
    from wazo_router_calld.models.domain import Domain
    from wazo_router_calld.models.tenant import Tenant

    session = SessionLocal(bind=app.engine)
    tenant = Tenant(name='fabio')
    domain = Domain(domain='testdomain.com', tenant=tenant)
    session.add_all([domain, tenant])
    session.commit()
    #
    response = client.post(
        "/domains/", json={"domain": "testdomain.com", "tenant_id": 1}
    )
    assert response.status_code == 400


@get_app_and_client
def test_get_domain(app=None, client=None):
    from wazo_router_calld.database import SessionLocal
    from wazo_router_calld.models.domain import Domain
    from wazo_router_calld.models.tenant import Tenant

    session = SessionLocal(bind=app.engine)
    tenant = Tenant(name='fabio')
    domain = Domain(domain='testdomain.com', tenant=tenant)
    session.add_all([domain, tenant])
    session.commit()
    #
    response = client.get("/domains/1")
    assert response.status_code == 200
    assert response.json() == {"id": 1, "domain": "testdomain.com", "tenant_id": 1}


@get_app_and_client
def test_get_domain_not_found(app=None, client=None):
    response = client.get("/domains/1")
    assert response.status_code == 404


@get_app_and_client
def test_get_domains(app=None, client=None):
    from wazo_router_calld.database import SessionLocal
    from wazo_router_calld.models.domain import Domain
    from wazo_router_calld.models.tenant import Tenant

    session = SessionLocal(bind=app.engine)
    tenant = Tenant(name='fabio')
    domain = Domain(domain='testdomain.com', tenant=tenant)
    session.add_all([domain, tenant])
    session.commit()
    #
    response = client.get("/domains/")
    assert response.status_code == 200
    assert response.json() == [{'id': 1, 'domain': 'testdomain.com', 'tenant_id': 1}]


@get_app_and_client
def test_update_domain(app=None, client=None):
    from wazo_router_calld.database import SessionLocal
    from wazo_router_calld.models.domain import Domain
    from wazo_router_calld.models.tenant import Tenant

    session = SessionLocal(bind=app.engine)
    tenant = Tenant(name='test')
    domain = Domain(domain='testdomain.com', tenant=tenant)
    session.add_all([domain, tenant])
    session.commit()
    #
    response = client.put(
        "/domains/1", json={'domain': 'otherdomain.com', 'tenant_id': 2}
    )
    assert response.status_code == 200
    assert response.json() == {'id': 1, 'domain': 'otherdomain.com', 'tenant_id': 2}


@get_app_and_client
def test_update_domain_not_found(app=None, client=None):
    response = client.put("/domains/1", json={'domain': 'thirdone.com'})
    assert response.status_code == 404
