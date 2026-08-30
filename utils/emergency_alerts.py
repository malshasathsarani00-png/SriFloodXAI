def get_emergency_alert(
    risk_level,
    district=None,
    river_name=None,
    river_level=None,
    rainfall=None,
    dmc_alert=None
):

    location = district if district else "selected area"

    if river_name and river_name != "None":
        river_text = f"{river_name} in {location}"
    else:
        river_text = location

    condition_lines = []

    if river_level is not None:
        condition_lines.append(
            f"🌊 Current River Level: {river_level:.2f} m"
        )

    if rainfall is not None:
        condition_lines.append(
            f"🌧 Current Rainfall: {rainfall:.2f} mm"
        )

    if dmc_alert is not None:
        dmc_text = "Active" if dmc_alert in [1, "Yes", True] else "No active alert"
        condition_lines.append(
            f"🚨 DMC Status: {dmc_text}"
        )

    conditions = "\n".join(condition_lines)

    if risk_level == "LOW":

        message = f"""
🟢 LOW FLOOD RISK

📍 Area: {river_text}

{conditions}

Current conditions indicate a low flood risk.

Recommended Actions:
• Continue monitoring weather and river updates
• Follow official DMC information
• No immediate evacuation action is required
"""

        alert_type = "success"

    elif risk_level == "MODERATE":

        message = f"""
🟡 MODERATE FLOOD RISK

📍 Area: {river_text}

{conditions}

Flood conditions may develop if rainfall or river levels increase.

Recommended Actions:
• Stay alert for changing weather conditions
• Monitor official DMC warnings
• Prepare essential emergency supplies
• Residents in low-lying areas near the river should remain prepared

Emergency Number:
📞 DMC: 117
"""

        alert_type = "warning"

    elif risk_level == "HIGH":

        message = f"""
🟠 HIGH FLOOD RISK

📍 Area: {river_text}

{conditions}

There is a significant flood risk for vulnerable and low-lying areas.

Recommended Actions:
• Closely monitor river levels and official warnings
• Move valuables and essential documents to higher places
• Prepare to move to safer higher ground if conditions worsen
• Avoid river banks and flood-prone roads
• Follow instructions issued by DMC and local authorities

Emergency Numbers:
📞 DMC: 117
📞 Police: 119
📞 Ambulance: 110
"""

        alert_type = "error"

    else:

        message = f"""
🔴 CRITICAL FLOOD RISK

📍 Area: {river_text}

{conditions}

🚨 IMMEDIATE FLOOD EMERGENCY 🚨

People in low-lying and flood-prone areas should take immediate precautions.

IMMEDIATE ACTIONS:
• Move to safe higher ground
• Follow DMC and local authority instructions
• Do not enter flooded roads or flowing water
• Switch off electricity if flooding reaches the property and it is safe to do so
• Keep emergency communication devices available

Emergency Numbers:
📞 DMC: 117
📞 Police: 119
📞 Ambulance: 110
📞 Fire Brigade: 110
"""

        alert_type = "critical"

    return {
        "type": alert_type,
        "message": message
    }