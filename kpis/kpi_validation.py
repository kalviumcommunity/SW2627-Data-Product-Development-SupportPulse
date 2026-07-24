import json
import pandas as pd

from kpis.kpi_functions import *


def validate_kpis(df):
    """
    Validate KPI values
    against target ranges.
    """

    with open(

        "kpis/kpi_validation_targets.json",

        "r",

        encoding="utf-8"

    ) as file:

        targets = json.load(file)

    mau = calculate_mau(df)

    rpc = calculate_revenue_per_customer(df)

    churn = calculate_churn_rate(df)

    payment = calculate_payment_success_rate(df)

    cac = calculate_cac(
        marketing_cost=7000,
        new_customers=180
    )

    current_kpis = {

        "monthly_active_users":
            mau,

        "revenue_per_customer":
            rpc,

        "churn_rate":
            churn,

        "payment_success_rate":
            payment,

        "customer_acquisition_cost":
            cac

    }

    report = []

    for kpi, target in targets.items():

        actual = current_kpis[kpi]

        status = (

            "PASS"

            if target["min"]
            <= actual
            <= target["max"]

            else

            "ALERT"

        )

        report.append({

            "KPI":
                kpi,

            "Actual":
                round(actual, 2),

            "Target Min":
                target["min"],

            "Target Max":
                target["max"],

            "Status":
                status

        })

    validation_df = pd.DataFrame(
        report
    )

    print(validation_df)

    failures = validation_df[
        validation_df["Status"] == "ALERT"
    ]

    if len(failures) > 0:

        print(
            f"\n⚠ {len(failures)} KPI(s) "
            "outside target range."
        )

    else:

        print(
            "\n✓ All KPIs "
            "within target range."
        )

    return validation_df