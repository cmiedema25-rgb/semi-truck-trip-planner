from truckplan.roi import RoiAssumptions, compute_roi, format_roi_markdown


def test_default_long_haul_roi_math():
    roi = compute_roi()
    assert roi.time_saved_minutes == 28.0
    assert abs(roi.time_saved_pct - 87.5) < 0.2
    assert abs(roi.illustrative_value_usd - 16.33) < 0.05
    assert abs(roi.daily_hours_saved - 3.73) < 0.05
    assert abs(roi.daily_illustrative_value_usd - 130.67) < 1.0
    assert roi.assumptions.scenario_miles == 2010.0
    assert "illustrative" in roi.label.lower()


def test_custom_assumptions():
    roi = compute_roi(
        RoiAssumptions(manual_minutes=40, tool_minutes=3, dispatcher_rate_usd_per_hour=40, trips_per_day=8)
    )
    assert roi.time_saved_minutes == 37.0


def test_markdown_table():
    md = format_roi_markdown(compute_roi())
    assert "32 min" in md
    assert "4 min" in md
