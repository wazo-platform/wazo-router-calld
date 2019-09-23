from .common import get_app_and_client


@get_app_and_client
def test_create_routing_group(app=None, client=None):
    response = client.post("/routing_groups/", json={"routing_rule": 1, "tenant_id": 1})
    assert response.status_code == 200
    assert response.json() == {"id": 1, "routing_rule": 1, "tenant_id": 1}


@get_app_and_client
def test_get_routing_group(app=None, client=None):
    from wazo_router_calld.database import SessionLocal
    from wazo_router_calld.models.routing_group import RoutingGroup

    session = SessionLocal(bind=app.engine)
    session.add(RoutingGroup(routing_rule=1, tenant_id=1))
    session.commit()
    #
    response = client.get("/routing_groups/1")
    assert response.status_code == 200
    assert response.json() == {"id": 1, "routing_rule": 1, "tenant_id": 1}


@get_app_and_client
def test_get_routing_group_not_found(app=None, client=None):
    response = client.get("/routing_groups/1")
    assert response.status_code == 404


@get_app_and_client
def test_get_routing_groups(app=None, client=None):
    from wazo_router_calld.database import SessionLocal
    from wazo_router_calld.models.routing_group import RoutingGroup

    session = SessionLocal(bind=app.engine)
    session.add(RoutingGroup(routing_rule=1, tenant_id=1))
    session.commit()
    #
    response = client.get("/routing_groups/")
    assert response.status_code == 200
    assert response.json() == [{"id": 1, "routing_rule": 1, "tenant_id": 1}]


@get_app_and_client
def test_update_routing_group(app=None, client=None):
    from wazo_router_calld.database import SessionLocal
    from wazo_router_calld.models.routing_group import RoutingGroup

    session = SessionLocal(bind=app.engine)
    session.add(RoutingGroup(routing_rule=1, tenant_id=1))
    session.commit()
    #
    response = client.put("/routing_groups/1", json={'routing_rule': 2, 'tenant_id': 2})
    assert response.status_code == 200
    assert response.json() == {"id": 1, "routing_rule": 2, "tenant_id": 2}


@get_app_and_client
def test_update_routing_group_not_found(app=None, client=None):
    response = client.put("/routing_groups/1", json={'name': 'updated_carrier'})
    assert response.status_code == 404


@get_app_and_client
def test_delete_routing_group(app=None, client=None):
    from wazo_router_calld.database import SessionLocal
    from wazo_router_calld.models.routing_group import RoutingGroup

    session = SessionLocal(bind=app.engine)
    session.add(RoutingGroup(routing_rule=1, tenant_id=1))
    session.commit()
    #
    response = client.delete("/routing_groups/1")
    assert response.status_code == 200
    assert response.json() == {"id": 1, "routing_rule": 1, "tenant_id": 1}


@get_app_and_client
def test_delete_routing_group_not_found(app=None, client=None):
    response = client.delete("/routing_groups/1")
    assert response.status_code == 404
