import streamlit as st
import math
import matplotlib.pyplot as plt
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io

st.set_page_config(page_title="Industrial Energy AI", layout="wide")

st.title("⚡ Industrial Compressor Optimization AI")
st.caption("Version 5 – Selection + Report + Advanced Logic")

# -------------------------------
# MACHINE SIZING
# -------------------------------

st.header("🏭 Compressor Sizing")

num_machines = st.slider("Number of Machines", 1, 10, 3)

total_cfm = 0
pressures = []

for i in range(num_machines):
    col1, col2, col3 = st.columns(3)

    with col1:
        cfm = st.selectbox(f"Machine {i+1} CFM", list(range(10, 305, 5)), key=f"cfm{i}")

    with col2:
        pressure = st.selectbox(f"Pressure {i+1}", list(range(4, 11)), key=f"p{i}")

    with col3:
        mode = st.selectbox(f"Mode {i+1}", ["Continuous", "Intermittent"], key=f"m{i}")

    if mode == "Continuous":
        eff_cfm = cfm
    else:
        on = st.slider(f"ON time {i+1}", 1, 60, 10, key=f"on{i}")
        cycle = st.slider(f"Cycle time {i+1}", 1, 60, 20, key=f"cy{i}")
        eff_cfm = cfm * (on / cycle)

    total_cfm += eff_cfm
    pressures.append(pressure)

avg_pressure = sum(pressures) / len(pressures)
flow = total_cfm * 1.7
efficiency = st.slider("Efficiency", 0.5, 0.95, 0.75)

power = (flow * avg_pressure * math.log(avg_pressure)) / (36.7 * efficiency)
specific_power = power / total_cfm

st.subheader("📊 Sizing Result")
st.write(f"Total Demand: {round(total_cfm,2)} CFM")
st.write(f"Power: {round(power,2)} kW")
st.write(f"Specific Power: {round(specific_power,3)} kW/CFM")

# -------------------------------
# COMPRESSOR SELECTION
# -------------------------------

st.header("⚙ Compressor Selection")

if power < 75:
    selection = "1 x Small Screw Compressor"
elif power < 200:
    selection = "2 x Medium Compressors (1 working + 1 standby)"
else:
    selection = "3 x Compressors (2 working + 1 standby)"

st.success(selection)

# -------------------------------
# LEAKAGE
# -------------------------------

st.header("💨 Leakage Audit")

num_leaks = st.slider("Leak Points", 1, 20, 3)
pressure_leak = st.slider("Pressure", 4, 10, 7)

total_leak = 0

for i in range(num_leaks):
    size = st.selectbox(f"Leak size {i+1}", [round(0.1+j*0.2,1) for j in range(20)], key=f"l{i}")
    count = st.number_input(f"No. {i+1}", 1, 20, 1, key=f"c{i}")

    area = math.pi * (size/1000)**2 / 4
    leak = area * 10000 * math.sqrt(pressure_leak) * 2118

    total_leak += leak * count

cost = st.slider("Power cost ₹", 5, 15, 5)

leak_power = total_leak * 0.1
leak_cost = leak_power * 8000 * cost

st.write(f"Leakage: {round(total_leak,2)} CFM")
st.write(f"Leak Cost: ₹ {round(leak_cost,0)}")

# -------------------------------
# TOTAL ENERGY
# -------------------------------

total_power = power + leak_power
total_cost = total_power * 8000 * cost

st.header("💰 Total Cost")
st.write(f"Annual Cost: ₹ {round(total_cost,0)}")

# -------------------------------
# PDF REPORT
# -------------------------------

st.header("📄 Generate Report")

def create_pdf():
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)

    c.drawString(50, 750, "Industrial Compressor Report")
    c.drawString(50, 720, f"Total CFM: {round(total_cfm,2)}")
    c.drawString(50, 700, f"Power: {round(power,2)} kW")
    c.drawString(50, 680, f"Leak Cost: ₹ {round(leak_cost,0)}")
    c.drawString(50, 660, f"Total Cost: ₹ {round(total_cost,0)}")
    c.drawString(50, 640, f"Recommendation: {selection}")

    c.save()
    buffer.seek(0)
    return buffer

pdf = create_pdf()

st.download_button(
    label="Download Report",
    data=pdf,
    file_name="compressor_report.pdf",
    mime="application/pdf"
)

# -------------------------------
# GRAPH
# -------------------------------

st.header("📈 Efficiency Curve")

eff_range = [0.6,0.65,0.7,0.75,0.8,0.85]
power_list = []

for e in eff_range:
    p = (flow * avg_pressure * math.log(avg_pressure)) / (36.7 * e)
    power_list.append(p)

plt.figure()
plt.plot(eff_range, power_list)
st.pyplot(plt)
# -------------------------------
# SAVING REPORT
# -------------------------------

st.header("📢 Energy Saving Report")

saving_leak = leak_cost
saving_pressure = total_cost * 0.05 if avg_pressure > 7 else 0
saving_efficiency = total_cost * 0.1 if specific_power > 0.12 else 0

total_saving = saving_leak + saving_pressure + saving_efficiency

st.subheader("💰 Saving Potential")

st.write(f"Leakage Saving: ₹ {round(saving_leak,0)}")
st.write(f"Pressure Optimization Saving: ₹ {round(saving_pressure,0)}")
st.write(f"Efficiency Improvement Saving: ₹ {round(saving_efficiency,0)}")

st.success(f"Total Possible Saving: ₹ {round(total_saving,0)} per year")

# -------------------------------
# ACTION PLAN
# -------------------------------

st.subheader("🛠 Recommended Actions")

if saving_leak > 0:
    st.write("✔ Fix all leakage points immediately")

if avg_pressure > 7:
    st.write("✔ Reduce system pressure by 1 bar")

if specific_power > 0.12:
    st.write("✔ Upgrade compressor or improve system efficiency")

st.write("✔ Install proper monitoring system")
