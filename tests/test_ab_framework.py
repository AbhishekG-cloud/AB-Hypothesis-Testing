from src.ab_framework import ABTestFramework


def test_equal_conversion():

    framework = ABTestFramework()

    results = framework.run_full_analysis(
        n_A=1000, conv_A=120, n_B=1000, conv_B=120, prior_A=(1, 1), prior_B=(1, 1)
    )

    assert isinstance(results, dict)

    assert "frequentist" in results
    assert "bayesian" in results
    assert "monte_carlo" in results
    assert "recommendation" in results


def test_small_uplift():

    framework = ABTestFramework()

    results = framework.run_full_analysis(
        n_A=1000, conv_A=120, n_B=1000, conv_B=130, prior_A=(1, 1), prior_B=(1, 1)
    )

    probability = results["monte_carlo"]["probability_B_beats_A"]

    assert probability > 0.5


def test_large_uplift():

    framework = ABTestFramework()

    results = framework.run_full_analysis(
        n_A=1000, conv_A=120, n_B=1000, conv_B=180, prior_A=(1, 1), prior_B=(1, 1)
    )

    recommendation = results["recommendation"]["recommendation"]

    assert recommendation == "Launch Variant B"


import pytest


def test_invalid_input():

    framework = ABTestFramework()

    with pytest.raises(ValueError):

        framework.run_full_analysis(
            n_A=100, conv_A=120, n_B=100, conv_B=50, prior_A=(1, 1), prior_B=(1, 1)
        )
