from sigmar.basics.roll import Roll


def test_4plus_is_fifty_fifty():
    # given
    roll = Roll(4)
    # assert
    success, crit = roll.chances({})
    assert success + crit == 0.5
    assert -0.000001 < success - 2/6 < 0.000001
    assert -0.000001 < crit - 1/6 < 0.000001


def test_average_of_3_5plus_is_one():
    # given
    roll = Roll(5)
    # assert
    success, crit = roll.average(3, {})
    assert success + crit == 1
