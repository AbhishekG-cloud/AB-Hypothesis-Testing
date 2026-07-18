def update_posterior(
    alpha_prior: float,
    beta_prior: float,
    conversion: int,
    visitors: int,
) -> tuple[float, float]:
    """
    Update the parameters of a Beta posterior distribution.

    Computes the posterior Beta distribution after observing binary
    conversion data using the Beta-Binomial conjugate relationship.

    Args:
        alpha_prior:
            Alpha parameter of the prior Beta distribution.

        beta_prior:
            Beta parameter of the prior Beta distribution.

        conversion:
            Number of observed conversions (successes).

        visitors:
            Total number of observed visitors (trials).

    Returns:
        A tuple ``(alpha_post, beta_post)`` representing the updated
        posterior Beta distribution parameters.

    Raises:
        ValueError:
            If the number of conversions is negative.

        ValueError:
            If the number of visitors is negative.

        ValueError:
            If conversions exceed the number of visitors.

        ValueError:
            If either prior parameter is not positive.

    Mathematical Notes:
        Given a prior distribution

            Beta(alpha_prior, beta_prior)

        and observing

            conversion successes
            visitors - conversion failures,

        the posterior distribution is

            Beta(
                alpha_prior + conversion,
                beta_prior + visitors - conversion
            )

        This update follows directly from the conjugacy between the
        Beta prior and the Binomial likelihood.
    """
    if conversion < 0:
        raise ValueError("Conversions cannot be negative.")

    if visitors < 0:
        raise ValueError("Visitors cannot be negative.")

    if conversion > visitors:
        raise ValueError("Conversions cannot exceed visitors.")

    if alpha_prior <= 0 or beta_prior <= 0:
        raise ValueError("Alpha and beta must be positive.")

    alpha_post = alpha_prior + conversion
    beta_post = beta_prior + visitors - conversion

    return (alpha_post, beta_post)


def posterior_mean(alpha: float, beta: float) -> float:
    """
    Compute the mean of a Beta posterior distribution.

    Args:
        alpha:
            Alpha parameter of the Beta distribution.

        beta:
            Beta parameter of the Beta distribution.

    Returns:
        The posterior mean, representing the expected conversion rate.

    Raises:
        ValueError:
            If either Beta distribution parameter is not positive.

    Mathematical Notes:
        For a Beta distribution

            Beta(alpha, beta)

        the posterior mean is

            alpha / (alpha + beta)

        which is the expected value of the underlying conversion
        probability.
    """
    if alpha <= 0 or beta <= 0:
        raise ValueError("Alpha and beta must be positive.")

    mean = alpha / (alpha + beta)
    return mean


def posterior_varinace(alpha: float, beta: float) -> float:
    """
    Compute the variance of a Beta posterior distribution.

    Args:
        alpha:
            Alpha parameter of the Beta distribution.

        beta:
            Beta parameter of the Beta distribution.

    Returns:
        The posterior variance of the conversion rate.

    Raises:
        ValueError:
            If either Beta distribution parameter is not positive.

    Mathematical Notes:
        For a Beta distribution

            Beta(alpha, beta)

        the variance is

            (alpha × beta) /
            ((alpha + beta)^2 × (alpha + beta + 1))

        This measures the uncertainty associated with the estimated
        conversion probability.
    """
    if alpha <= 0 or beta <= 0:
        raise ValueError("Alpha and beta must be positive.")

    var = (alpha * beta) / (((alpha + beta) ** 2) * (alpha + beta + 1))
    return var
