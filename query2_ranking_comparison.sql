WITH RecentMonth AS (
    SELECT b.name, COUNT(r._id) AS receipt_count
    FROM Receipts r
    JOIN ReceiptItems ri ON r._id = ri.receiptId
    JOIN Brands b ON ri.brandId = b._id
    WHERE r.createDate >= DATE_SUB(CURDATE(), INTERVAL 1 MONTH)
    GROUP BY b.name
),
PreviousMonth AS (
    SELECT b.name, COUNT(r._id) AS receipt_count
    FROM Receipts r
    JOIN ReceiptItems ri ON r._id = ri.receiptId
    JOIN Brands b ON ri.brandId = b._id
    WHERE r.createDate >= DATE_SUB(DATE_SUB(CURDATE(), INTERVAL 1 MONTH), INTERVAL 1 MONTH)
    AND r.createDate < DATE_SUB(CURDATE(), INTERVAL 1 MONTH)
    GROUP BY b.name
)
SELECT rm.name, rm.receipt_count AS recent_receipts, COALESCE(pm.receipt_count, 0) AS previous_receipts
FROM RecentMonth rm
LEFT JOIN PreviousMonth pm ON rm.name = pm.name
ORDER BY recent_receipts DESC
LIMIT 5;