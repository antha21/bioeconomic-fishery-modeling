import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
	
# --- 1. Biological & Harvesting Parameters ---
r = 0.05
K = 11715
q = 0.001
c = 150
days = 90
P0 = [9080]
	
E_min = 5
E_max = 50
	
def E(t):
    return E_min + (E_max - E_min) * np.sin(np.pi * t / days)
	
# --- 2. Differential Equation for Population ---
def population_model(t, P):
    return r * P * (1 - P / K) - q * P * E(t)
	
# Solve Biological Model (Only needs to be solved once)
N_steps = 500
t_span = (0, days)
t_eval = np.linspace(0, days, N_steps)
solution = solve_ivp(population_model, t_span, P0, t_eval=t_eval)
	
time = solution.t
population = solution.y[0]
	
# --- 3. Geometric Brownian Motion Parameters ---
p0 = 40
mu = 0.02
sigma = 0.15
dt = days / (N_steps - 1)
	
# --- 4. Plotting Two 3x2 Grids ---
# Set up two separate figures
fig1, axes1 = plt.subplots(3, 2, figsize=(15, 12), constrained_layout=True)
fig2, axes2 = plt.subplots(3, 2, figsize=(15, 12), constrained_layout=True)
	
# Flatten the 3x2 array of axes for easy iteration
axes1 = axes1.flatten()
axes2 = axes2.flatten()

# We are intentionally NOT using a random seed here so every run is unique
for i in range(6):
    # Generate independent Brownian motion path
    dW = np.random.normal(0, np.sqrt(dt), N_steps)
    W = np.cumsum(dW)
    W[0] = 0
	
    # Calculate stochastic price p(t)
    price = p0 * np.exp((mu - 0.5 * sigma**2) * time + sigma * W)
	
    # Calculate resulting profit per catch
    profit_per_catch = price - c / (q * population)
	
# ---------------------------------------------------------
# Plotting Figure 1: Market Price vs. Profit
# ---------------------------------------------------------
    ax1_price = axes1[i]
    color_price = 'tab:orange'
    ax1_price.plot(time, price, color=color_price, linewidth=2)
    ax1_price.set_ylabel('Market Price ($)', color=color_price)
    ax1_price.tick_params(axis='y', labelcolor=color_price)
    ax1_price.set_xlabel('Time (Days)')
    ax1_price.grid(True, alpha=0.3)
	
    ax1_profit = ax1_price.twinx()
    color_profit = 'tab:green'
    ax1_profit.plot(time, profit_per_catch, color=color_profit, linestyle='--', linewidth=2)
    ax1_profit.set_ylabel('Profit Margin ($)', color=color_profit)
    ax1_profit.tick_params(axis='y', labelcolor=color_profit)
    ax1_price.set_title(f'Realization {i+1}: Price vs. Profit Margin')
	
# ---------------------------------------------------------
# Plotting Figure 2: Fish Population vs. Profit
# ---------------------------------------------------------
    ax2_pop = axes2[i]
    color_pop = 'tab:blue'
    ax2_pop.plot(time, population, color=color_pop, linewidth=2)
    ax2_pop.set_ylabel('Fish Population (P)', color=color_pop)
    ax2_pop.tick_params(axis='y', labelcolor=color_pop)
    ax2_pop.set_xlabel('Time (Days)')
    ax2_pop.grid(True, alpha=0.3)
	
    ax2_profit = ax2_pop.twinx()
    ax2_profit.plot(time, profit_per_catch, color=color_profit, linestyle='--', linewidth=2)
    ax2_profit.set_ylabel('Profit Margin ($)', color=color_profit)
    ax2_profit.tick_params(axis='y', labelcolor=color_profit)
    ax2_pop.set_title(f'Realization {i+1}: Population vs. Profit Margin')
	
# Final layout adjustments for Figure 1
fig1.suptitle('Bioeconomic Model: 6 Realizations of Stochastic Market Price vs. Profit', fontsize=16)
plt.show()
	
# Final layout adjustments for Figure 2
fig2.suptitle('Bioeconomic Model: 6 Realizations of Fish Population vs. Profit', fontsize=16)
plt.show()
