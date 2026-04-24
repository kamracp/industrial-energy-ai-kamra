import streamlit as st
import math
import matplotlib.pyplot as plt

st.set_page_config(page_title="Industrial Energy AI", layout="wide")

st.title("⚡ Industrial Compressor Sizing AI – Pro Version")

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

# Corrected Flow
actual_flow = flow * (1 + leakage/100)

# Pipe velocity (approx)
area = math.pi * (pipe_dia/1000)**2 / 4
velocity = (actual_flow/3600) / area

# Pipe pressure loss (simplified)
rho = 1.2
f = 0.02
dp = f * (pipe_length/(pipe_dia/1000)) * (rho * velocity**2 / 2) / 100000  # bar

# Effective pressure
effective_pressure = pressure + dp

# Power
power = (actual_flow * effective_pressure * math.log(effective_pressure/1)) / (36.7 * efficiency)

# Annual cost
annual_energy = power * hours
annual_cost = annual_energy * cost

# --- Results ---
st.subheader("📊 Results")

st.write(f"Corrected Flow: {round(actual_flow,2)} Nm3/hr")
st.write(f"Pipe Pressure Loss: {round(dp,3)} bar")
st.write(f"Required Compressor Power: {round(power,2)} kW")
st.write(f"Annual Energy Cost: ₹ {round(annual_cost,0)}")

# --- AI Advisor ---
st.subheader("🤖 AI Advisor")

if leakage > 15:
    st.warning("⚠ High leakage – potential loss ₹ " + str(int(annual_cost*0.15)))

if dp > 0.5:
    st.warning("⚠ High pipe loss – increase pipe diameter")

if efficiency < 0.7:
    st.warning("⚠ Low efficiency – consider VFD compressor")

if pressure > 7:
    st.warning("⚠ High pressure – reduce setpoint")

saving = annual_cost * 0.2
st.success(f"💰 Potential Saving: ₹ {round(saving,0)} per year")

# --- Graph ---
st.subheader("📈 Energy vs Efficiency")

eff_range = [0.6, 0.65, 0.7, 0.75, 0.8, 0.85]
energy_list = []

for e in eff_range:
    p = (actual_flow * effective_pressure * math.log(effective_pressure/1)) / (36.7 * e)
    energy_list.append(p)

plt.figure()
plt.plot(eff_range, energy_list, marker='o')
plt.xlabel("Efficiency")
plt.ylabel("Power (kW)")
plt.title("Efficiency vs Power Consumption")

st.pyplot(plt)
