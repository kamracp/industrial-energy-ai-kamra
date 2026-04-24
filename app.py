import streamlit as st
import math

st.set_page_config(page_title="Industrial Energy AI", layout="wide")

st.title("⚡ Industrial Compressor Sizing AI")

col1, col2 = st.columns(2)

with col1:
    flow = st.number_input("Air Flow (Nm3/hr)", value=1000)
    pressure = st.number_input("Discharge Pressure (bar)", value=7)
    efficiency = st.slider("Efficiency", 0.5, 0.95, 0.75)
    leakage = st.slider("Leakage %", 0, 50, 20)

with col2:
    hours = st.number_input("Operating Hours/year", value=8000)
    cost = st.number_input("Electricity Cost (₹/kWh)", value=8)

# Engineering Calculation
actual_flow = flow * (1 + leakage/100)

power = (actual_flow * pressure * math.log(pressure/1)) / (36.7 * efficiency)

annual_energy = power * hours
annual_cost = annual_energy * cost

st.subheader("📊 Results")

st.write(f"Required Compressor Power: {round(power,2)} kW")
st.write(f"Annual Energy Cost: ₹ {round(annual_cost,0)}")

st.subheader("🤖 AI Advisor")

if leakage > 15:
    st.warning("⚠ High leakage detected – fix leaks immediately")

if efficiency < 0.7:
    st.warning("⚠ Low efficiency – consider VFD compressor")

if pressure > 7:
    st.warning("⚠ High pressure – reduce setpoint to save energy")

saving = annual_cost * 0.2

st.success(f"💰 Potential Saving: ₹ {round(saving,0)} per year")
