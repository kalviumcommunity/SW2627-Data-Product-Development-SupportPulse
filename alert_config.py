# ==========================================
# SUPPORTPULSE ALERT CONFIGURATION
# ==========================================

ALERT_THRESHOLDS = {

    # Alert when churn rises above the safe limit.
    "churn_rate": {
        "metric": "Churn Rate",
        "threshold": 7.0,
        "direction": "above",
        "severity": "critical",
        "message": (
            "Churn exceeds the safe limit. "
            "Investigate customer retention immediately."
        )
    },

    # Alert when average customer spend falls below target.
    "average_spend": {
        "metric": "Average Spend",
        "threshold": 30.0,
        "direction": "below",
        "severity": "warning",
        "message": (
            "Average spend is below the target. "
            "Check pricing and customer product mix."
        )
    },

    # Alert when data quality becomes poor.
    "null_percentage": {
        "metric": "Data Quality (Null %)",
        "threshold": 5.0,
        "direction": "above",
        "severity": "warning",
        "message": (
            "Null percentage exceeds the acceptable limit. "
            "Check the data pipeline for missing values."
        )
    }
}