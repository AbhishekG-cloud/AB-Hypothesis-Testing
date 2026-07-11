import pytest

from src.monte_carlo import (
    prob_B_beats_A,
    expected_uplift,
    expected_loss,
    convergence_check
)
invalid_scenarios = [
    (0, 20, 15, 15, 1000),      # alpha_A <= 0
    (10, 0, 15, 15, 1000),      # beta_A <= 0
    (10, 20, -1, 15, 1000),     # alpha_B <= 0
    (10, 20, 15, 0, 1000),      # beta_B <= 0
    (10, 20, 15, 15, 0),        # n_samples <= 0
    (10, 20, 15, 15, -100),     # negative n_samples
]


@pytest.mark.parametrize(
    "alpha_A,beta_A,alpha_B,beta_B,n_samples",
    invalid_scenarios,
)
def test_prob_B_beats_A_invalid(
    alpha_A, beta_A, alpha_B, beta_B, n_samples
):
    with pytest.raises(ValueError):
        prob_B_beats_A(
            alpha_A, beta_A, alpha_B, beta_B, n_samples)

def test_identical_posteriors():
    prob = prob_B_beats_A(10, 10, 10, 10)
    uplift = expected_uplift(10, 10, 10, 10)
    loss = expected_loss(10, 10, 10, 10)

    assert 0.45 < prob < 0.55
    assert abs(uplift) < 0.01
    assert loss > 0

def test_B_better_than_A():
    prob = prob_B_beats_A(20, 80, 80, 20)

    assert prob > 0.99

@pytest.mark.parametrize(
    "alpha_A,beta_A,alpha_B,beta_B,n_samples",
    invalid_scenarios,
)
def test_expected_uplift_invalid(
    alpha_A, beta_A, alpha_B, beta_B, n_samples
):
    with pytest.raises(ValueError):
        expected_uplift(
            alpha_A, beta_A, alpha_B, beta_B, n_samples
        )

 
def test_positive_uplift():
    uplift = expected_uplift(20, 80, 80, 20)

    assert uplift > 0

@pytest.mark.parametrize(
    "alpha_A,beta_A,alpha_B,beta_B,n_samples",
    invalid_scenarios,
)
def test_expected_loss_invalid(
    alpha_A, beta_A, alpha_B, beta_B, n_samples
):
    with pytest.raises(ValueError):
        expected_loss(
            alpha_A, beta_A, alpha_B, beta_B, n_samples
        )


def test_expected_loss_non_negative():
    loss = expected_loss(20, 80, 80, 20)

    assert loss >= 0

def test_A_better_than_B():
    prob = prob_B_beats_A(80, 20, 20, 80)

    assert prob < 0.01

@pytest.mark.parametrize(
    "alpha_A,beta_A,alpha_B,beta_B,_",
    invalid_scenarios,
)
def test_convergence_check_invalid(
    alpha_A, beta_A, alpha_B, beta_B, _
):
    with pytest.raises(ValueError):
        convergence_check(alpha_A, beta_A, alpha_B, beta_B)


