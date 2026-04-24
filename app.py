import streamlit as st
import math
import matplotlib.pyplot as plt

st.set_page_config(page_title="Industrial Energy AI", layout="wide")

st.title("⚡ Industrial Energy Optimization AI")
st.markdown("### 🏭 Compressor + Energy Audit Dashboard (Version 8)")

# -------------------------------
# MACHINE SIZING
# -------------------------------

st.header("🏭 Compressor Sizing")

num_machines = st.slider("Number of Machines", 1, 10, 3)

total_cfm = 0

for i in range(num_machines):
    st.subheader(f"Machine {i+1}")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        cfm = st.selectbox(f"Air Requirement (CFM)", list(range(10, 305, 5)), key=f"cfm{i}")
        
    with col2:
        mode = st.selectbox(f"Mode", ["Continuous", "Intermittent"], key=f"mode{i}")
        
    with col3:
        if mode == "Continuous":
            effective_cfm = cfm
        else:
            on = st.slider(f"ON Time (sec)", 1, 60, 10, key=f"on{i}")
            cycle = st.slider(f"Cycle Time (sec)", 1, 60, 20, key=f"cycle{i}")
            effective_cfm = cfm * (on / cycle)

    total_cfm += effective_cfm
    st.write(f"Effective Load: {round(effective_cfm,2)} CFM")

# -------------------------------
# THERMODYNAMIC POWER
# -------------------------------

st.header("⚙ Compressor Power")

p1 = st.number_input("Inlet Pressure (bar)", value=1.0)
p2 = st.number_input("Discharge Pressure (bar)", value=7.0)

flow = total_cfm * 1.7
Q = flow / 3600
k = 1.4

if p2 <= p1:
    st.error("Discharge pressure must be higher than inlet pressure")
    power = 0
else:
    power = (k/(k-1)) * (p1*100000) * Q * ((p2/p1)**((k-1)/k) - 1) / 1000

specific_power = power / total_cfm if total_cfm > 0 else 0

# -------------------------------
# MOTOR + PF
# -------------------------------

st.header("🔌 Motor & Power Factor")

V = st.number_input("Voltage (V)", value=415)
I = st.number_input("Current (A)", value=50)
pf = st.slider("Power Factor", 0.5, 1.0, 0.8)

motor_power = 1.732 * V * I * pf / 1000

# PF correction
target_pf = st.slider("Target PF", 0.85, 0.99, 0.95)

tan1 = math.sqrt(1/pf**2 - 1)
tan2 = math.sqrt(1/target_pf**2 - 1)

Qc = motor_power * (tan1 - tan2)

# -------------------------------
# LEAKAGE
# -------------------------------

st.header("💨 Leakage Audit")

num_leaks = st.slider("Number of Leakage Points", 1, 20, 3)

total_leak = 0

for i in range(num_leaks):
    col1, col2 = st.columns(2)
    
    with col1:
        size = st.selectbox(f"Leak Size (mm)", [round(0.1+j*0.2,1) for j in range(20)], key=f"l{i}")
        
    with col2:
        count = st.number_input(f"No. of Points", 1, 20, 1, key=f"c{i}")

    area = math.pi * (size/1000)**2 / 4
    leak = area * 10000 * math.sqrt(p2) * 2118
    
    total_leak += leak * count

loss_percent = (total_leak / total_cfm)*100 if total_cfm>0 else 0

# -------------------------------
# ENERGY COST
# -------------------------------

st.header("💰 Energy & Cost")

cost = st.number_input("Electricity Cost ₹/kWh", value=6)
hours = st.number_input("Operating Hours/year", value=8000)

leak_power = total_leak * 0.1

total_power = power + leak_power
total_cost = total_power * hours * cost

saving = total_cost * 0.2

# -------------------------------
# KPI DASHBOARD (TOP)
# -------------------------------

st.header("📊 Key Performance Indicators")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Air Demand (CFM)", round(total_cfm,1))
col2.metric("Power (kW)", round(power,1))
col3.metric("Leakage (%)", round(loss_percent,1))
col4.metric("Annual Cost (₹)", round(total_cost,0))

# -------------------------------
# STATUS
# -------------------------------

if loss_percent > 20:
    st.error("🚨 High Leakage – Immediate Action Required")
elif loss_percent > 10:
    st.warning("⚠ Moderate Leakage")
else:
    st.success("✔ Leakage under control")

# -------------------------------
# RESULTS
# -------------------------------

st.header("📊 Detailed Results")

st.write(f"Compressor Power: {round(power,2)} kW")
st.write(f"Specific Power: {round(specific_power,3)} kW/CFM")
st.write(f"Motor Power: {round(motor_power,2)} kW")
st.write(f"Required Capacitor: {round(Qc,2)} kVAr")

st.write(f"Total Leakage: {round(total_leak,2)} CFM ({round(loss_percent,1)}%)")
st.write(f"Annual Energy Cost: ₹ {round(total_cost,0)}")

# -------------------------------
# EXECUTIVE SUMMARY
# -------------------------------

st.header("📢 Executive Summary")

st.info(f"""
Your plant is consuming ₹ {round(total_cost,0)} annually in compressed air energy.

Key losses identified:
- Leakage: {round(loss_percent,1)}%
- System inefficiency

Estimated saving potential:
👉 ₹ {round(saving,0)} per year

Recommended actions:
✔ Fix leakage immediately  
✔ Improve power factor  
✔ Optimize compressor loading  
✔ Reduce pressure setting  
✔ Consider energy-efficient compressor  
""")

st.success("💡 This tool can reduce energy cost by 15–30% annually.")

# -------------------------------
# GRAPH
# -------------------------------

st.header("📈 Efficiency Impact")

eff_range = [0.6, 0.7, 0.8, 0.9]
power_list = [power/e if e>0 else 0 for e in eff_range]

plt.figure()
plt.plot(eff_range, power_list, marker='o')
plt.xlabel("Efficiency")
plt.ylabel("Power (kW)")
st.pyplot(plt)
