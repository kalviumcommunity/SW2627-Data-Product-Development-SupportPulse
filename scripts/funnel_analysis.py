import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os


def create_sample_dataset():
    """
    Create a sample user funnel dataset.
    """

    np.random.seed(42)

    total_users = 10000

    users = pd.DataFrame({

        "user_id": range(1, total_users + 1)

    })

    users["signup_completed"] = 1

    users["email_entered"] = np.where(
        users["user_id"] <= 8000,
        1,
        0
    )

    users["password_created"] = np.where(
        users["user_id"] <= 6000,
        1,
        0
    )

    users["email_verified"] = np.where(
        users["user_id"] <= 5000,
        1,
        0
    )

    users["payment_added"] = np.where(
        users["user_id"] <= 4000,
        1,
        0
    )

    users["first_purchase"] = np.where(
        users["user_id"] <= 2000,
        1,
        0
    )

    return users


def define_funnel(df):
    """
    Count users present
    at every funnel stage.
    """

    print("\n" + "=" * 65)
    print("FUNNEL STAGES")
    print("=" * 65)

    stage1_signup = len(

        df[
            df["signup_completed"] == 1
        ]

    )

    stage2_email = len(

        df[
            df["email_entered"] == 1
        ]

    )

    stage3_password = len(

        df[
            df["password_created"] == 1
        ]

    )

    stage4_verified = len(

        df[
            df["email_verified"] == 1
        ]

    )

    stage5_payment = len(

        df[
            df["payment_added"] == 1
        ]

    )

    stage6_purchase = len(

        df[
            df["first_purchase"] == 1
        ]

    )

    stages = {

        "Sign Up":
            stage1_signup,

        "Email Entered":
            stage2_email,

        "Password Created":
            stage3_password,

        "Email Verified":
            stage4_verified,

        "Payment Added":
            stage5_payment,

        "First Purchase":
            stage6_purchase

    }

    print("\nFunnel Stage Counts\n")

    for stage, count in stages.items():

        print(

            f"{stage:<20}"

            f"{count:,}"

        )

    return stages   
def compute_drop_off(stages):
    """
    Compute drop-off and completion
    rates between funnel stages.
    """

    print("\n" + "=" * 65)
    print("FUNNEL DROP-OFF ANALYSIS")
    print("=" * 65)

    stage_names = list(stages.keys())
    stage_values = list(stages.values())

    drop_off = []

    for i in range(len(stage_values) - 1):

        users_before = stage_values[i]
        users_after = stage_values[i + 1]

        users_lost = users_before - users_after

        completion_rate = (
            users_after / users_before
        ) * 100

        drop_rate = (
            users_lost / users_before
        ) * 100

        drop_off.append({

            "from_stage": stage_names[i],

            "to_stage": stage_names[i + 1],

            "users_lost": users_lost,

            "completion_rate": completion_rate,

            "drop_rate": drop_rate

        })

    funnel_df = pd.DataFrame(drop_off)

    display_df = funnel_df.copy()

    display_df["completion_rate"] = (
        display_df["completion_rate"]
        .apply(lambda x: f"{x:.1f}%")
    )

    display_df["drop_rate"] = (
        display_df["drop_rate"]
        .apply(lambda x: f"{x:.1f}%")
    )

    print(display_df)

    biggest_drop = funnel_df.loc[
        funnel_df["users_lost"].idxmax()
    ]

    print("\nBiggest Funnel Leak")
    print("----------------------")

    print(
        f"Stage : "
        f"{biggest_drop['from_stage']} → "
        f"{biggest_drop['to_stage']}"
    )

    print(
        f"Users Lost : "
        f"{biggest_drop['users_lost']:,}"
    )

    print(
        f"Drop Rate : "
        f"{biggest_drop['drop_rate']:.1f}%"
    )

    return funnel_df


def create_funnel_chart(stages):
    """
    Create funnel visualization.
    """

    print("\n" + "=" * 65)
    print("FUNNEL VISUALIZATION")
    print("=" * 65)

    os.makedirs(
        "output",
        exist_ok=True
    )

    colors = [

        "#3b82f6",
        "#10b981",
        "#f59e0b",
        "#ef4444",
        "#8b5cf6",
        "#ec4899"

    ]

    plt.figure(figsize=(10, 6))

    bars = plt.bar(

        stages.keys(),

        stages.values(),

        color=colors

    )

    plt.title(
        "Signup Funnel Analysis"
    )

    plt.xlabel(
        "Funnel Stage"
    )

    plt.ylabel(
        "Users"
    )

    plt.xticks(
        rotation=30,
        ha="right"
    )

    plt.ylim(
        0,
        max(stages.values()) * 1.15
    )

    for bar in bars:

        height = bar.get_height()

        plt.text(

            bar.get_x()
            + bar.get_width() / 2,

            height,

            f"{int(height):,}",

            ha="center",

            va="bottom",

            fontweight="bold"

        )

    plt.tight_layout()

    plt.savefig(

        "output/funnel_chart.png",

        dpi=300,

        bbox_inches="tight"

    )

    plt.close()

    print(
        "Funnel chart saved successfully."
    )
