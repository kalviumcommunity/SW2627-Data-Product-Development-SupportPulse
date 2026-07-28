SELECT

    DATE(created_at) AS signup_date,

    COUNT(*) AS signups,

    SUM(

        CASE

            WHEN email_verified_at IS NOT NULL

            THEN 1

            ELSE 0

        END

    ) AS email_verified,

    SUM(

        CASE

            WHEN first_purchase_at IS NOT NULL

            THEN 1

            ELSE 0

        END

    ) AS first_purchase,

    ROUND(

        100.0 *

        SUM(

            CASE

                WHEN first_purchase_at IS NOT NULL

                THEN 1

                ELSE 0

            END

        )

        /

        COUNT(*),

        1

    ) AS conversion_pct

FROM users

GROUP BY DATE(created_at)

ORDER BY signup_date DESC;