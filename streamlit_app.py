import json
import streamlit as st
import pandas as pd
from io import StringIO
from src.BaysianABtest import BayesianABTest

from src.ab_framework import ABTestFramework
from src.comparison import comparison_plots


# ---------------------------------------------------------
# Page Configuration
# ---------------------------------------------------------

st.set_page_config(
    page_title="Bayesian A/B Testing Framework",
    page_icon="📊",
    layout="wide"
)

st.title("📊 Bayesian A/B Testing Framework")

st.write(
    """
Compare two product variants using Frequentist and Bayesian
statistical analysis.
"""
)

# ---------------------------------------------------------
# Sidebar
# ---------------------------------------------------------

st.sidebar.header("Experiment Settings")

visitors_A = st.sidebar.number_input(
    "Visitors (A)",
    min_value=1,
    value=1000,
)

visitors_B = st.sidebar.number_input(
    "Visitors (B)",
    min_value=1,
    value=1000,
)

conversions_A = st.sidebar.number_input(
    "Conversions (A)",
    min_value=0,
    value=52,
)

conversions_B = st.sidebar.number_input(
    "Conversions (B)",
    min_value=0,
    value=61,
)

PRIORS = {
    "Uniform": (1.0, 1.0),
    "Jeffreys": (0.5, 0.5),
    "Informative": (5.0, 5.0),
}

prior_name_A = st.sidebar.selectbox(
    "Prior A",
    list(PRIORS.keys()),
    key="prior_A"
)

prior_name_B = st.sidebar.selectbox(
    "Prior B",
    list(PRIORS.keys()),
    key="prior_B"
)

prior_A = PRIORS[prior_name_A]
prior_B = PRIORS[prior_name_B]

st.sidebar.subheader("Decision Thresholds")

alpha = st.sidebar.slider(
    "Frequentist α",
    min_value=0.01,
    max_value=0.10,
    value=0.05,
    step=0.01,
)

probability_threshold = st.sidebar.slider(
    "Bayesian Probability Threshold",
    min_value=0.50,
    max_value=0.99,
    value=0.95,
    step=0.01,
)

loss_threshold = st.sidebar.number_input(
    "Maximum Expected Loss",
    min_value=0.0000,
    max_value=0.0100,
    value=0.0010,
    step=0.0001,
    format="%.4f",
)


# ---------------------------------------------------------
# Validation
# ---------------------------------------------------------

if conversions_A > visitors_A:
    st.error("Conversions (A) cannot exceed Visitors (A).")
    st.stop()

if conversions_B > visitors_B:
    st.error("Conversions (B) cannot exceed Visitors (B).")
    st.stop()

# ---------------------------------------------------------
# Run Analysis
# ---------------------------------------------------------

framework = ABTestFramework()

results = framework.run_full_analysis(
    n_A=visitors_A,
    conv_A=conversions_A,
    n_B=visitors_B,
    conv_B=conversions_B,
    prior_A=prior_A,
    prior_B=prior_B,
    alpha=alpha,
    probability_threshold=probability_threshold,
    loss_threshold=loss_threshold,
)

# ---------------------------------------------------------
# Tabs
# ---------------------------------------------------------
st.subheader("Decision Thresholds")

thresholds = results["thresholds"]

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "α",
        f"{thresholds['alpha']:.2f}"
    )

with col2:
    st.metric(
        "Probability Threshold",
        f"{thresholds['probability_threshold']:.0%}"
    )

with col3:
    st.metric(
        "Max Expected Loss",
        f"{thresholds['loss_threshold']:.4%}"
    )

tab1, tab2, tab3, tab4, tab5 = st.tabs(
    [
        "Summary",
        "Analysis",
        "Frequentist vs Bayesian",
        "Visualization",
        "Sequential Analysis"
    ]
)

# =========================================================
# SUMMARY
# =========================================================

with tab1:

    st.header("Experiment Summary")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Conversion Rate A",
            f"{conversions_A / visitors_A:.2%}"
        )

    with col2:
        st.metric(
            "Conversion Rate B",
            f"{conversions_B / visitors_B:.2%}"
        )

    st.divider()

    st.subheader("Posterior Means")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Posterior Mean A",
            f"{results['bayesian']['A']['mean']:.2%}"
        )

    with col2:
        st.metric(
            "Posterior Mean B",
            f"{results['bayesian']['B']['mean']:.2%}"
        )

    st.divider()

    st.subheader("Recommendation")

    recommendation = results["recommendation"]

    if recommendation["recommendation"] == "Launch Variant B":
        st.success(f"✅ {recommendation['recommendation']}")

    elif recommendation["recommendation"] == "Keep Variant A":
        st.warning(f"⚠️ {recommendation['recommendation']}")

    else:
        st.info(recommendation["recommendation"])

    st.info(recommendation["reason"])

