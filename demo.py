from pprint import pprint

from src.ab_framework import ABTestFramework
from src.comparison import comparison_plot


def main():

    # ==========================================================
    # Example Experiment
    # ==========================================================

    n_A = 1000
    conv_A = 120

    n_B = 1000
    conv_B = 145

    prior_A = (1.0, 1.0)
    prior_B = (1.0, 1.0)

    # ==========================================================
    # Create Framework
    # ==========================================================

    framework = ABTestFramework(n_samples=100000)

    # ==========================================================
    # Run Complete Analysis
    # ==========================================================

    results = framework.run_full_analysis(
        n_A=n_A,
        conv_A=conv_A,
        n_B=n_B,
        conv_B=conv_B,
        prior_A=prior_A,
        prior_B=prior_B,
    )

    # ==========================================================
    # Frequentist Results
    # ==========================================================

    print("\n" + "=" * 60)
    print("FREQUENTIST RESULTS")
    print("=" * 60)

    pprint(results["frequentist"])

    # ==========================================================
    # Bayesian Results
    # ==========================================================

    print("\n" + "=" * 60)
    print("BAYESIAN RESULTS")
    print("=" * 60)

    pprint(results["bayesian"])

    # ==========================================================
    # Monte Carlo Results
    # ==========================================================

    print("\n" + "=" * 60)
    print("MONTE CARLO RESULTS")
    print("=" * 60)

    pprint(results["monte_carlo"])

    # ==========================================================
    # Recommendation
    # ==========================================================

    print("\n" + "=" * 60)
    print("FINAL RECOMMENDATION")
    print("=" * 60)

    pprint(results["recommendation"])

    # ==========================================================
    # Complete Dictionary
    # ==========================================================

    print("\n" + "=" * 60)
    print("COMPLETE RESULTS DICTIONARY")
    print("=" * 60)

    pprint(results)

    # ==========================================================
    # Plotly Dashboard
    # ==========================================================

    fig = comparison_plot(results)

    fig.show()


if __name__ == "__main__":
    main()
