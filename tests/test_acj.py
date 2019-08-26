from project.acj import *
import numpy.testing as npt

def test_calc_probability():
    assert calc_probability(5, 5) == .5


def test_get_iteration_value():
    script_score, script_value, other_scripts_values = 4, 1, [1, 1, 1, 1]
    new_script_value = get_iteration_value(script_score, script_value, other_scripts_values)
    assert new_script_value == (3,2)

def test_get_iteration_values():
    script_scores, script_values = [1,4,2,1,2], [1, 1, 1, 1,1]

    actual = get_iteration_values(script_scores, script_values)
    expected = ([0, 3, 1, 0, 1], [2]*5)

    npt.assert_array_almost_equal(actual, expected, decimal=3)


def test_estimate_values():
    _, actual = estimate_values([1, 4, 2, 1, 2]) 
    expected = [1,4,2,1,2]
    npt.assert_array_almost_equal(actual, expected, decimal=3)



if __name__ == '__main__':
    