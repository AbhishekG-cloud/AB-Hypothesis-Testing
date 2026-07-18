import numpy as np
from scipy.stats import beta as beta_dist
import plotly.graph_objects as go


def beta_mean(alpha: float, beta: float) -> float:
    """
    Return the expected value (mean)  of the Beta distribution.
    """
    if alpha <= 0 or beta <= 0:
        raise ValueError("alpha and beta must be positive.")
    return alpha / (alpha + beta)


def beta_mode(alpha: float, beta: float) -> float:
    """
    Return the most probable value (peak) of the Beta distribution.
    """
    if alpha <= 1 or beta <= 1:
        raise ValueError("alpha and beta must be positive.")
    return (alpha - 1) / (alpha + beta - 2)


def beta_variance(alpha: float, beta: float) -> float:
    """
    Return the uncertainty (spread) of the Beta distribution.
    """
    if alpha <= 0 or beta <= 0:
        raise ValueError("alpha and beta must be positive.")
    return (alpha * beta) / (((alpha + beta) ** 2) * (alpha + beta + 1))


def beta_ci(
    alpha: float, Beta: float, confidence_level: float = 0.95
) -> tuple[float, float]:
    """
    Return the credible interval for a Beta distribution
    """
    if alpha <= 0 or Beta <= 0:
        raise ValueError("alpha and beta must be positive.")
    if confidence_level <= 0 or confidence_level >= 1:
        raise ValueError("Confidence level must be between 0 and 1.")
    tail_prob = (1 - confidence_level) / 2
    lower = beta_dist.ppf(tail_prob, alpha, Beta)
    upper = beta_dist.ppf(1 - tail_prob, alpha, Beta)
    return (lower, upper)


def beta_from_historical(conversions: int, visitors: int) -> tuple[float, float]:
    """
    Convert historical A/B testing data into a Beta prior.
    Parameters
    ----------
    alpha : float
        Alpha shape parameter (> 0)
    beta : float
        Beta shape parameter (> 0)
    label : str
        Label for the plotted distribution.

    Returns
    -------
    Alpha and Beta
    """
    if conversions < 0 or visitors <= 0:
        raise ValueError("alpha and beta must be positive.")
    if conversions > visitors:
        raise ValueError("Conversions can't be greater thne visitors.")

    alpha = conversions + 1
    beta = visitors - conversions + 1
    return (alpha, beta)


def plot_beta(alpha, beta, label):
    """
    Plot a Beta distribution.

    Parameters
    ----------
    alpha : float
        Alpha shape parameter (> 0)
    beta : float
        Beta shape parameter (> 0)
    label : str
        Label for the plotted distribution.

    Returns
    -------
    go.Figure
        Plotly figure containing the Beta distribution.
    """

    # Validate inputs
    if alpha <= 0:
        raise ValueError("alpha must be greater than 0")
    if beta <= 0:
        raise ValueError("beta must be greater than 0")

    x = np.linspace(0, 1, 500)

    if alpha == 1 and beta == 1:
        y = np.ones_like(x)
    else:
        y = beta_dist.pdf(x, alpha, beta)

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=x,
            y=y,
            mode="lines",
            name=label,
        )
    )

    fig.update_layout(
        title=f"Beta Distribution: {label}",
        xaxis_title="Probability",
        yaxis_title="Density",
        template="plotly_white",
    )

    fig.update_yaxes(range=[0, max(y) * 1.1])

    return fig
