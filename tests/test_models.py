from truckplan.models import CLASS8_DRY_VAN, PRESETS, VehicleProfile


def test_class8_defaults():
    v = CLASS8_DRY_VAN
    assert v.height_m == 4.11
    assert v.width_m == 2.59
    assert v.axles == 5
    assert v.hazmat is False


def test_ors_options_include_restrictions():
    opts = VehicleProfile().as_ors_options()
    r = opts["profile_params"]["restrictions"]
    assert r["height"] == 4.11
    assert r["weight"] == 36.29


def test_hazmat_option():
    opts = VehicleProfile(hazmat=True).as_ors_options()
    assert opts["profile_params"]["restrictions"]["hazmat"] is True


def test_presets():
    assert set(PRESETS) >= {"dry_van", "reefer", "flatbed"}
