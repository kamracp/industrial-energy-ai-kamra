import streamlit as st
import math
import matplotlib.pyplot as plt

st.set_page_config(page_title="Industrial Energy AI", layout="wide")

st.title("⚡ Industrial Compressor Optimization AI – Commercial Version")

# Layout
col1, col2 = st.columns(2)

with col1:
    flow = st.number_input("Air Flow (Nm3/hr)", value=1000)
    pressure = st.number_input("Discharge Pressure (bar)", value=7)
    efficiency = st.slider("Efficiency", 0.5, 0.95, 0.75)
    leakage = st.slider("Leakage %", 0, 50, 20)

with col2:
    pipe_length = st.number_input("Pipe Length (m)", value=100)
    pipe_dia = st.number_input("Pipe Diameter (mm)", value=100)
    hours = st.number_input("Operating Hours/year", value=8000)
    cost = st.number_input("Electricity Cost (₹/kWh)", value=8)

# --- Calculations ---

actual_flow = flow * (1 + leakage/100)

area = math.pi * (pipe_dia/1000)**2 / 4
velocity = (actual_flow/3600) / area

rho = 1.2
f = 0.02
dp = f * (pipe_length/(pipe_dia/1000)) * (rho * velocity**2 / 2) / 100000

effective_pressure = pressure + dp

power = (actual_flow * effective_pressure * math.log(effective_pressure/1)) / (36.7 * efficiency)

annual_energy = power * hours
annual_cost = annual_energy * cost

# --- Loss Breakdown ---
leakage_loss = annual_cost * (leakage/100)
pipe_loss_cost = annual_cost * (dp / pressure)

# --- Compressor Selection ---
if power < 75:
    comp_type = "Small Screw Compressor"
elif power < 250:
    comp_type = "Medium Screw Compressor (VFD Recommended)"
else:
    comp_type = "High Capacity Multi-stage Compressor"

# --- ROI ---
investment = power * 8000  # approx ₹ per kW
saving = annual_cost * 0.2
payback = investment / saving if saving > 0 else 0

# --- Results ---
st.subheader("📊 Engineering Results")

st.write(f"Corrected Flow: {round(actual_flow,2)} Nm3/hr")
st.write(f"Pipe Pressure Loss: {round(dp,3)} bar")
st.write(f"Required Power: {round(power,2)} kW")
st.write(f"Annual Energy Cost: ₹ {round(annual_cost,0)}")

# --- Loss ---
st.subheader("💸 Loss Analysis")

st.write(f"Leakage Loss: ₹ {round(leakage_loss,0)}")
st.write(f"Pipe Loss Cost: ₹ {round(pipe_loss_cost,0)}")

# --- Selection ---
st.subheader("🏭 Recommended Equipment")

st.success(f"Recommended: {comp_type}")

# --- ROI ---
st.subheader("📈 ROI Analysis")

st.write(f"Estimated Investment: ₹ {round(investment,0)}")
st.write(f"Annual Saving: ₹ {round(saving,0)}")
st.write(f"Payback Period: {round(payback,1)} years")

# --- CEO SUMMARY ---
st.subheader("📢 CEO Summary")

st.info(f"""
Your plant is consuming approximately ₹ {round(annual_cost,0)} per year in compressed air energy.

Potential saving of ₹ {round(saving,0)} per year is achievable through optimization.

Major losses:
- Leakage: ₹ {round(leakage_loss,0)}
- Piping inefficiency: ₹ {round(pipe_loss_cost,0)}

Recommended Action:
✔ Optimize pressure settings  
✔ Reduce leakage  
✔ Upgrade compressor system  

Estimated Payback: {round(payback,1)} years
""")

# --- Graph ---
st.subheader("📈 Efficiency Impact")

eff_range = [0.6, 0.65, 0.7, 0.75, 0.8, 0.85]
energy_list = []

for e in eff_range:
    p = (actual_flow * effective_pressure * math.log(effective_pressure/1)) / (36.7 * e)
    energy_list.append(p)

plt.figure()
plt.plot(eff_range, energy_list, marker='o')
plt.xlabel("Efficiency")
plt.ylabel("Power (kW)")
plt.title("Efficiency vs Power")

st.pyplot(plt)
