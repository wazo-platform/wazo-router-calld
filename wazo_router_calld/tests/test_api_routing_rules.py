from .common import get_app_and_client


@get_app_and_client
def test_create_routing_rule(app=None, client=None):
    response = client.post(
        "/routing_rules/",
        json={
            "prefix": "39",
            "carrier_trunk_id": 1,
            "ipbx_id": 1,
            "did_regex": r"^(\+?1)?(8(00|44|55|66|77|88)[2-9]\d{6})$",
            "route_type": "pstn",
        },
    )
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "prefix": "39",
        "carrier_trunk_id": 1,
        "ipbx_id": 1,
        "did_regex": r"^(\+?1)?(8(00|44|55|66|77|88)[2-9]\d{6})$",
        "route_type": "pstn",
    }


@get_app_and_client
def test_get_routing_rule(app=None, client=None):
    from wazo_router_calld.database import SessionLocal
    from wazo_router_calld.models.routing_rule import RoutingRule

    session = SessionLocal(bind=app.engine)
    session.add(
        RoutingRule(
            prefix="39",
            carrier_trunk_id=1,
            ipbx_id=1,
            did_regex=r'^(\+?1)?(8(00|44|55|66|77|88)[2-9]\d{6})$',
            route_type="pstn",
        )
    )
    session.commit()
    #
    response = client.get("/routing_rules/1")
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "prefix": "39",
        "carrier_trunk_id": 1,
        "ipbx_id": 1,
        "did_regex": r"^(\+?1)?(8(00|44|55|66|77|88)[2-9]\d{6})$",
        "route_type": "pstn",
    }


@get_app_and_client
def test_get_routing_rule_not_found(app=None, client=None):
    response = client.get("/routing_rules/1")
    assert response.status_code == 404


@get_app_and_client
def test_get_routing_rules(app=None, client=None):
    from wazo_router_calld.database import SessionLocal
    from wazo_router_calld.models.routing_rule import RoutingRule

    session = SessionLocal(bind=app.engine)
    session.add(
        RoutingRule(
            prefix="39",
            carrier_trunk_id=1,
            ipbx_id=1,
            did_regex=r'^(\+?1)?(8(00|44|55|66|77|88)[2-9]\d{6})$',
            route_type="pstn",
        )
    )
    session.commit()
    #
    response = client.get("/routing_rules/")
    assert response.status_code == 200
    assert response.json() == [
        {
            "id": 1,
            "prefix": "39",
            "carrier_trunk_id": 1,
            "ipbx_id": 1,
            "did_regex": r"^(\+?1)?(8(00|44|55|66|77|88)[2-9]\d{6})$",
            "route_type": "pstn",
        }
    ]


@get_app_and_client
def test_update_routing_rule(app=None, client=None):
    from wazo_router_calld.database import SessionLocal
    from wazo_router_calld.models.routing_rule import RoutingRule

    session = SessionLocal(bind=app.engine)
    session.add(
        RoutingRule(
            prefix="39",
            carrier_trunk_id=1,
            ipbx_id=1,
            did_regex=r'^(\+?1)?(8(00|44|55|66|77|88)[2-9]\d{6})$',
            route_type="pstn",
        )
    )
    session.commit()
    #
    response = client.put(
        "/routing_rules/1", json={'prefix': '40', 'carrier_trunk_id': 2}
    )
    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "prefix": "40",
        "carrier_trunk_id": 2,
        "ipbx_id": 1,
        "did_regex": r"^(\+?1)?(8(00|44|55|66|77|88)[2-9]\d{6})$",
        "route_type": "pstn",
    }


@get_app_and_client
def test_update_routing_rule_not_found(app=None, client=None):
    response = client.put("/routing_rules/1", json={'prefix': '385'})
    assert response.status_code == 404
