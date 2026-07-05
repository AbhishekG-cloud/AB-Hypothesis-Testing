from src.prior_utils import (
    beta_mean,
    beta_mode,
    beta_variance,
    beta_ci,
    beta_from_historical,
    plot_beta,
)

import math
import pytest
import plotly.graph_objects as go


# ==========================
# beta_mean
# ==========================

def test_beta_mean_normal():
    mean = beta_mean(1, 1)
    assert isinstance(mean, float)
    assert math.isclose(mean, 0.5)


@pytest.mark.parametrize(
    "alpha,beta",
    [
        (-1, 2),
        (2, -1),
        (0, 2),
        (2, 0),
    ],
)
def test_beta_mean_invalid(alpha, beta):
    with pytest.raises(ValueError):
        beta_mean(alpha, beta)


# ==========================
# beta_mode
# ==========================

def test_beta_mode_normal():
    mode = beta_mode(5, 3)
    assert math.isclose(mode, 4 / 6)


@pytest.mark.parametrize(
    "alpha,beta",
    [
        (1, 5),
        (5, 1),
        (1, 1),
        (0, 2),
        (-1, 2),
    ],
)
def test_beta_mode_invalid(alpha, beta):
    with pytest.raises(ValueError):
        beta_mode(alpha, beta)


# ==========================
# beta_variance
# ==========================

def test_beta_variance_normal():
    var = beta_variance(1, 1)
    assert math.isclose(var, 1 / 12)


@pytest.mark.parametrize(
    "alpha,beta",
    [
        (0, 1),
        (1, 0),
        (-1, 2),
        (2, -1),
    ],
)
def test_beta_variance_invalid(alpha, beta):
    with pytest.raises(ValueError):
        beta_variance(alpha, beta)


# ==========================
# beta_ci
# ==========================

def test_beta_ci_normal():
    lower, upper = beta_ci(5, 3)

    assert isinstance(lower, float)
    assert isinstance(upper, float)

    assert lower < upper
    assert 0 <= lower <= 1
    assert 0 <= upper <= 1


@pytest.mark.parametrize(
    "confidence",
    [
        0,
        1,
        -0.5,
        1.5,
    ],
)
def test_beta_ci_invalid_confidence(confidence):
    with pytest.raises(ValueError):
        beta_ci(5, 3, confidence)


@pytest.mark.parametrize(
    "alpha,beta",
    [
        (0, 3),
        (3, 0),
        (-1, 3),
        (3, -1),
    ],
)
def test_beta_ci_invalid_parameters(alpha, beta):
    with pytest.raises(ValueError):
        beta_ci(alpha, beta)


# ==========================
# beta_from_historical
# ==========================

def test_beta_from_historical_normal():
    alpha, beta = beta_from_historical(50, 100)

    assert alpha == 51
    assert beta == 51


def test_beta_from_historical_zero_conversions():
    alpha, beta = beta_from_historical(0, 100)

    assert alpha == 1
    assert beta == 101


def test_beta_from_historical_all_converted():
    alpha, beta = beta_from_historical(100, 100)

    assert alpha == 101
    assert beta == 1


@pytest.mark.parametrize(
    "conversions,visitors",
    [
        (-1, 100),
        (10, 0),
        (101, 100),
    ],
)
def test_beta_from_historical_invalid(conversions, visitors):
    with pytest.raises(ValueError):
        beta_from_historical(conversions, visitors)


# ==========================
# plot_beta
# ==========================

def test_plot_beta_normal():
    fig = plot_beta(5, 3, "Beta(5,3)")

    assert isinstance(fig, go.Figure)


@pytest.mark.parametrize(
    "alpha,beta",
    [
        (0, 3),
        (3, 0),
        (-1, 3),
        (3, -1),
    ],
)
def test_plot_beta_invalid(alpha, beta):
    with pytest.raises(ValueError):
        plot_beta(alpha, beta, "Invalid")