
import pytest

from parking_fee import parking_fee, find_slot, monthly_pass


def test_free_short_stay():
    assert parking_fee("car", 20, False, False) == 0


def test_all_vehicle_rates():
    assert parking_fee("bike", 60, False, False) == 10
    assert parking_fee("car", 60, False, False) == 30
    assert parking_fee("truck", 60, False, False) == 60


def test_partial_hour_rounds_up():
    assert parking_fee("car", 61, False, False) == 60


def test_boundary_at_30_minutes():
    assert parking_fee("car", 30, False, False) == 0


def test_invalid_vehicle():
    with pytest.raises(ValueError, match="unknown vehicle"):
        parking_fee("bus", 60, False, False)


def test_negative_duration():
    with pytest.raises(ValueError, match="invalid duration"):
        parking_fee("car", -1, False, False)


def test_ev_discount():
    assert parking_fee("car", 60, True, False) == 15
    assert parking_fee("bike", 60, True, False) == 5


def test_truck_has_no_ev_discount():
    assert parking_fee("truck", 60, True, False) == 60


def test_lost_ticket_surcharge():
    assert parking_fee("car", 60, False, True) == 230


def test_ev_and_lost_ticket():
    assert parking_fee("car", 60, True, True) == 215


def test_full_parking_lot():
    assert find_slot("car", 0, False) == "full"
    assert find_slot("car", -1, False) == "full"


def test_disabled_parking():
    assert find_slot("car", 5, True) == "ground floor"


def test_truck_slot():
    assert find_slot("truck", 5, False) == "basement"


def test_any_floor():
    assert find_slot("car", 5, False) == "any floor"


def test_monthly_pass_prices():
    assert monthly_pass("bike", False) == 500
    assert monthly_pass("car", False) == 1500


def test_resident_monthly_discount():
    assert monthly_pass("bike", True) == 400
    assert monthly_pass("car", True) == 1200


def test_unsupported_monthly_pass():
    with pytest.raises(ValueError, match="no pass for this vehicle"):
        monthly_pass("truck", False)
