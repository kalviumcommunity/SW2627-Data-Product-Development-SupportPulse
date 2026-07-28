SELECT
    strftime('%Y-%m', transaction_date) AS month,

    COUNT(DISTINCT customer_id) AS active_users,

    COUNT(DISTINCT CASE
        WHEN customer_type='Enterprise'
        THEN customer_id
    END) AS enterprise_users,

    COUNT(DISTINCT CASE
        WHEN customer_type='SMB'
        THEN customer_id
    END) AS smb_users

FROM transactions

GROUP BY strftime('%Y-%m', transaction_date)

ORDER BY month DESC;