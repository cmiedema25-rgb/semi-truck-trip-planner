from truckplan.hos import plan_long_haul


def test_la_chicago_four_day_plan():
    plan = plan_long_haul(2010.0, 131564)
    assert plan.days_required == 4
    assert plan.drive_blocks[0].drive_hours == 11.0
    assert plan.drive_blocks[-1].drive_hours < 11.0
    assert any(s.kind == "break" for s in plan.stops)
    assert any(s.kind == "fuel" for s in plan.stops)
    assert any(s.kind == "overnight" for s in plan.stops)
    assert "not compliance" in plan.disclaimer.lower() or "planning aid" in plan.disclaimer.lower()


def test_short_trip_one_day():
    plan = plan_long_haul(100.0, 7200)
    assert plan.days_required == 1
