import streamlit as st
import math
import matplotlib.pyplot as plt

st.set_page_config(page_title="Industrial Energy AI", layout="wide")

st.title("⚡ Industrial Compressor Sizing & Optimization AI")
st.caption("Version 4 – Machine Based Sizing + Leakage Analysis")

# -------------------------------
# SECTION 1: MACHINE BASED SIZING
# -------------------------------

st.header("🏭 Compressor Sizing (Machine Based)")

unit = st.selectbox("Select Flow Unit", ["CFM", "Nm3/hr"])

num_machines = st.slider("Number of Machines", 1, 10, 3)

total_cfm = 0
pressures = []

for i in range(num_machines):
    col1, col2 = st.columns(2)
    with col1:
        cfm = st.selectbox(
            f"Machine {i+1} Air (CFM)",
            list(range(10, 305, 5)),
            key=f"cfm{i}"
        )
    with col2:
        pressure = st.selectbox(
            f"Machine {i+1} Pressure (bar)",
            list(range(4, 11)),
            key=f"p{i}"
        )

    total_cfm += cfm
    pressures.append(pressure)

avg_pressure = sum(pressures) / len(pressures)

# Convert to Nm3/hr
if unit == "CFM":
    flow = total_cfm * 1.7
else:
    flow = total_cfm

efficiency = st.slider("Compressor Efficiency", 0.5, 0.95, 0.75)

# Power Calculation
power = (flow * avg_pressure * math.log(avg_pressure/1)) / (36.7 * efficiency)

specific_power = power / total_cfm if total_cfm > 0 else 0

st.subheader("📊 Sizing Results")

st.write(f"Total Air Demand: {total_cfm} CFM")
st.write(f"Average Pressure: {round(avg_pressure,2)} bar")
st.write(f"Required Compressor Power: {round(power,2)} kW")
st.write(f"Specific Power: {round(specific_power,3)} kW/CFM")

# -------------------------------
# SECTION 2: LEAKAGE ANALYSIS
# -------------------------------

st.header("💨 Leakage Analysis")

leak_size = st.selectbox(
    "Leak Hole Size (mm)",
    [round(0.1 + i*0.2, 1) for i in range(20)]
)

pressure_leak = st.slider("Leak Pressure (bar)", 4, 10, 7)

area = math.pi * (leak_size / 1000) ** 2 / 4

# Practical leakage estimation
leak_cfm = area * 10000 * math.sqrt(pressure_leak) * 2118

cost_per_kwh = st.slider("Power Cost ₹/kWh", 5, 15, 5)

leak_power = leak_cfm * 0.1
annual_hours = 8000

leak_cost = leak_power * annual_hours * cost_per_kwh

st.subheader("📉 Leakage Results")

st.write(f"Leakage Air Loss: {round(leak_cfm,2)} CFM")
st.write(f"Power Loss: {round(leak_power,2)} kW")
st.write(f"Annual Cost Loss: ₹ {round(leak_cost,0)}")

# -------------------------------
# SECTION 3: TOTAL ENERGY COST
# -------------------------------

st.header("💰 Energy Cost Analysis")

total_power = power + leak_power
total_energy = total_power * annual_hours
total_cost = total_energy * cost_per_kwh

st.write(f"Total Power (with leakage): {round(total_power,2)} kW")
st.write(f"Annual Energy Cost: ₹ {round(total_cost,0)}")

# -------------------------------
# SECTION 4: AI ADVISOR
# -------------------------------

st.header("🤖 AI Advisor")

if leak_size > 1:
    st.warning("⚠ Major leakage detected – urgent repair required")

if specific_power > 0.12:
    st.warning("⚠ High specific power – inefficient system")

if avg_pressure > 7:
    st.warning("⚠ High pressure setting – reduce if possible")

saving = total_cost * 0.2

st.success(f"💰 Potential Saving: ₹ {round(saving,0)} per year")

# -------------------------------
# SECTION 5: GRAPH
# -------------------------------

st.header("📈 Efficiency vs Power")

eff_range = [0.6, 0.65, 0.7, 0.75, 0.8, 0.85]
energy_list = []

for e in eff_range:
    p = (flow * avg_pressure * math.log(avg_pressure/1)) / (36.7 * e)
    energy_list.append(p)

plt.figure()
plt.plot(eff_range, energy_list, marker='o')
plt.xlabel("Efficiency")
plt.ylabel("Power (kW)")
plt.title("Efficiency Impact on Power")

st.pyplot(plt)
