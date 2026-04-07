-- publication_year: publication year
-- book_count: number of books published that year
-- avg_price_usd: average price in USD (EUR converted €1 = $1.2)

CREATE TABLE IF NOT EXISTS books_summary AS
SELECT
    year AS publication_year,
    COUNT(*) AS book_count,
    ROUND(
        AVG(
            CASE
                WHEN currency = 'EUR' THEN price_value * 1.2
                ELSE price_value
            END
        ), 2
    ) AS avg_price_usd
FROM books
GROUP BY year
ORDER BY year;

SELECT * FROM books_summary ORDER BY publication_year;



-- row counts
SELECT 'books' AS table_name, COUNT(*) AS row_count FROM books
UNION ALL
SELECT 'books_summary' AS table_name, COUNT(*) AS row_count FROM books_summary;

