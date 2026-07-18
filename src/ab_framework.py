from src.frequentist_tests import two_proportion_ztest
from src.BaysianABtest import BayesianABTest
from src.monte_carlo import (
    prob_B_beats_A,
    expected_uplift,
    expected_loss,
)
from src.config import (
    DEFAULT_MONTE_CARLO_SAMPLES,
    DEFAULT_ALPHA,
    DEFAULT_EXPECTED_LOSS_THRESHOLD,
    DEFAULT_PROBABILITY_THRESHOLD,
)


class ABTestFramework:
    """Coordinate Frequentist, Bayesian, and Monte Carlo A/B testing analyses.

    This class serves as the orchestration layer for the A/B testing framework.
    It combines hypothesis testing, Bayesian posterior estimation, Monte Carlo
    simulation, and decision logic into a unified analysis pipeline.
    """

    def __init__(self, n_samples: int = DEFAULT_MONTE_CARLO_SAMPLES) -> None:
        """
        Initialize the A/B testing framework.

        Configures the number of Monte Carlo simulations used for Bayesian
        probability estimates and expected value calculations.

        Args:
            n_samples:
                Number of Monte Carlo samples used for simulation-based
                Bayesian metrics.

        Raises:
            ValueError:
                If ``n_samples`` is less than or equal to zero.
        """

        if n_samples <= 0:
            raise ValueError("n_samples must be greater than zero.")

        self.n_samples = n_samples

    def _generate_recommendation(
        self,
        frequentist_results: dict,
        probability_superiority: float,
        expected_loss: float,
        alpha=DEFAULT_ALPHA,
        probability_threshold=DEFAULT_PROBABILITY_THRESHOLD,
        loss_threshold=DEFAULT_EXPECTED_LOSS_THRESHOLD,
    ) -> dict:
        """
        Generate a recommendation by combining Frequentist and Bayesian evidence.

        The recommendation is based on statistical significance from the
        Frequentist hypothesis test together with Bayesian decision metrics,
        including the posterior probability that Variant B outperforms
        Variant A and the expected opportunity loss.

        Args:
            frequentist_results:
                Dictionary containing the output of the Frequentist
                two-proportion z-test.

            probability_superiority:
                Posterior probability that Variant B performs better than
                Variant A.

            expected_loss:
                Expected opportunity loss incurred by selecting
                Variant B.

            alpha:
                Significance level used for the Frequentist hypothesis test.

            probability_threshold:
                Minimum posterior probability required before recommending
                deployment of Variant B.

            loss_threshold:
                Maximum acceptable expected loss for recommending
                Variant B.

        Returns:
            Dictionary containing the recommendation decision and a
            human-readable explanation.

        Mathematical Notes:
            The decision combines two statistical paradigms.

            Frequentist evidence is evaluated using

                p-value < alpha

            Bayesian evidence is evaluated using

                P(B > A)

            estimated through Monte Carlo sampling from the posterior
            Beta distributions.

            Variant B is recommended only if:

            - the Frequentist hypothesis test is statistically significant,
            - the posterior superiority probability exceeds the specified
              threshold, and
            - the expected opportunity loss is below the acceptable limit.

            Otherwise, the framework recommends either continuing the
            experiment or retaining Variant A based on the available
            evidence.
        """

        frequentist_significant = frequentist_results["p_value"] < alpha

        if (
            frequentist_significant
            and probability_superiority >= probability_threshold
            and expected_loss <= loss_threshold
        ):
            return {
                "recommendation": "Launch Variant B",
                "reason": (
                    f"p-value ({frequentist_results['p_value']:.4f}) "
                    f"is below α={alpha:.2f}, "
                    f"P(B>A)={probability_superiority:.2%} exceeds "
                    f"{probability_threshold:.0%}, "
                    f"and expected loss "
                    f"({expected_loss:.4%}) is below "
                    f"{loss_threshold:.4%}."
                ),
            }

        elif (
            not frequentist_significant
        ) and probability_superiority < probability_threshold:
            return {
                "recommendation": "Keep Variant A",
                "reason": (
                    f"Evidence is insufficient. "
                    f"p-value={frequentist_results['p_value']:.4f}, "
                    f"P(B>A)={probability_superiority:.2%}."
                ),
            }

        return {
            "recommendation": "Continue Experiment",
            "reason": (
                "Current evidence is inconclusive. " "Continue collecting data."
            ),
        }

    def run_full_analysis(
        self,
        n_A,
        conv_A,
        n_B,
        conv_B,
        prior_A,
        prior_B,
        alpha=0.05,
        probability_threshold=0.95,
        loss_threshold=0.001,
    ):
        """
        Execute the complete A/B testing analysis pipeline.

        This method performs a unified analysis by combining Frequentist
        hypothesis testing, Bayesian posterior updating, Monte Carlo
        estimation, and automated recommendation generation.

        Args:
            n_A:
                Total number of visitors assigned to Variant A.

            conv_A:
                Number of conversions observed for Variant A.

            n_B:
                Total number of visitors assigned to Variant B.

            conv_B:
                Number of conversions observed for Variant B.

            prior_A:
                Beta prior parameters ``(alpha, beta)`` for Variant A.

            prior_B:
                Beta prior parameters ``(alpha, beta)`` for Variant B.

            alpha:
                Significance level used by the Frequentist hypothesis test.

            probability_threshold:
                Minimum posterior probability required to recommend
                launching Variant B.

            loss_threshold:
                Maximum acceptable expected opportunity loss when selecting
                Variant B.

        Returns:
            A dictionary containing:

            - Frequentist hypothesis test results.
            - Bayesian posterior summaries.
            - Monte Carlo decision metrics.
            - Final recommendation.
            - Decision thresholds used during analysis.

        Raises:
            ValueError:
                If sample sizes are non-positive.

            ValueError:
                If conversion counts are negative.

            ValueError:
                If conversions exceed the number of visitors.

            ValueError:
                If prior distributions do not contain exactly two positive
                parameters.

            ValueError:
                If the significance level is not between 0 and 1.

        Workflow:
            1. Validate all user inputs.
            2. Perform the Frequentist two-proportion z-test.
            3. Update Bayesian posterior distributions.
            4. Estimate posterior metrics using Monte Carlo simulation.
            5. Generate a recommendation by combining statistical evidence.
            6. Return a unified results dictionary.

        Mathematical Notes:
            The Frequentist analysis evaluates the null hypothesis

                H₀: p_A = p_B

            using a two-proportion z-test.

            Bayesian inference updates Beta priors according to

                Beta(alpha, beta)

            with observed conversion data to obtain posterior
            distributions.

            Monte Carlo sampling from the posterior distributions
            estimates:

            - P(B > A)
            - Expected uplift
            - Expected opportunity loss

            These metrics are combined with the Frequentist test
            to produce the final recommendation.
        """

        # Sample sizes must be positive
        if n_A <= 0 or n_B <= 0:
            raise ValueError("Sample sizes must be positive.")

        # Conversions cannot be negative
        if conv_A < 0 or conv_B < 0:
            raise ValueError("Conversions cannot be negative.")

        # Conversions cannot exceed sample size
        if conv_A > n_A:
            raise ValueError("conv_A cannot exceed n_A.")

        if conv_B > n_B:
            raise ValueError("conv_B cannot exceed n_B.")

        # Priors must have two positive values
        if len(prior_A) != 2 or len(prior_B) != 2:
            raise ValueError("Each prior must contain exactly two values.")

        if prior_A[0] <= 0 or prior_A[1] <= 0:
            raise ValueError("prior_A values must be positive.")

        if prior_B[0] <= 0 or prior_B[1] <= 0:
            raise ValueError("prior_B values must be positive.")

        if alpha <= 0 or alpha > 1:
            raise ValueError("must be betweeb 0 and 1")

        frequentist_results = two_proportion_ztest(
            n_A=n_A,
            conv_A=conv_A,
            n_B=n_B,
            conv_B=conv_B,
        )

        bayes_model = BayesianABTest(
            prior_params_A=prior_A,
            prior_params_B=prior_B,
        )

        bayes_model.update(
            visitors_A=n_A,
            conversions_A=conv_A,
            visitors_B=n_B,
            conversions_B=conv_B,
        )

        bayes_results = bayes_model.get_posterior_summary()

        alpha_A, beta_A = bayes_results["A"]["posterior_params"]
        alpha_B, beta_B = bayes_results["B"]["posterior_params"]

        probability_superiority = prob_B_beats_A(
            alpha_A,
            beta_A,
            alpha_B,
            beta_B,
            n_samples=self.n_samples,
        )

        uplift = expected_uplift(
            alpha_A,
            beta_A,
            alpha_B,
            beta_B,
            n_samples=self.n_samples,
        )

        loss = expected_loss(
            alpha_A,
            beta_A,
            alpha_B,
            beta_B,
            n_samples=self.n_samples,
        )

        recommendation = self._generate_recommendation(
            frequentist_results=frequentist_results,
            probability_superiority=probability_superiority,
            expected_loss=loss,
            alpha=alpha,
            probability_threshold=probability_threshold,
            loss_threshold=loss_threshold,
        )

        results = {
            "frequentist": frequentist_results,
            "bayesian": bayes_results,
            "monte_carlo": {
                "probability_B_beats_A": probability_superiority,
                "expected_uplift": uplift,
                "expected_loss": loss,
            },
            "recommendation": recommendation,
            "thresholds": {
                "alpha": alpha,
                "probability_threshold": probability_threshold,
                "loss_threshold": loss_threshold,
            },
        }

        return results