def calculate_business_impact(funnel_df):
    """
    Calculate the revenue impact
    of each funnel drop-off.
    """

    print("\n" + "=" * 65)
    print("BUSINESS IMPACT ANALYSIS")
    print("=" * 65)

    revenue_per_customer = 100

    impact_analysis = []

    for _, row in funnel_df.iterrows():

        revenue_lost = (
            row["users_lost"] *
            revenue_per_customer
        )

        priority = (
            "HIGH"
            if revenue_lost >= 150000
            else "MEDIUM"
        )

        impact_analysis.append({

            "drop_point":
                f"{row['from_stage']} → {row['to_stage']}",

            "users_lost":
                row["users_lost"],

            "revenue_impact":
                revenue_lost,

            "priority":
                priority

        })

    impact_df = pd.DataFrame(
        impact_analysis
    )

    display_df = impact_df.copy()

    display_df["revenue_impact"] = (
        display_df["revenue_impact"]
        .apply(lambda x: f"${x:,.0f}")
    )

    print(
        display_df.sort_values(
            by="users_lost",
            ascending=False
        )
    )

    return impact_df


def generate_recommendation(
    funnel_df,
    impact_df
):
    """
    Generate business recommendations
    based on funnel bottlenecks.
    """

    print("\n" + "=" * 65)
    print("FUNNEL OPTIMIZATION RECOMMENDATION")
    print("=" * 65)

    os.makedirs(
        "output",
        exist_ok=True
    )

    highest_impact = funnel_df.loc[
        funnel_df["users_lost"].idxmax()
    ]

    recovered_users = int(
        highest_impact["users_lost"] * 0.10
    )

    recovered_revenue = (
        recovered_users * 100
    )

    recommendation = f"""
FUNNEL OPTIMIZATION PRIORITY
============================

CRITICAL BOTTLENECK
-------------------
Stage:
{highest_impact['from_stage']}
→
{highest_impact['to_stage']}

Users Lost:
{highest_impact['users_lost']:,}

Drop Rate:
{highest_impact['drop_rate']:.1f}%

Revenue Impact:
${highest_impact['users_lost'] * 100:,.0f}

ROOT CAUSE HYPOTHESES
---------------------
• Step may be confusing.
• Too many form fields.
• Payment process is lengthy.
• Users lose trust before purchasing.

RECOMMENDED ACTIONS
-------------------
1. Simplify this funnel step.
2. Run A/B testing.
3. Track conversion improvement.
4. Deploy changes if
   completion improves by >5%.

EXPECTED BUSINESS IMPACT
------------------------
10% Improvement

Recovered Users:
{recovered_users:,}

Recovered Revenue:
${recovered_revenue:,.0f}
"""

    print(recommendation)

    with open(
        "output/funnel_analysis.txt",
        "w",
        encoding="utf-8"
    ) as file:

        file.write(
            recommendation
        )

    print(
        "\nRecommendation saved successfully."
    )


def main():

    os.makedirs(
        "output",
        exist_ok=True
    )

    print("=" * 70)
    print("FUNNEL ANALYSIS & DROP-OFF DETECTION")
    print("=" * 70)

    df = create_sample_dataset()

    stages = define_funnel(df)

    funnel_df = compute_drop_off(
        stages
    )

    create_funnel_chart(
        stages
    )

    impact_df = calculate_business_impact(
        funnel_df
    )

    generate_recommendation(
        funnel_df,
        impact_df
    )

    print("\n" + "=" * 65)
    print("TESTING")
    print("=" * 65)

    print(
        f"Total Users : {len(df):,}"
    )

    print(
        f"Funnel Stages : {len(stages)}"
    )

    print(
        f"Drop-Off Points : {len(funnel_df)}"
    )

    print(
        "\nPipeline Completed Successfully."
    )


if __name__ == "__main__":
    main()