import plotly.graph_objects as go


def comparison_plot(results: dict) -> go.Figure:

    frequentist = results["frequentist"]
    bayesian = results["bayesian"]
    monte = results["monte_carlo"]

    p_value = frequentist["p_value"]

    probability = monte["probability_B_beats_A"]

    uplift = monte["expected_uplift"]

    loss = monte["expected_loss"]

    mean_A = bayesian["A"]["mean"]

    mean_B = bayesian["B"]["mean"]

    fig = go.Figure()

    fig.add_bar(
        name="Posterior Mean",
        x=["Variant A", "Variant B"],
        y=[mean_A, mean_B],
    )

    fig.update_layout(
        title="Bayesian A/B Test Summary",
        xaxis_title="Variant",
        yaxis_title="Conversion Rate",
        barmode="group",
        template="plotly_white",
    )

    return fig


import plotly.graph_objects as go


def comparison_plots(results: dict) -> go.Figure:
    """
    Create an interactive dashboard summarizing the
    Bayesian A/B Test results.

    Parameters
    ----------
    results : dict
        Output returned by ABTestFramework.run_full_analysis().

    Returns
    -------
    go.Figure
        Interactive Plotly dashboard.
    """

    # -----------------------------
    # Extract Frequentist Results
    # -----------------------------
    frequentist = results["frequentist"]

    p_value = frequentist["p_value"]

    # -----------------------------
    # Extract Bayesian Results
    # -----------------------------
    bayesian = results["bayesian"]

    mean_A = bayesian["A"]["mean"]
    mean_B = bayesian["B"]["mean"]

    ci_A = bayesian["A"]["credible_interval"]
    ci_B = bayesian["B"]["credible_interval"]

    # -----------------------------
    # Extract Monte Carlo Results
    # -----------------------------
    monte = results["monte_carlo"]

    probability = monte["probability_B_beats_A"]
    uplift = monte["expected_uplift"]
    loss = monte["expected_loss"]

    # -----------------------------
    # Recommendation
    # -----------------------------
    recommendation = results["recommendation"]["recommendation"]

    # -----------------------------
    # Create Figure
    # -----------------------------
    fig = go.Figure()

    # =====================================================
    # Posterior Mean Bar Plot
    # =====================================================

    fig.add_trace(
        go.Bar(
            x=["Variant A", "Variant B"],
            y=[mean_A, mean_B],
            name="Posterior Mean",
            text=[f"{mean_A:.3f}", f"{mean_B:.3f}"],
            textposition="outside",
            hovertemplate=(
                "<b>%{x}</b><br>" "Posterior Mean: %{y:.4f}" "<extra></extra>"
            ),
        )
    )

    # =====================================================
    # Credible Interval Error Bars
    # =====================================================

    fig.update_traces(
        error_y=dict(
            type="data",
            symmetric=False,
            array=[
                ci_A[1] - mean_A,
                ci_B[1] - mean_B,
            ],
            arrayminus=[
                mean_A - ci_A[0],
                mean_B - ci_B[0],
            ],
        )
    )

    # =====================================================
    # Dashboard Annotations
    # =====================================================

    fig.add_annotation(
        x=1.15,
        y=1.00,
        xref="paper",
        yref="paper",
        align="left",
        showarrow=False,
        bordercolor="black",
        borderwidth=1,
        text=f"<b>Frequentist</b><br>" f"p-value : {p_value:.5f}",
    )

    fig.add_annotation(
        x=1.15,
        y=0.78,
        xref="paper",
        yref="paper",
        align="left",
        showarrow=False,
        bordercolor="black",
        borderwidth=1,
        text=f"<b>Bayesian</b><br>" f"P(B>A) : {probability:.3%}",
    )

    fig.add_annotation(
        x=1.15,
        y=0.56,
        xref="paper",
        yref="paper",
        align="left",
        showarrow=False,
        bordercolor="black",
        borderwidth=1,
        text=f"<b>Expected Uplift</b><br>" f"{uplift:.4%}",
    )

    fig.add_annotation(
        x=1.15,
        y=0.34,
        xref="paper",
        yref="paper",
        align="left",
        showarrow=False,
        bordercolor="black",
        borderwidth=1,
        text=f"<b>Expected Loss</b><br>" f"{loss:.6f}",
    )

    fig.add_annotation(
        x=0.5,
        y=1.18,
        xref="paper",
        yref="paper",
        showarrow=False,
        font=dict(size=18),
        text=f"<b>{recommendation}</b>",
    )

    # =====================================================
    # Layout
    # =====================================================

    fig.update_layout(
        title="Bayesian A/B Testing Dashboard",
        xaxis_title="Variant",
        yaxis_title="Estimated Conversion Rate",
        template="plotly_white",
        width=1000,
        height=600,
        margin=dict(
            l=60,
            r=250,
            t=90,
            b=60,
        ),
    )

    return fig
