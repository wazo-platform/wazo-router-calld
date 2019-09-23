from .common import get_app_and_client


@get_app_and_client
def test_create_ipbx(app=None, client=None):
    from wazo_router_calld.database import SessionLocal
    from wazo_router_calld.models.domain import Domain
    from wazo_router_calld.models.tenant import Tenant

    tenant = Tenant(name='fabio')
    domain = Domain(domain='testdomain.com', tenant=tenant)
    session = SessionLocal(bind=app.engine)
    session.add_all([tenant, domain])
    session.commit()
    #
    response = client.post(
        "/ipbx/",
        json={
            "tenant_id": tenant.id,
            "domain_id": domain.id,
            "customer": 1,
            "ip_fqdn": "mypbx.com",
            "port": 5060,
            "registered": True,
            "username": "user",
            "sha1": "da39a3ee5e6b4b0d3255bfef95601890afd80709",
            "sha1b": "f10e2821bbbea527ea02200352313bc059445190",
        },
    )
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "tenant_id": 1,
        "domain_id": 1,
        "customer": 1,
        "ip_fqdn": "mypbx.com",
        "port": 5060,
        "registered": True,
        "username": "user",
        "sha1": "da39a3ee5e6b4b0d3255bfef95601890afd80709",
        "sha1b": "f10e2821bbbea527ea02200352313bc059445190",
    }


@get_app_and_client
def test_get_ipbx(app=None, client=None):
    from wazo_router_calld.database import SessionLocal
    from wazo_router_calld.models.domain import Domain
    from wazo_router_calld.models.tenant import Tenant
    from wazo_router_calld.models.ipbx import IPBX

    tenant = Tenant(name='fabio')
    domain = Domain(domain='testdomain.com', tenant=tenant)
    ipbx = IPBX(
        tenant=tenant,
        domain=domain,
        customer=1,
        ip_fqdn='mypbx.com',
        registered=True,
        username='user',
        sha1='da39a3ee5e6b4b0d3255bfef95601890afd80709',
        sha1b='f10e2821bbbea527ea02200352313bc059445190',
    )
    session = SessionLocal(bind=app.engine)
    session.add_all([tenant, domain, ipbx])
    session.commit()
    #
    response = client.get("/ipbx/1")
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "customer": 1,
        "ip_fqdn": "mypbx.com",
        "port": 5060,
        "domain_id": domain.id,
        "tenant_id": tenant.id,
        "registered": True,
        "username": "user",
        "sha1": "da39a3ee5e6b4b0d3255bfef95601890afd80709",
        "sha1b": "f10e2821bbbea527ea02200352313bc059445190",
    }


@get_app_and_client
def test_get_ipbx_not_found(app=None, client=None):
    response = client.get("/ipbx/1")
    assert response.status_code == 404


@get_app_and_client
def test_update_ipbx(app=None, client=None):
    from wazo_router_calld.database import SessionLocal
    from wazo_router_calld.models.ipbx import IPBX
    from wazo_router_calld.models.domain import Domain
    from wazo_router_calld.models.tenant import Tenant

    tenant = Tenant(name='fabio')
    domain = Domain(domain='testdomain.com', tenant=tenant)
    ipbx = IPBX(
        tenant=tenant,
        domain=domain,
        customer=1,
        ip_fqdn='mypbx.com',
        registered=True,
        username='user',
        sha1='da39a3ee5e6b4b0d3255bfef95601890afd80709',
        sha1b='f10e2821bbbea527ea02200352313bc059445190',
    )
    session = SessionLocal(bind=app.engine)
    session.add_all([tenant, domain, ipbx])
    session.commit()
    #
    response = client.put(
        "/ipbx/1",
        json={
            'ip_fqdn': 'mypbx2.com',
            'tenant_id': 2,
            'domain_id': 3,
            'username': 'otheruser',
            'registered': False,
        },
    )
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "customer": 1,
        "ip_fqdn": "mypbx2.com",
        "port": 5060,
        "domain_id": 3,
        "tenant_id": 2,
        "registered": False,
        "username": "otheruser",
        "sha1": "da39a3ee5e6b4b0d3255bfef95601890afd80709",
        "sha1b": "f10e2821bbbea527ea02200352313bc059445190",
    }


@get_app_and_client
def test_update_ipbx_not_found(app=None, client=None):
    response = client.put("/ipbx/1", json={"ip_fqdn": "mypbx3.com"})
    assert response.status_code == 404


@get_app_and_client
def test_delete_ipbx(app=None, client=None):
    from wazo_router_calld.database import SessionLocal
    from wazo_router_calld.models.ipbx import IPBX
    from wazo_router_calld.models.domain import Domain
    from wazo_router_calld.models.tenant import Tenant

    tenant = Tenant(name='fabio')
    domain = Domain(domain='testdomain.com', tenant=tenant)
    ipbx = IPBX(
        tenant=tenant,
        domain=domain,
        customer=1,
        ip_fqdn='mypbx.com',
        registered=True,
        username='user',
        sha1='da39a3ee5e6b4b0d3255bfef95601890afd80709',
        sha1b='f10e2821bbbea527ea02200352313bc059445190',
    )
    session = SessionLocal(bind=app.engine)
    session.add_all([tenant, domain, ipbx])
    session.commit()
    #
    response = client.delete("/ipbx/1")
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "customer": 1,
        "ip_fqdn": "mypbx.com",
        "port": 5060,
        "domain_id": 1,
        "tenant_id": 1,
        "registered": True,
        "username": "user",
        "sha1": "da39a3ee5e6b4b0d3255bfef95601890afd80709",
        "sha1b": "f10e2821bbbea527ea02200352313bc059445190",
    }


@get_app_and_client
def test_delete_ipbx_not_found(app=None, client=None):
    response = client.delete("/ipbx/1")
    assert response.status_code == 404