# =========================================================
# ANALYSIS
# =========================================================

with tab2:

    st.header("Frequentist Analysis")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "P-value",
            f"{results['frequentist']['p_value']:.4f}"
        )

    with col2:
        st.metric(
            "Z Statistic",
            f"{results['frequentist']['z_statistic']:.4f}"
        )

    ci_low, ci_high = results["frequentist"]["confidence_interval"]

    st.write(
        f"95% Confidence Interval: ({ci_low:.4f}, {ci_high:.4f})"
    )

    if results["frequentist"]["p_value"] < alpha:
        st.success(
            "Difference is statistically significant."
        )
    else:
        st.warning(
            "Difference is NOT statistically significant."
        )

    st.divider()

    st.header("Bayesian Analysis")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "P(B > A)",
            f"{results['monte_carlo']['probability_B_beats_A']:.2%}"
        )

    with col2:
        st.metric(
            "Expected Lift",
            f"{results['monte_carlo']['expected_uplift']:.2%}"
        )

    with col3:
        st.metric(
            "Expected Loss",
            f"{results['monte_carlo']['expected_loss']:.4%}"
        )
# =========================================================
# FREQUENTIST VS BAYESIAN
# =========================================================

with tab3:

    st.header("Frequentist vs Bayesian")

    comparison_data = {
        "Metric": [
            "Question Answered",
            "Confidence Measure",
            "Decision"
        ],
        "Frequentist": [
            "Is the observed difference statistically significant?",
            f"P-value = {results['frequentist']['p_value']:.4f}",
            results["frequentist"]["decision"]
        ],
        "Bayesian": [
            "What is the probability B is better than A?",
            f"P(B>A) = {results['monte_carlo']['probability_B_beats_A']:.2%}",
            results["recommendation"]["recommendation"]
        ]
    }

    st.table(comparison_data)
# =========================================================
# VISUALIZATION
# =========================================================

with tab4:

    st.header("Interactive Dashboard")

    fig = comparison_plots(results)

    st.plotly_chart(
        fig,
        use_container_width=True
    )
# ---------------------------------------------------------
# Sequential Bayesian Updating
# ---------------------------------------------------------
with tab5:

    st.header("Sequential Bayesian Updating")
    csv_text = st.text_area(
    "Paste daily data (CSV)",
    height=200,
    placeholder="""day,n_A,conv_A,n_B,conv_B
    1,1000,52,1000,61
    2,980,49,1005,58
    3,1020,56,995,64"""
    )
    if csv_text.strip():

        df = pd.read_csv(StringIO(csv_text))

        st.subheader("Input Data")

        st.dataframe(df)
        required_columns = [
        "day",
        "n_A",
        "conv_A",
        "n_B",
        "conv_B"
]

    missing = set(required_columns) - set(df.columns)

    if missing:
        st.error(
            f"Missing columns: {', '.join(missing)}"
        )
        st.stop()
    history = []

    bayes_model = BayesianABTest(
    prior_params_A=prior_A,
    prior_params_B=prior_B
        
)       
    for _, row in df.iterrows():

        bayes_model.update(
            visitors_A=int(row["n_A"]),
            conversions_A=int(row["conv_A"]),
            visitors_B=int(row["n_B"]),
            conversions_B=int(row["conv_B"])
        )

        summary = bayes_model.get_posterior_summary()

        history.append({
            "Day": row["day"],
            "Posterior Mean A": summary["A"]["mean"],
            "Posterior Mean B": summary["B"]["mean"]
        })
    history_df = pd.DataFrame(history)

    st.subheader("Posterior Evolution")

    st.dataframe(history_df)
    
    st.line_chart(
    history_df.set_index("Day")[
        ["Posterior Mean A", "Posterior Mean B"]
    ]
)
# ---------------------------------------------------------
# Raw Results
# ---------------------------------------------------------

st.divider()

with st.expander("Raw Results Dictionary"):

    st.json(results)

# ---------------------------------------------------------
# Download
# ---------------------------------------------------------

st.download_button(
    label="⬇ Download Results (JSON)",
    data=json.dumps(results, indent=4, default=str),
    file_name="ab_test_results.json",
    mime="application/json",
)
with st.expander("📚 Methodology"):

    st.markdown("""
### Z-Statistic
Measures how many standard errors separate the observed difference from the null hypothesis.

### P-value
Probability of observing data this extreme (or more) if there is actually no difference.

### Confidence Interval
A range of plausible values for the true difference in conversion rates.

### Posterior Mean
The Bayesian estimate of the conversion rate after combining prior beliefs with observed data.

### P(B > A)
The probability that Variant B has a higher conversion rate than Variant A.

### Expected Uplift
The expected increase in conversion rate if Variant B is deployed.

### Expected Loss
The expected regret of choosing Variant B when it is actually not the better variant.
""")