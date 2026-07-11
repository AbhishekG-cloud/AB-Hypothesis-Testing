import numpy as np
import matplotlib.pyplot as plt 

def prob_B_beats_A(
        alpha_A:float,beta_A:float,
        alpha_B:float,beta_B:float,
        n_samples:int = 100000

)->float:
    """
    Estimate P(B > A) using Monte Carlo simulation.

    Args:
        alpha_A: Posterior alpha for Variant A.
        beta_A: Posterior beta for Variant A.
        alpha_B: Posterior alpha for Variant B.
        beta_B: Posterior beta for Variant B.
        n_samples: Number of Monte Carlo samples.

    Returns:
        Estimated probability that B outperforms A.
    """
    # Validate parameters
    if (
        alpha_A <= 0
        or beta_A <= 0
        or alpha_B <= 0
        or beta_B <= 0
    ):
        raise ValueError(
            "alpha_A, beta_A, alpha_B, and beta_B must all be positive."
        )

    if not isinstance(n_samples, int):
        raise ValueError("n_samples must be an integer.")

    if n_samples <= 0:
        raise ValueError("n_samples must be greater than 0.")
    samples_A = rng.beta(alpha_A,beta_A,size=n_samples)
    samples_B = rng.beta(alpha_B,beta_B,size=n_samples)
    rng = np.random.default_rng()

    wins = (samples_B>samples_A).mean()
    return wins

def expected_uplift(alpha_A:float,beta_A:float,
        alpha_B:float,beta_B:float,
        n_samples:int = 100000

)->float:
    """
    Estimate the expected uplift of Variant B over Variant A.

    Args:
        alpha_A: Posterior alpha for Variant A.
        beta_A: Posterior beta for Variant A.
        alpha_B: Posterior alpha for Variant B.
        beta_B: Posterior beta for Variant B.
        n_samples: Number of Monte Carlo samples.

    Returns:
        Estimated expected uplift.
    """
    if (
        alpha_A <= 0
        or beta_A <= 0
        or alpha_B <= 0
        or beta_B <= 0
    ):
        raise ValueError(
            "alpha_A, beta_A, alpha_B, and beta_B must all be positive."
        )

    if not isinstance(n_samples, int):
        raise ValueError("n_samples must be an integer.")

    if n_samples <= 0:
        raise ValueError("n_samples must be greater than 0.")
    samples_A = rng.beta(alpha_A,beta_A,size=n_samples)
    samples_B = rng.beta(alpha_B,beta_B,size=n_samples)
    rng = np.random.default_rng()

    uplift = (samples_B-samples_A).mean()

    return uplift

def expected_loss(alpha_A:float,beta_A:float,
        alpha_B:float,beta_B:float,
        n_samples:int = 100000

)->float:
    """
    Estimate the expected loss (regret) of choosing Variant B.

    Args:
        alpha_A: Posterior alpha for Variant A.
        beta_A: Posterior beta for Variant A.
        alpha_B: Posterior alpha for Variant B.
        beta_B: Posterior beta for Variant B.
        n_samples: Number of Monte Carlo samples.

    Returns:
        Estimated expected loss.
    """
    if (
        alpha_A <= 0
        or beta_A <= 0
        or alpha_B <= 0
        or beta_B <= 0
    ):
        raise ValueError(
            "alpha_A, beta_A, alpha_B, and beta_B must all be positive."
        )

    if not isinstance(n_samples, int):
        raise ValueError("n_samples must be an integer.")

    if n_samples <= 0:
        raise ValueError("n_samples must be greater than 0.")
    samples_A = rng.beta(alpha_A,beta_A,size=n_samples)
    samples_B = rng.beta(alpha_B,beta_B,size=n_samples)
    rng = np.random.default_rng()

    loss = np.maximum(samples_B-samples_A,0)
    return loss.mean()


def convergence_check(alpha_A: float,
    beta_A: float,
    alpha_B: float,
    beta_B: float,
    ) -> None:
    """
    Plot the convergence of the Monte Carlo estimate for P(B > A).

    Args:
        alpha_A: Posterior alpha for Variant A.
        beta_A: Posterior beta for Variant A.
        alpha_B: Posterior alpha for Variant B.
        beta_B: Posterior beta for Variant B.
    """
    if (
        alpha_A <= 0
        or beta_A <= 0
        or alpha_B <= 0
        or beta_B <= 0
    ):
        raise ValueError(
            "alpha_A, beta_A, alpha_B, and beta_B must all be positive."
        )

    sample_sizes = [
    100,
    500,
    1000,
    5000,
    10000,
    50000,
    100000,
]
    estimates = []

    for n in sample_sizes:
        estimate = prob_B_beats_A(
            alpha_A,
            beta_A,
            alpha_B,
            beta_B,
            n_samples=n,
        )
        estimates.append(estimate)
    plt.plot(sample_sizes, estimates)
    plt.xlabel("Number of Monte Carlo Samples")
    plt.ylabel("Estimated P(B > A)")
    plt.title("Monte Carlo Convergence")
    plt.show()