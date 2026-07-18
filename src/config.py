"""
Central configuration for the Bayesian A/B Testing Framework.
"""

# ----------------------------------------------------------
# Priors
# ----------------------------------------------------------

UNIFORM_PRIOR: tuple[float, float] = (1.0, 1.0)
JEFFREYS_PRIOR: tuple[float, float] = (0.5, 0.5)
INFORMATIVE_PRIOR: tuple[float, float] = (5.0, 5.0)

DEFAULT_PRIOR = UNIFORM_PRIOR

PRIORS = {
    "Uniform": UNIFORM_PRIOR,
    "Jeffreys": JEFFREYS_PRIOR,
    "Informative": INFORMATIVE_PRIOR,
}

# ----------------------------------------------------------
# Statistical Thresholds
# ----------------------------------------------------------

DEFAULT_ALPHA = 0.05
DEFAULT_CONFIDENCE_LEVEL = 0.95

DEFAULT_PROBABILITY_THRESHOLD = 0.95
DEFAULT_EXPECTED_LOSS_THRESHOLD = 0.001
DEFAULT_ROPE_THRESHOLD = 0.001

# ----------------------------------------------------------
# Monte Carlo
# ----------------------------------------------------------

DEFAULT_MONTE_CARLO_SAMPLES = 100_000

# ----------------------------------------------------------
# Visualization
# ----------------------------------------------------------

DEFAULT_PAGE_TITLE = "Bayesian A/B Testing Framework"
DEFAULT_PAGE_ICON = "📊"
DEFAULT_LAYOUT = "wide"
