from truckplan.roi import RoiAssumptions, compute_roi, format_roi_markdown


def test_default_roi_math():
    roi = compute_roi()
    assert roi.time_saved_minutes == 13.0
    assert abs(roi.time_saved_pct - 86.7) < 0.2
    assert abs(roi.illustrative_value_usd - 7.58) < 0.05
    assert abs(roi.daily_hours_saved - 4.33) < 0.05
    assert abs(roi.daily_illustrative_value_usd - 151.67) < 1.0
    assert "illustrative" in roi.label.lower()
    assert "customer" in roi.label.lower() or "synthetic" in roi.label.lower()


def test_custom_assumptions():
    roi = compute_roi(RoiAssumptions(manual_minutes=20, tool_minutes=1, dispatcher_rate_usd_per_hour=40, trips_per_day=10))
    assert roi.time_saved_minutes == 19.0
    assert abs(roi.illustrative_value_usd - (19 / 60 * 40)) < 0.01


def test_markdown_table():
    md = format_roi_markdown(compute_roi())
    assert "Trip ROI" in md
    assert "15 min" in md
    assert "2 min" in md
    assert "Illustrative" in md or "illustrative" in md
