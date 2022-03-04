# Value at Risk

In this demo, we demonstrate how crypto hodlers can modernize their risk management practices by efficiently scaling their Monte Carlo simulations from tens of thousands up to millions by leveraging both the flexibility of cloud compute and the robustness of Apache Spark. We use Databricks, which helps accelerate model development lifecycle by bringing both the transparency of experiments and the reliability in data, bridging the gap between science and engineering and enabling investors to have a more robust yet agile approach to risk management. The data used is crypto data from Yahoo Finance (through `yfinance` library) for a top 20 crypto portfolio.

## Value at risk

VaR is measure of potential loss at a specific confidence interval. A VAR statistic has three components: a time period, a confidence level and a loss amount (or loss percentage). What is the most I can - with a 95% or 99% level of confidence - expect to lose in dollars over the next month? There are 3 ways to compute Value at risk
# 

+ **Historical Method**: The historical method simply re-organizes actual historical returns, putting them in order from worst to best.
+ **The Variance-Covariance Method**: This method assumes that stock returns are normally distributed and use pdf instead of actual returns.
+ **Monte Carlo Simulation**: This method involves developing a model for future stock price returns and running multiple hypothetical trials.

We report in below example a simple Value at risk calculation for a synthetic instrument, given a volatility (i.e. standard deviation of instrument returns) and a time horizon (365 days). **What is the most I could lose in 300 days with a 95% confidence?**