import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
	
# --- 1. Model Parameters ---
r = 0.05        # Intrinsic growth rate of the fish population
K = 11715       # Carrying capacity of the environment
q = 0.001       # Catchability coefficient
p = 40          # Price per unit catch
c = 150         # Cost per unit of fishing effort
days = 90       # Length of the fishing season in days
P0 = [9080]     # Initial fish population
	
# Effort parameters
#E_min = 10
#E_max = 100
E_min = 5
E_max = 50
	
# Periodic Cost Parameters: C(t) = C0 + A*sin(omega*t + phi)
C0 = c        # Baseline average cost per unit effort
A = 50          # Amplitude of cost fluctuation
omega = 12 * np.pi / days # Angular frequency (1 full cycle per 90-day season)
phi = 0         # Phase shift (starts at baseline cost)
	
# --- 2. Time-Dependent Functions ---
def E(t):
    """Fishing effort function."""
    return E_min + (E_max - E_min) * np.sin(np.pi * t / days)
	
def C(t):
    """Periodic cost per unit effort function."""
    return C0 + A * np.sin(omega * t + phi)
	
# --- 3. Differential Equation for Population ---
def population_model(t, P):
    return r * P * (1 - P / K) - q * P * E(t)
	
# --- 4. Solving the Model ---
t_span = (0, days)
t_eval = np.linspace(0, days, 500)
solution = solve_ivp(population_model, t_span, P0, t_eval=t_eval)
	
time = solution.t
population = solution.y[0]
effort = E(time)
cost_per_effort = C(time)
	
# --- 5. Economic Model ---
# Profit per unit catch: pi_catch = p - C(t) / (q * P)
profit_per_catch = p - cost_per_effort / (q * population)
	
# --- 6. Visualization ---
	
# --- Plot 1: Cost per Unit Effort vs. Profit per Unit Catch ---
fig1, ax1 = plt.subplots(figsize=(10, 6))
	
color1 = 'tab:purple'
ax1.set_xlabel('Time (Days)')
ax1.set_ylabel('Cost per Unit Effort ($)', color=color1)
ax1.plot(time, cost_per_effort, color=color1, linewidth=2, label='Cost C(t)')
ax1.tick_params(axis='y', labelcolor=color1)
ax1.grid(True, alpha=0.3)
	
ax2 = ax1.twinx()
color2 = 'tab:green'
ax2.set_ylabel('Profit per Unit Catch ($)', color=color2)
ax2.plot(time, profit_per_catch, color=color2, linestyle='--', linewidth=2, label='Profit Margin')
ax2.tick_params(axis='y', labelcolor=color2)
	
plt.title('Bioeconomic Model: Cost vs. Profit per Catch')
fig1.tight_layout()
plt.show()
	
# --- Plot 2: Fish Population vs. Profit per Unit Catch ---
fig2, ax3 = plt.subplots(figsize=(10, 6))
	
color3 = 'tab:blue'
ax3.set_xlabel('Time (Days)')
ax3.set_ylabel('Fish Population (P)', color=color3)
ax3.plot(time, population, color=color3, linewidth=2, label='Fish Population')
ax3.tick_params(axis='y', labelcolor=color3)
ax3.grid(True, alpha=0.3)
	
ax4 = ax3.twinx()
color4 = 'tab:green'
ax4.set_ylabel('Profit per Unit Catch ($)', color=color4)
ax4.plot(time, profit_per_catch, color=color4, linestyle='--', linewidth=2, label='Profit Margin')
ax4.tick_params(axis='y', labelcolor=color4)
	
plt.title('Bioeconomic Model: Fish Population vs. Profit per Catch')
fig2.tight_layout()
plt.show()