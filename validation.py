import numpy as np
from statsmodels.stats.proportion import proportions_ztest

from src.frequentist_tests import two_proportion_ztest,minimum_sample_size


def test_two_proportion_ztest():

    n_A = 1000
    conv_A = 100

    n_B = 1000
    conv_B = 120

    my_result = two_proportion_ztest(
        n_A,
        conv_A,
        n_B,
        conv_B
    )

    z_ref, p_ref = proportions_ztest(
        count=[conv_A, conv_B],
        nobs=[n_A, n_B]
    )

    assert np.isclose(
        abs(my_result["z_statistic"]),
        abs(z_ref),
        atol=1e-10
    )

    assert np.isclose(
        my_result["p_value"],
        p_ref,
        atol=1e-10
    )
    print("My Implementation")
    print(my_result)

    print()

    print("Statsmodels")

    print("Z =", z_ref)

    print("P =", p_ref)
test_two_proportion_ztest()
def test_minimum_sample_size_positive():
    sample_mde = minimum_sample_size(
        baseline_rate=0.10,
        mde=0.01
    )
    assert isinstance(sample_mde, int)
    assert sample_mde > 0
test_minimum_sample_size_positive()