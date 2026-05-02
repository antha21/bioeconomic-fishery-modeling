# Profit and Population Dynamics: Bioeconomic Modeling and Real Options Analysis of a Fishery

**Authors:** Anthony Artino and Sarah Decipeda<br>
**Institution:** Kent State University, Department of Mathematical Sciences<br>
**Course:** Modeling Projects (MATH 52039)

## Project Overview
In this project, we model the bioeconomic dynamics of a fish population being harvested and the profit produced from the yield. The population follows logistic growth with harvesting, and profit is measured per unit catch. 

We analyze changes to the economic portion of the model by adjusting the original system to include:
* **Periodic seasonal costs** modeled by a sinusoidal formula.
* **Abrupt cost changes** written as a piecewise constant function.
* **Sudden demand and price increases** following geometric Brownian motion.

Finally, we bridge bioeconomics and quantitative finance by adapting the Black-Scholes Partial Differential Equation (PDE) to mathematically value the fishery as a financial derivative, creating a Real Options valuation for optimal harvesting strategies.

## Technologies Used
* **Python:** Core modeling and simulation.
* **NumPy:** Numerical computations.
* **SciPy (`solve_ivp`):** Solving Ordinary Differential Equations (ODEs).
* **Matplotlib:** 2D and 3D data visualization.

## Repository Structure
* `bioeconomic_fishery_model.py`, `periodic_seasonal_costs.py`, `abrupt_cost_changes.py`, `stochastic_market_price.py`, `black_scholes.py`.
