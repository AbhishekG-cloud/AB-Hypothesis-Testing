import numpy as np
from scipy.stats import norm
from statsmodels.stats.proportion import proportions_ztest
from exception import CustomException,InvalidInputError
import sys
import math

def two_proportion_ztest(n_A:int,conv_A:int,n_B:int,conv_B:int,alpha: float = 0.05)->dict:
    """Performs a two-proportion z-test for comparing two independent conversion rates.

    The function computes the z-statistic, two-tailed p-value, confidence
    interval for the difference in proportions, and a statistical decision
    based on the specified significance level.

    Args:
        n_A (int): Total number of observations in group A. Must be greater
            than 0.
        conv_A (int): Number of successful outcomes (conversions) in group A.
            Must satisfy 0 <= conv_A <= n_A.
        n_B (int): Total number of observations in group B. Must be greater
            than 0.
        conv_B (int): Number of successful outcomes (conversions) in group B.
            Must satisfy 0 <= conv_B <= n_B.
        alpha (float, optional): Significance level used for hypothesis
            testing and confidence interval calculation. Must satisfy
            0 < alpha < 1. Defaults to 0.05.

    Returns:
        dict: A dictionary containing:
            - ``z_statistic`` (float): Computed z-test statistic.
            - ``p_value`` (float): Two-tailed p-value.
            - ``confidence_interval`` (tuple[float, float]): Lower and upper
              bounds of the confidence interval for the difference in
              proportions (p_B - p_A).
            - ``decision`` (str): Statistical conclusion ("Reject H0" or
              "Fail to Reject H0").

    Raises:
        InvalidInputError: If any input parameter is outside its valid range.
        CustomException: Wraps any unexpected exception.
    """
    try:
        if n_A <= 0:
            raise InvalidInputError("n_A must be greater than 0.")

        if n_B <= 0:
            raise InvalidInputError("n_B must be greater than 0.")

        if not (0 <= conv_A <= n_A):
            raise InvalidInputError("conv_A must satisfy 0 <= conv_A <= n_A.")

        if not (0 <= conv_B <= n_B):
            raise InvalidInputError("conv_B must satisfy 0 <= conv_B <= n_B.")

        if not (0 < alpha < 1):
            raise InvalidInputError("alpha must satisfy 0 < alpha < 1.")
                
        p_hat_A = conv_A / n_A
        p_hat_B = conv_B / n_B

        difference = p_hat_B - p_hat_A

        p_pool = (conv_A + conv_B) / (n_A + n_B)

        standard_error = np.sqrt(
            p_pool * (1 - p_pool) *
            ((1 / n_A) + (1 / n_B))
        )

        z_statistic = difference / standard_error
        p_value = 2 * (1 - norm.cdf(abs(z_statistic)))
        
        ci_standard_error = np.sqrt(
        (p_hat_A * (1 - p_hat_A)) / n_A
        +
        (p_hat_B * (1 - p_hat_B)) / n_B
        )
        z_critical = norm.ppf(1 - alpha / 2)
        margin = z_critical * ci_standard_error
        lower = difference - margin
        upper = difference + margin
        
        if p_value < alpha:
            decision = "Reject H0"
        else:
            decision = "Fail to Reject H0"



        return {
            "z_statistic": z_statistic,
            "p_value": p_value,
            "confidence_interval": (lower, upper),
            "decision": decision
                }
    except InvalidInputError:
        raise
    except Exception as e:
       raise CustomException(e,sys)


def minimum_sample_size(baseline_rate:float,mde:float,alpha: float = 0.05,
    power: float = 0.8)->int:
    """Estimates the minimum required sample size per group for an A/B test.

    The sample size is computed using the normal approximation based on the
    specified baseline conversion rate, minimum detectable effect (MDE),
    significance level, and desired statistical power.

    Args:
        baseline_rate (float): Expected baseline conversion rate. Must be
            greater than 0.
        mde (float): Minimum detectable effect (absolute difference in
            conversion rates). Must be greater than 0.
        alpha (float): Significance level (Type I error rate). Typically 0.05.
        power (float): Desired statistical power (1 - β). Typically 0.80
            or 0.90.

    Returns:
        int: Minimum required sample size per group, rounded up to the nearest
        whole number.

    Raises:
        InvalidInputError: If ``baseline_rate`` or ``mde`` is not positive.
        CustomException: Wraps any unexpected exception.
    """
    try:
        if baseline_rate <= 0:
            raise InvalidInputError("baseline_rate must be greater than 0.")
        if mde <= 0:
            raise InvalidInputError("mde must be greater than 0.")
        if alpha < 0 or alpha >1 :
            raise InvalidInputError("alpha must be between o and 1 .")
        if power <= 0:
            raise InvalidInputError("power must be greater than 0.")
        

        z_alpha = norm.ppf(1-alpha/2)
        z_beta = norm.ppf(power)

        sample_size = 2*((z_alpha+z_beta)**(2))*(baseline_rate*(1-baseline_rate))/(mde)**2 
        sample_size = math.ceil(sample_size)
        return sample_size
        
          
          
          

    except InvalidInputError:
        raise
    except Exception as e:
       raise CustomException(e,sys)
          