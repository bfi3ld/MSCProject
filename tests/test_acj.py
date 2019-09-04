from project.acj import *
import numpy.testing as npt
import pytest


@pytest.mark.parametrize('v1,v2,exp', [
    (5, 5, .5),
    (0, 0, .5),
    (1, 2, 0.26894),
    (None, None, None)
])

def test_calc_probability(v1, v2, exp):
    if exp is None:
        with pytest.raises(TypeError):
            _ = calc_probability(v1, v2)
    else:
        actual = calc_probability(v1, v2)
        npt.assert_almost_equal(actual, exp, decimal=5)


def test_get_iteration_value():
    script_score, script_value, other_scripts_values = 4, 1, [1, 1, 1, 1]
    new_script_value = get_iteration_value(script_score, script_value, other_scripts_values)
    assert new_script_value == (3, 2)


def test_get_iteration_values():
    script_scores, script_values = [1, 4, 2, 1, 2], [1, 1, 1, 1, 1]

    actual = get_iteration_values(script_scores, script_values)
    expected = ([0, 3, 1, 0, 1], [2] * 5)

    npt.assert_array_almost_equal(actual, expected, decimal=3)


def test_estimate_values():
    _, actual = estimate_values([1, 4, 2, 1, 2])
    expected = [1, 4, 2, 1, 2]
    npt.assert_array_almost_equal(actual, expected, decimal=3)


if __name__ == '__main__':
    pass
