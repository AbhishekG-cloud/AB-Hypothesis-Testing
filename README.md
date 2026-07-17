# 📊 Bayesian A/B Testing Framework

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)]()
[![Streamlit](https://img.shields.io/badge/Streamlit-App-red.svg)]()
[![License](https://img.shields.io/badge/License-MIT-green.svg)]()
[![Status](https://img.shields.io/badge/Status-Active-success.svg)]()

## 🚀 Live Demo

🌐 **Streamlit App**

https://ab-hypothesis-testing-w49ahrcng6znrcci6wg8o6.streamlit.app/

📂 **GitHub Repository**

https://github.com/AbhishekG-cloud/AB-Hypothesis-Testing
---

# Project Summary

The **Bayesian A/B Testing Framework** is an end-to-end statistical experimentation platform that combines **Frequentist hypothesis testing**, **Bayesian inference**, and **Monte Carlo simulation** into a single interactive application.

Unlike traditional A/B testing tools that rely solely on p-values, this framework provides probabilistic business insights such as:

* Probability that Variant B outperforms Variant A
* Expected uplift after deployment
* Expected loss (regret)
* Business-oriented deployment recommendations

The project is built with a modular architecture, making it suitable for both learning Bayesian statistics and demonstrating production-oriented software engineering practices.

---
## ✨ Key Highlights

- Built a complete Bayesian & Frequentist A/B Testing framework from scratch.
- Combined hypothesis testing, Bayesian inference, and Monte Carlo simulation.
- Interactive Streamlit dashboard with real-time statistical analysis.
- Modular architecture designed for extensibility and reuse.
- Deployed publicly on Streamlit Community Cloud.
---

# Why Bayesian A/B Testing?

Traditional hypothesis testing answers:

> **"Is there sufficient evidence to reject the null hypothesis?"**

Bayesian A/B testing answers:

> **"Given the observed data, how likely is Variant B to be better than Variant A?"**

This probabilistic interpretation is often more intuitive for product managers and business stakeholders.

Example:

Frequentist Result:

* p-value = 0.07

Bayesian Result:

* Probability(B > A) = 96%

Although the Frequentist test is not statistically significant at α = 0.05, Bayesian analysis indicates a high probability that Variant B performs better.

This richer decision-making process is one of the major motivations for Bayesian experimentation.

---

# Features

## Frequentist Analysis

* Two-Proportion Z-Test
* p-value
* Confidence Interval
* Z Statistic
* Statistical Decision

## Bayesian Analysis

* Beta-Binomial Conjugate Model
* Posterior Distribution
* Posterior Mean
* Posterior Variance
* Posterior Mode
* Credible Interval
* Highest Density Interval (HDI)

## Monte Carlo Simulation

* Probability(B > A)
* Expected Uplift
* Expected Loss
* Posterior Predictive Sampling

## Decision Engine

Business recommendation system using:

* Frequentist significance
* Bayesian probability
* Expected loss

Possible recommendations:

* 🟢 Launch Variant B
* 🟡 Continue Experiment
* 🔴 Keep Variant A

## Interactive Dashboard

* Streamlit interface
* Sidebar controls
* Interactive Plotly visualizations
* Sequential Bayesian updates
* Frequentist vs Bayesian comparison
* Download results as JSON

---

# Mathematical Background

## Frequentist Testing

The framework performs a Two-Proportion Z-Test.

Metrics reported:

* Conversion Rate
* Standard Error
* Z Statistic
* p-value
* Confidence Interval

Decision Rule:

* Reject H₀ if p-value < α

---

## Bayesian Updating

The conversion rate is modeled as

[
\theta \sim Beta(\alpha,\beta)
]

After observing conversions,

[
\theta | Data \sim Beta(\alpha + Successes,; \beta + Failures)
]

The posterior distribution is then used to estimate:

* Posterior Mean
* Credible Interval
* Probability of Superiority

---

## Monte Carlo Simulation

Posterior samples are generated from both variants.

Using these samples the framework estimates:

* P(B > A)
* Expected Uplift
* Expected Loss

These metrics support practical deployment decisions beyond hypothesis testing.

---

# Project Architecture

```text
Bayesian-AB-Testing/

├── app/
│   └── streamlit_app.py
│
├── notebooks/
│   ├── 01_frequentist_analysis.ipynb
│   ├── 02_bayesian_core.ipynb
│   ├── 03_monte_carlo_decisions.ipynb
│   └── 04_full_pipeline_demo.ipynb
│
├── src/
│   ├── ab_framework.py
│   ├── bayesian_engine.py
│   ├── frequentist_tests.py
│   ├── monte_carlo.py
│   ├── comparison.py
│   └── data_simulator.py
│
├── tests/
│
├── requirements.txt
│
└── README.md
```

---

# Framework Workflow

```text
User Input

        │

        ▼

Streamlit Dashboard

        │

        ▼

ABTestFramework

        │

 ┌──────┼────────┐

 ▼      ▼        ▼

Frequentist  Bayesian  Monte Carlo

        │

        ▼

Unified Results Dictionary

        │

        ▼

Decision Recommendation

        │

        ▼

Interactive Dashboard
```

---

# Streamlit Dashboard

The dashboard allows users to:

* Input visitors and conversions
* Select Bayesian priors
* Configure statistical thresholds
* Compare Frequentist and Bayesian analyses
* Visualize posterior distributions
* Perform sequential Bayesian updates
* Download experiment results

---

# Sequential Bayesian Updating

The dashboard supports sequential experiments by processing daily observations.

Users can:

* Paste CSV data
* Update posteriors day-by-day
* Track posterior evolution over time

This demonstrates how Bayesian inference naturally incorporates new evidence without restarting the analysis.

---

# Installation

Clone the repository

```bash
git clone https://github.com/AbhishekG-cloud/AB-Hypothesis-Testing.git
```

Move into the project

```bash
cd <repository>
```

Create a virtual environment

```bash
python -m venv .venv
```

Activate the environment

### Windows

```bash
.venv\Scripts\activate
```

### Linux / macOS

```bash
source .venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

# Run the Application

```bash
streamlit run app/streamlit_app.py
```

The application will open automatically in your browser.

---

# Example Experiment

| Metric          | Variant A | Variant B |
| --------------- | --------: | --------: |
| Visitors        |      1000 |      1000 |
| Conversions     |        52 |        61 |
| Conversion Rate |      5.2% |      6.1% |

Example outputs:

* p-value = 0.0699
* Probability(B>A) = 96.46%
* Expected Uplift ≈ 1.8%
* Expected Loss ≈ Very Small

Recommendation:

**Launch Variant B**

---

# Screenshots



## Dashboard

<img width="959" height="416" alt="image" src="https://github.com/user-attachments/assets/4d089d9d-a25d-4f65-a759-2a271e69eee6" />


---

## Frequentist vs Bayesian

<img width="959" height="415" alt="image" src="https://github.com/user-attachments/assets/710d9133-e94a-4ea1-95bc-da7e90154ef3" />


---

## Frequentist vs Bayesian Comparison

<img width="950" height="411" alt="image" src="https://github.com/user-attachments/assets/1234148e-7d0d-4f37-bbd3-b000bf7d275c" />


---

## Sequential Analysis

<img width="956" height="416" alt="image" src="https://github.com/user-attachments/assets/f089d817-920b-4fbe-818e-ef9728188cc3" />


---

# Testing

The project includes:

* Unit tests
* Input validation
* Edge case handling

Edge cases tested:

* Zero conversions
* Full conversions
* Equal conversion rates
* Large sample sizes
* Invalid inputs

---

# Future Improvements

Potential extensions include:

* Thompson Sampling
* Multi-armed Bandits
* CUPED variance reduction
* Hierarchical Bayesian models
* Sequential stopping rules
* Power analysis dashboard
* Real-time experiment monitoring
* FastAPI REST API
* Docker deployment
* CI/CD pipeline

---

# Technologies Used

* Python
* NumPy
* SciPy
* Pandas
* Plotly
* Streamlit
* Matplotlib

---

# Learning Outcomes

This project demonstrates practical understanding of:

* Bayesian Statistics
* Frequentist Hypothesis Testing
* Monte Carlo Simulation
* Statistical Decision Making
* Software Architecture
* Interactive Data Applications
* Modular Python Development
* Data Visualization

---

# Acknowledgements

This project was developed as part of a comprehensive study of Bayesian statistics and A/B testing, with the goal of building a production-style experimentation framework suitable for portfolio demonstration and real-world analytics workflows.

---

# License

This project is released under the MIT License.

