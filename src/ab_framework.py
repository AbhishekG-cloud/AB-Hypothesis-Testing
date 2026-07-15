from src.frequentist_tests import two_proportion_ztest
from src.BaysianABtest import BayesianABTest
from src.monte_carlo import (
    prob_B_beats_A,
    expected_uplift,
    expected_loss,
)


class ABTestFramework:


    def __init__(self, n_samples: int = 100000) -> None:
        """
        Initialize framework configuration.

        Parameters
        ----------
        n_samples : int, default=100000
            Number of Monte Carlo samples used in Bayesian
            simulation-based metrics.
        """

        if n_samples <= 0:
            raise ValueError(
                "n_samples must be greater than zero."
            )

        self.n_samples = n_samples
    
    def _generate_recommendation(
    self,
    frequentist_results: dict,
    probability_superiority: float,
    expected_loss: float,
    ) -> dict:
    

        frequentist_significant = (
            frequentist_results["decision"] == "Reject H0"
        )

        if (
            frequentist_significant
            and probability_superiority >= 0.95
            and expected_loss <= 0.001
        ):
            return {
                "recommendation": "Launch Variant B",
                "reason":
                    "Frequentist significance achieved, Bayesian confidence is high, and expected loss is negligible.",
            }

        elif (
            not frequentist_significant
            and probability_superiority < 0.80
        ):
            return {
                "recommendation": "Keep Variant A",
                "reason":
                    "Neither Frequentist nor Bayesian evidence supports Variant B.",
            }

        else:
            return {
                "recommendation": "Continue Experiment",
                "reason":
                    "Current evidence is inconclusive. Collect more data.",
            }
    

    def run_full_analysis(
            self,
            n_A: int,
            conv_A: int,
            n_B: int,
            conv_B: int,
            prior_A: tuple[float, float] = (1.0, 1.0),prior_B: tuple[float, float] = (1.0, 1.0),
            ) -> dict:
        

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
        frequentist_results= two_proportion_ztest(n_A=n_A,conv_A=conv_A,n_B=n_B,conv_B=conv_B)
        bayes_model = BayesianABTest(prior_params_A=prior_A,prior_params_B=prior_B,)
        bayes_model.update(visitors_A=n_A,conversions_A=conv_A,visitors_B=n_B,conversions_B=conv_B)
        bayes_results = bayes_model.get_posterior_summary()
        alpha_A,beta_A = bayes_results["A"]["posterior_params"]
        alpha_B, beta_B = bayes_results["B"]["posterior_params"]
       
        probability_superiority = prob_B_beats_A(alpha_A,beta_A,alpha_B,beta_B,n_samples=self.n_samples,)
        uplift = expected_uplift(alpha_A,beta_A,alpha_B,beta_B,n_samples=self.n_samples,)
        loss = expected_loss(alpha_A,beta_A,alpha_B,beta_B,n_samples=self.n_samples,)
        recommendation = self._generate_recommendation(
            frequentist_results=frequentist_results,
            probability_superiority=probability_superiority,
            expected_loss=loss,)

        results = {
        "frequentist": frequentist_results,
        "bayesian": bayes_results,
        "monte_carlo": {
        "probability_B_beats_A": probability_superiority,
        "expected_uplift": uplift,
        "expected_loss": loss,
            },
        "recommendation": recommendation,
        }
        return results