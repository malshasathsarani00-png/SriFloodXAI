def generate_semantic_alert(alert_type, severity):

    if severity == "High":

        return (
            "🚨 Immediate action is recommended. "
            "Residents should follow instructions "
            "from local authorities."
        )

    elif severity == "Medium":

        return (
            "⚠️ Stay alert and monitor weather "
            "conditions closely."
        )

    else:

        return (
            "✅ No immediate threat detected. "
            "Continue normal activities with caution."
        )