import streamlit as st
import math
import matplotlib.pyplot as plt

st.set_page_config(page_title="Industrial Energy AI", layout="wide")

st.title("⚡ Industrial Compressor Sizing & Optimization AI")
st.caption("Version 4.1 – Intermittent Load + Multi-Point Leakage")

# -------------------------------
# MACHINE BASED SIZING
# -------------------------------

st.header("🏭 Compressor Sizing (Machine Based)")

num_machines = st.slider("Number of Machines", 1, 10, 3)

total_cfm = 0
pressures = []

for i in range(num_machines):
    st.subheader(f"Machine {i+1}")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        cfm = st.selectbox(
            f"Air Requirement (CFM)",
            list(range(10, 305, 5)),
            key=f"cfm{i}"
        )
        
    with col2:
        pressure = st.selectbox(
            f"Pressure (bar)",
            list(range(4, 11)),
            key=f"p{i}"
        )
        
    with col3:
        mode = st.selectbox(
            f"Operation Mode",
            ["Continuous", "Intermittent"],
            key=f"mode{i}"
        )

    if mode == "Continuous":
        effective_cfm = cfm
    else:
        on_time = st.slider(f"ON Time (sec)", 1, 60, 10, key=f"on{i}")
        cycle_time = st.slider(f"Cycle Time (sec)", 1, 60, 20, key=f"cycle{i}")
        duty = on_time / cycle_time
        effective_cfm = cfm * duty

    total_cfm += effective_cfm
    pressures.append(pressure)

avg_pressure = sum(pressures) / len(pressures)

flow = total_cfm * 1.7  # convert to Nm3/hr

efficiency = st.slider("Compressor Efficiency", 0.5, 0.95, 0.75)

power = (flow * avg_pressure * math.log(avg_pressure/1)) / (36.7 * efficiency)

specific_power = power / total_cfm if total_cfm > 0 else 0

st.subheader("📊 Sizing Results")

st.write(f"Effective Air Demand: {round(total_cfm,2)} CFM")
st.write(f"Required Power: {round(power,2)} kW")
st.write(f"Specific Power: {round(specific_power,3)} kW/CFM")

# -------------------------------
# MULTI-POINT LEAKAGE
# -------------------------------

st.header("💨 Leakage Audit (Multiple Points)")

num_leaks = st.slider("Number of Leakage Points", 1, 20, 3)

total_leak_cfm = 0

pressure_leak = st.slider("System Pressure (bar)", 4, 10, 7)

for i in range(num_leaks):
    col1, col2 = st.columns(2)
    
    with col1:
        leak_size = st.selectbox(
            f"Leak {i+1} Size (mm)",
            [round(0.1 + j*0.2,1) for j in range(20)],
            key=f"leak{i}"
        )
        
    with col2:
        count = st.number_input(f"No. of points", 1, 50, 1, key=f"count{i}")

    area = math.pi * (leak_size/1000)**2 / 4
    
    leak_cfm = area * 10000 * math.sqrt(pressure_leak) * 2118
    
    total_leak_cfm += leak_cfm * count

# Cost calculation
cost_per_kwh = st.slider("Power Cost ₹/kWh", 5, 15, 5)
annual_hours = 8000

leak_power = total_leak_cfm * 0.1
leak_cost = leak_power * annual_hours * cost_per_kwh

st.subheader("📉 Leakage Results")

st.write(f"Total Leakage: {round(total_leak_cfm,2)} CFM")
st.write(f"Power Loss: {round(leak_power,2)} kW")
st.write(f"Annual Leakage Cost: ₹ {round(leak_cost,0)}")

# -------------------------------
# TOTAL ENERGY
# -------------------------------

st.header("💰 Total Energy Analysis")

total_power = power + leak_power
total_energy = total_power * annual_hours
total_cost = total_energy * cost_per_kwh

st.write(f"Total Power: {round(total_power,2)} kW")
st.write(f"Annual Cost: ₹ {round(total_cost,0)}")

# -------------------------------
# AI ADVISOR
# -------------------------------

st.header("🤖 AI Advisor")

if total_leak_cfm > 50:
    st.warning("⚠ High leakage detected – immediate action required")

if specific_power > 0.12:
    st.warning("⚠ System inefficient – check compressor selection")

if avg_pressure > 7:
    st.warning("⚠ Pressure too high – reduce if possible")

saving = total_cost * 0.2

st.success(f"💰 Potential Saving: ₹ {round(saving,0)} per year")

# -------------------------------
# GRAPH
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
plt.title("Efficiency Impact")

st.pyplot(plt)
