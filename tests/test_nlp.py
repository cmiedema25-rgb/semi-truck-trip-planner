from truckplan.nlp import parse_trip_text, template_summary


def test_destination_only():
    p = parse_trip_text("Houston warehouse")
    assert p.destination == "Houston warehouse"
    assert p.origin is None
    assert p.hazmat is False


def test_to_from_hazmat():
    p = parse_trip_text("to Austin TX from Dallas yard, hazmat")
    assert p.destination is not None
    assert "Austin" in p.destination
    assert p.origin is not None
    assert "Dallas" in p.origin
    assert p.hazmat is True


def test_going_to():
    p = parse_trip_text("going to 5600 Warehouse Blvd, Houston, TX")
    assert p.destination is not None
    assert "Warehouse" in p.destination


def test_template_summary_mentions_disclaimer_context():
    s = template_summary("A", "B", 100.0, "2h 0m", "Class-8", "mock", False)
    assert "A → B" in s
    assert "100.0 miles" in s
