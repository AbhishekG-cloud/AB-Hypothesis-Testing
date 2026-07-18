from src.BaysianABtest import BayesianABTest
import pytest


def test_initialization():
    test = BayesianABTest()

    assert test.prior_params_A == (1.0, 1.0)
    assert test.prior_params_B == (1.0, 1.0)

    assert test.posterior_params_A == (1.0, 1.0)
    assert test.posterior_params_B == (1.0, 1.0)


def test_invalid_prior():
    with pytest.raises(ValueError):
        BayesianABTest(
            prior_params_A=(0, 1),
            prior_params_B=(1, 1),
        )


def test_update():
    test = BayesianABTest()

    test.update(
        visitors_A=100,
        conversions_A=20,
        visitors_B=100,
        conversions_B=10,
    )

    assert test.posterior_params_A == (21.0, 81.0)
    assert test.posterior_params_B == (11.0, 91.0)


def test_update_sequential():
    test = BayesianABTest()

    daily_data = [
        (100, 20, 100, 10),
        (50, 10, 50, 5),
    ]

    test.update_sequential(daily_data)

    assert test.posterior_params_A == (31.0, 121.0)
    assert test.posterior_params_B == (16.0, 136.0)


def test_posterior_mean():
    test = BayesianABTest()

    test.update(100, 20, 100, 10)

    summary = test.get_posterior_summary()

    assert summary["A"]["mean"] == pytest.approx(21 / 102)

    assert summary["B"]["mean"] == pytest.approx(11 / 102)


def test_posterior_mode():
    test = BayesianABTest()

    test.update(100, 20, 100, 10)

    summary = test.get_posterior_summary()

    assert summary["A"]["mode"] == pytest.approx(20 / 100)

    assert summary["B"]["mode"] == pytest.approx(10 / 100)


def test_credible_interval():
    test = BayesianABTest()

    test.update(100, 20, 100, 10)

    summary = test.get_posterior_summary()

    lower, upper = summary["A"]["credible_interval"]

    assert lower < upper

    assert lower <= summary["A"]["mean"] <= upper


def test_invalid_update():
    test = BayesianABTest()

    with pytest.raises(ValueError):
        test.update(
            visitors_A=100,
            conversions_A=120,
            visitors_B=100,
            conversions_B=10,
        )
