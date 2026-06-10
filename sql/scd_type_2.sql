-- SCD Type 2 merge for product price history in BigQuery

MERGE `retail_analytics.dim_product` AS target
USING (
    SELECT
        product_id,
        raw_price AS current_price,
        CURRENT_TIMESTAMP() AS effective_start_date
    FROM `retail_analytics.stg_clean_transactions`
    QUALIFY ROW_NUMBER() OVER (
        PARTITION BY product_id
        ORDER BY transaction_date DESC
    ) = 1
) AS source
ON target.product_id = source.product_id
AND target.is_current = TRUE

WHEN MATCHED
AND target.current_price != source.current_price THEN
    UPDATE SET
        effective_end_date = TIMESTAMP_SUB(source.effective_start_date, INTERVAL 1 SECOND),
        is_current = FALSE,
        updated_at = CURRENT_TIMESTAMP()

WHEN NOT MATCHED THEN
    INSERT (
        product_id,
        current_price,
        effective_start_date,
        effective_end_date,
        is_current,
        created_at,
        updated_at
    )
    VALUES (
        source.product_id,
        source.current_price,
        source.effective_start_date,
        NULL,
        TRUE,
        CURRENT_TIMESTAMP(),
        CURRENT_TIMESTAMP()
    );S

    -- Insert new current records for products where the price changed

INSERT INTO `retail_analytics.dim_product` (
    product_id,
    current_price,
    effective_start_date,
    effective_end_date,
    is_current,
    created_at,
    updated_at
)
SELECT
    source.product_id,
    source.current_price,
    CURRENT_TIMESTAMP() AS effective_start_date,
    NULL AS effective_end_date,
    TRUE AS is_current,
    CURRENT_TIMESTAMP() AS created_at,
    CURRENT_TIMESTAMP() AS updated_at
FROM (
    SELECT
        product_id,
        raw_price AS current_price,
        transaction_date
    FROM `retail_analytics.stg_clean_transactions`
    QUALIFY ROW_NUMBER() OVER (
        PARTITION BY product_id
        ORDER BY transaction_date DESC
    ) = 1
) source
LEFT JOIN `retail_analytics.dim_product` target
    ON source.product_id = target.product_id
    AND target.is_current = TRUE
WHERE target.product_id IS NULL
   OR target.current_price != source.current_price;