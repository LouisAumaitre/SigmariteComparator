from sigmar.basics.value import DiceValue, value


def test_average_1_is_1():
    # given
    random_value = value(1)
    # assert
    assert random_value.average({}, mod=1) == 2


def test_max_1_is_1():
    # given
    random_value = value(1)
    # assert
    assert random_value.max({}, mod=-1) == 0


def test_average_d6_is_35():
    # given
    random_value = value('D6')
    # assert
    assert random_value.average({}, mod=1) == 4.5


def test_max_d6_is_6():
    # given
    random_value = value('D6')
    # assert
    assert random_value.max({}, mod=-1) == 5


def test_max_apply_extras_on_context():
    # given

    def bonus(context):
        return context.get('bonus', 0)

    random_value = DiceValue('D6')
    random_value.rules.append(bonus)
    # assert
    assert random_value.max({'bonus': 37}, mod=-1) == 42


def test_average_apply_extras_on_context():
    # given

    def bonus(context):
        return context.get('bonus', 0)

    random_value = value(1)
    random_value.extra_bonuses.append(bonus)
    # assert
    assert random_value.average({'bonus': 21}, mod=20) == 42


def test_rv_create_rv():
    # given
    a = value(6)
    b = value('D6')
    c = value(DiceValue('D6'))
    # assert
    assert a.max({}) == b.max({}) == c.max({})
