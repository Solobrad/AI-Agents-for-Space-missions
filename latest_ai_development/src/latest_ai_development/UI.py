import streamlit as st
import sqlite3

# Database Connection
DB_FILE = "crew_resources.db"

def query_db(query, params=()):
    """Helper function to query the database."""
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute(query, params)
    results = cursor.fetchall()
    conn.commit()
    conn.close()
    return results

st.title("🚀 CrewAI Resource Management")

st.subheader("📦 Available Resources")
resources = query_db("SELECT name, quantity, unit FROM resources")
for res in resources:
    st.write(f"**{res[0]}**: {res[1]} {res[2]}")

st.subheader("🛰️ Available Missions")
missions = query_db("SELECT name, required_resource, required_quantity FROM missions")
for mission in missions:
    st.write(f"**{mission[0]}**: Requires {mission[2]} {mission[1]}")

st.subheader("🎯 Start a Mission")
mission_name = st.selectbox("Select Mission", [m[0] for m in missions])
agent_name = st.text_input("Agent Name", "Resource Specialist")

if st.button("Start Mission"):
    mission = query_db("SELECT required_resource, required_quantity FROM missions WHERE name = ?", (mission_name,))
    if mission:
        resource_name, required_quantity = mission[0]

        available = query_db("SELECT quantity FROM resources WHERE name = ?", (resource_name,))
        if available and available[0][0] >= required_quantity:
            # Deduct resource
            query_db("UPDATE resources SET quantity = quantity - ? WHERE name = ?", (required_quantity, resource_name))

            # Log action
            query_db("INSERT INTO agent_logs (agent_name, action, resource_name, quantity) VALUES (?, ?, ?, ?)",
                     (agent_name, f"Started {mission_name}", resource_name, required_quantity))

            st.success(f"✅ {agent_name} successfully started '{mission_name}'. Used {required_quantity} {resource_name}.")
        else:
            st.error(f"❌ Not enough {resource_name} for '{mission_name}'")
    else:
        st.error(f"❌ Mission '{mission_name}' not found.")

# Show logs
st.subheader("📜 Mission Logs")
logs = query_db("SELECT agent_name, action, resource_name, quantity, timestamp FROM agent_logs ORDER BY timestamp DESC")

for log in logs:
    st.write(f"📝 **{log[4]}** - {log[0]} {log[1]}: {log[3]} {log[2]} used.")