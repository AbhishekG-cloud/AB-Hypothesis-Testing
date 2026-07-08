from scipy.stats import beta as be


class BayesianABTest:
    def __init__(
        self,
        prior_params_A: tuple[float, float] = (1.0, 1.0),
        prior_params_B: tuple[float, float] = (1.0, 1.0),
    ) -> None:
        """
        Initialize a Bayesian A/B Test with prior Beta distributions.
        """

        for alpha, beta in (prior_params_A, prior_params_B):
            if alpha <= 0 or beta <= 0:
                raise ValueError(
                    "Beta distribution parameters must be positive."
                )

        self.prior_params_A = tuple(prior_params_A)
        self.prior_params_B = tuple(prior_params_B)

        self.posterior_params_A = tuple(prior_params_A)
        self.posterior_params_B = tuple(prior_params_B)

    def update(
        self,
        visitors_A: int,
        conversions_A: int,
        visitors_B: int,
        conversions_B: int,
    ) -> None:
        """
        Update the posterior distributions for Variant A and Variant B
        using one batch of observed A/B test data.
        """

        for visitors, conversions in (
            (visitors_A, conversions_A),
            (visitors_B, conversions_B),
        ):
            if visitors < 0:
                raise ValueError("Visitors cannot be negative.")

            if conversions < 0:
                raise ValueError("Conversions cannot be negative.")

            if conversions > visitors:
                raise ValueError(
                    "Conversions cannot exceed visitors."
                )

        alpha_A, beta_A = self.posterior_params_A
        alpha_B, beta_B = self.posterior_params_B

        alpha_A += conversions_A
        beta_A += visitors_A - conversions_A

        alpha_B += conversions_B
        beta_B += visitors_B - conversions_B

        self.posterior_params_A = (alpha_A, beta_A)
        self.posterior_params_B = (alpha_B, beta_B)

    def update_sequential(
        self,
        daily_data: list[tuple[int, int, int, int]],
    ) -> None:
        """
        Sequentially update the posterior distributions using multiple
        batches of A/B test data.
        """

        for (
            visitors_A,
            conversions_A,
            visitors_B,
            conversions_B,
        ) in daily_data:
            self.update(
                visitors_A,
                conversions_A,
                visitors_B,
                conversions_B,
            )

    def get_posterior_summary(self) -> dict:
        """
        Return summary statistics for the current posterior distributions.
        """

        alpha_A, beta_A = self.posterior_params_A
        alpha_B, beta_B = self.posterior_params_B

        mean_A = alpha_A / (alpha_A + beta_A)
        mean_B = alpha_B / (alpha_B + beta_B)

        mode_A = (
            (alpha_A - 1) / (alpha_A + beta_A - 2)
            if alpha_A > 1 and beta_A > 1
            else None
        )

        mode_B = (
            (alpha_B - 1) / (alpha_B + beta_B - 2)
            if alpha_B > 1 and beta_B > 1
            else None
        )

        lower_A = be.ppf(0.025, alpha_A, beta_A)
        upper_A = be.ppf(0.975, alpha_A, beta_A)

        lower_B = be.ppf(0.025, alpha_B, beta_B)
        upper_B = be.ppf(0.975, alpha_B, beta_B)

        return {
            "A": {
                "posterior_params": self.posterior_params_A,
                "mean": mean_A,
                "mode": mode_A,
                "credible_interval": (lower_A, upper_A),
            },
            "B": {
                "posterior_params": self.posterior_params_B,
                "mean": mean_B,
                "mode": mode_B,
                "credible_interval": (lower_B, upper_B),
            },
        }