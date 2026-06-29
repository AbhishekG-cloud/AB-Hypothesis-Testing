import numpy as np
import pytest


from statsmodels.stats.proportion import proportions_ztest
from src.frequentist_tests import two_proportion_ztest,minimum_sample_size


def test_z_statistic_and_pvalue():

    my_result = two_proportion_ztest(
        n_A=1000,
        conv_A=100,
        n_B=1000,
        conv_B=120
    )

    z_ref, p_ref = proportions_ztest(
        count=[100, 120],
        nobs=[1000, 1000]
    )

    assert np.isclose(
        abs(my_result["z_statistic"]),
        abs(z_ref)
    )

    assert np.isclose(
        my_result["p_value"],
        p_ref
    )


def test_equal_conversion_rates():
    my_result = two_proportion_ztest(
        n_A=1000,
        conv_A=100,
        n_B=1000,
        conv_B=100
    )
    assert abs(my_result['z_statistic']) <= 1e-10
    assert my_result['p_value'] > 0.95
    assert my_result['decision'] == "Fail to Reject H0"
def test_large_uplift():
    my_result = two_proportion_ztest(
        n_A=1000,
        conv_A=100,
        n_B=1000,
        conv_B=150
    )
    assert my_result["p_value"] < 0.05
    assert my_result["decision"] == "Reject H0"
def test_confidence_interval_logic():
    my_result = two_proportion_ztest(
        n_A=1000,
        conv_A=100,
        n_B=1000,
        conv_B=150
    )
    lower, upper = my_result["confidence_interval"]

    assert lower < upper
    

def test_invalid_visitors():
    with pytest.raises(ValueError):
        two_proportion_ztest(
            n_A=-1000,
            conv_A=100,
            n_B=1000,
            conv_B=150
        )

def test_invalid_conversions():
    with pytest.raises(ValueError):
        two_proportion_ztest(
            n_A=1000,
            conv_A=-100,
            n_B=1000,
            conv_B=150
        )
def test_invalid_alpha():
     with pytest.raises(ValueError):
        two_proportion_ztest(
            n_A=-1000,
            conv_A=100,
            n_B=1000,
            conv_B=150,
            alpha=-0.05
        )




    
"""
z_statistic (float): Computed z-test statistic.
p_value (float): Two-tailed p-value.
confidence_interval (tuple[float, float]): Lower and upper bounds of the confidence interval for the difference in proportions (p_B - p_A).
decision (str): Statistical conclusion ("Reject H0" or "Fail to Reject H0").
"""
## ==============================================================================
## ==============================================================================
def test_minimum_sample_size_positive():
    sample_mde = minimum_sample_size(
        baseline_rate=0.10,
        mde=0.01
    )
    assert isinstance(sample_mde, int)
    assert sample_mde > 0


def test_smaller_mde_requires_more_samples():
    """
    Test that detecting a smaller Minimum Detectable Effect (MDE)
    requires a larger sample size.
    """

    # Arrange
    sample_small_mde = minimum_sample_size(
        baseline_rate=0.10,
        mde=0.01
    )

    sample_large_mde = minimum_sample_size(
        baseline_rate=0.10,
        mde=0.05
    )

    # Assert
    assert sample_small_mde > sample_large_mde

def test_higher_power_requires_more_samples():
    sample_small_power = minimum_sample_size(
        baseline_rate=0.10,
        mde=0.05,
        power=0.5
    )

    sample_large_power = minimum_sample_size(
        baseline_rate=0.10,
        mde=0.05,
        
    )
    assert sample_large_power> sample_small_power

def test_smaller_alpha_requires_more_samples():
    sample_small_alpha = minimum_sample_size(
        baseline_rate=0.10,
        mde=0.01,
        alpha=0.01
    )

    sample_large_alpha = minimum_sample_size(
        baseline_rate=0.10,
        mde=0.05
    )
    assert sample_small_alpha > sample_large_alpha
def test_invalid_baseline_rate():
    with pytest.raises(ValueError):
        sample_mde = minimum_sample_size(
        baseline_rate=-0.10,
        mde=0.01
    )
def test_invalid_mde():
    with pytest.raises(ValueError):
        sample_mde = minimum_sample_size(
        baseline_rate=0.10,
        mde=-0.01
    )
def test_invalid_power():
    with pytest.raises(ValueError):
        sample_mde = minimum_sample_size(
        baseline_rate=0.10,
        mde=0.01,
        power=-0.9
    )



