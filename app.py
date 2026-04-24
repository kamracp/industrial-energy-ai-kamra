import streamlit as st
import math
import matplotlib.pyplot as plt

st.set_page_config(page_title="Industrial Energy AI", layout="wide")

st.title("⚡ Industrial Energy AI – Compressor + Energy Audit Tool")
st.caption("Version 7 – Full Industrial Model")

# -------------------------------
# 1. MACHINE BASED SIZING
# -------------------------------

st.header("🏭 Compressor Sizing (Machine Based)")

num_machines = st.slider("Number of Machines", 1, 10, 3)

total_cfm = 0

for i in range(num_machines):
    st.subheader(f"Machine {i+1}")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        cfm = st.selectbox(f"CFM", list(range(10, 305, 5)), key=f"cfm{i}")
        
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

st.success(f"Total Air Demand: {round(total_cfm,2)} CFM")

# -------------------------------
# 2. THERMODYNAMIC POWER
# -------------------------------

st.header("⚙ Thermodynamic Compressor Power")

p1 = st.number_input("Inlet Pressure (bar)", value=1.0)
p2 = st.number_input("Discharge Pressure (bar)", value=7.0)

if p2 <= p1:
    st.error("Discharge pressure must be higher than inlet pressure")

flow = total_cfm * 1.7  # Nm3/hr
Q = flow / 3600

k = 1.4

power = (k/(k-1)) * (p1*100000) * Q * ((p2/p1)**((k-1)/k) - 1) / 1000

st.write(f"Compressor Power: {round(power,2)} kW")

specific_power = power / total_cfm if total_cfm > 0 else 0
st.write(f"Specific Power: {round(specific_power,3)} kW/CFM")

# -------------------------------
# 3. MOTOR + POWER FACTOR
# -------------------------------

st.header("🔌 Motor & Power Factor Analysis")

V = st.number_input("Voltage (V)", value=415)
I = st.number_input("Current (A)", value=50)
pf = st.slider("Power Factor", 0.5, 1.0, 0.8)

motor_power = 1.732 * V * I * pf / 1000

st.write(f"Motor Input Power: {round(motor_power,2)} kW")

# -------------------------------
# 4. CAPACITOR SIZING
# -------------------------------

st.subheader("⚡ Power Factor Improvement")

target_pf = st.slider("Target PF", 0.85, 0.99, 0.95)

tan_phi1 = math.sqrt(1/pf**2 - 1)
tan_phi2 = math.sqrt(1/target_pf**2 - 1)

Qc = motor_power * (tan_phi1 - tan_phi2)

st.write(f"Required Capacitor: {round(Qc,2)} kVAr")

# -------------------------------
# 5. LEAKAGE AUDIT
# -------------------------------

st.header("💨 Leakage Audit")

num_leaks = st.slider("Leak Points", 1, 20, 3)

total_leak = 0

for i in range(num_leaks):
    col1, col2 = st.columns(2)
    
    with col1:
        size = st.selectbox(f"Leak Size (mm)", [round(0.1+j*0.2,1) for j in range(20)], key=f"l{i}")
        
    with col2:
        count = st.number_input(f"No. of points", 1, 20, 1, key=f"c{i}")

    area = math.pi * (size/1000)**2 / 4
    leak = area * 10000 * math.sqrt(p2) * 2118
    
    total_leak += leak * count

st.write(f"Total Leakage: {round(total_leak,2)} CFM")

loss_percent = (total_leak / total_cfm)*100 if total_cfm>0 else 0
st.error(f"Leakage = {round(loss_percent,1)}% of demand")

# -------------------------------
# 6. TOTAL ENERGY
# -------------------------------

st.header("💰 Energy & Cost")

cost = st.number_input("Electricity Cost ₹/kWh", value=6)
hours = st.number_input("Operating Hours", value=8000)

leak_power = total_leak * 0.1

total_power = power + leak_power
total_cost = total_power * hours * cost

st.write(f"Total Power: {round(total_power,2)} kW")
st.write(f"Annual Cost: ₹ {round(total_cost,0)}")

# -------------------------------
# 7. EFFICIENCY
# -------------------------------

st.header("📊 Efficiency")

eff = power / motor_power if motor_power > 0 else 0

st.write(f"System Efficiency: {round(eff*100,1)} %")

# -------------------------------
# 8. FINAL REPORT
# -------------------------------

st.header("📢 Final Report")

saving = total_cost * 0.2

st.success(f"""
Total Demand: {round(total_cfm,1)} CFM  
Power Required: {round(power,1)} kW  
Motor Power: {round(motor_power,1)} kW  

Leakage: {round(total_leak,1)} CFM ({round(loss_percent,1)}%)  

Annual Cost: ₹ {round(total_cost,0)}  
Saving Potential: ₹ {round(saving,0)}  

Recommended Actions:
✔ Fix leakage  
✔ Improve power factor  
✔ Optimize pressure  
✔ Improve compressor efficiency  
✔ Consider VFD compressor  
""")

# -------------------------------
# GRAPH
# -------------------------------

st.header("📈 Efficiency Curve")

eff_range = [0.6,0.7,0.8,0.9]
power_list = []

for e in eff_range:
    p = power / e
    power_list.append(p)

plt.figure()
plt.plot(eff_range, power_list, marker='o')
plt.xlabel("Efficiency")
plt.ylabel("Power (kW)")
st.pyplot(plt)
