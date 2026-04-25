import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
	
# --- 1. Model Parameters ---
r = 0.05        # Intrinsic growth rate of the fish population
K = 11715       # Carrying capacity of the environment	
q = 0.001       # Catchability coefficient (proportionality constant)
p = 40          # Price per unit catch
c = 150         # Cost per unit of fishing effort
days = 90       # Length of the fishing season in days
P0 = [9080]     # Initial fish population
	
# --- 2. Defining the Effort Function E(t) ---
# The problem specifies effort is a fixed amount at the beginning/end 
# and maximum at midseason. A sine wave is a smooth way to model this.
#E_min = 10  # Baseline effort
#E_max = 100 # Maximum midseason effort
E_min = 5
E_max = 50
	
def E(t):
# Peaks at t = 45 days (midseason)
    return E_min + (E_max - E_min) * np.sin(np.pi * t / days)
	
# --- 3. Differential Equation for Population ---
# dP/dt = r*P*(1 - P/K) - q*P*E(t)
def population_model(t, P):
    dP_dt = r * P * (1 - P / K) - q * P * E(t)
    return dP_dt
	
# --- 4. Solving the Model ---
t_span = (0, days)
t_eval = np.linspace(0, days, 500) # 500 points for a smooth plot

# Solve the Ordinary Differential Equation (ODE)
solution = solve_ivp(population_model, t_span, P0, t_eval=t_eval)

time = solution.t
population = solution.y[0]
effort = E(time)
	
# --- 5. Economic Model ---
# Profit per unit catch: pi_catch = p - c / (q * P)
# Note: As population P drops, the cost to catch a single unit increases.
profit_per_catch = p - c / (q * population)
	
# Total profit rate over time (Profit per catch * Total catch rate)
catch_rate = q * population * E(time)
total_profit_rate = profit_per_catch * catch_rate
	
# --- 6. Visualization ---
# Fish Population and Effort
fig, ax1 = plt.subplots(figsize=(10, 6))
	
# Plot Fish Population on primary y-axis
color1 = 'tab:blue'
ax1.set_xlabel('Time (Days)')
ax1.set_ylabel('Fish Population (P)', color=color1)
ax1.plot(time, population, color=color1, linewidth=2, label='Fish Population')
ax1.tick_params(axis='y', labelcolor=color1)
ax1.grid(True, alpha=0.3)
	
# Plot Fishing Effort on secondary y-axis
ax2 = ax1.twinx()
color2 = 'tab:red'
ax2.set_ylabel('Fishing Effort (E)', color=color2)
ax2.plot(time, effort, color=color2, linestyle='-.', linewidth=2, label='Effort E(t)')
ax2.tick_params(axis='y', labelcolor=color2)

plt.title('Bioeconomic Model: Fish Population vs. Fishing Effort Over Time')
fig.tight_layout()
plt.savefig('population_vs_effort.png')
	
# Fish Population and Profit
fig, ax1 = plt.subplots(figsize=(10, 6))
	
# Plot Fish Population
color1 = 'tab:blue'
ax1.set_xlabel('Time (Days)')
ax1.set_ylabel('Fish Population (P)', color=color1)
ax1.plot(time, population, color=color1, linewidth=2, label='Fish Population')
ax1.tick_params(axis='y', labelcolor=color1)
ax1.grid(True, alpha=0.3)
	
# Create a second y-axis to plot Profit per Unit Catch
ax2 = ax1.twinx()
color2 = 'tab:green'
ax2.set_ylabel('Profit per Unit Catch ($)', color=color2)
ax2.plot(time, profit_per_catch, color=color2, linestyle='--', linewidth=2, label='Profit / Catch')
ax2.tick_params(axis='y', labelcolor=color2)
	
# Add title and show plot
plt.title('Bioeconomic Model: Fish Population vs. Profit Margins Over a 90-Day Season')
fig.tight_layout()
plt.show()