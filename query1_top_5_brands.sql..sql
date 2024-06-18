SELECT b.name, COUNT(r._id) AS receipt_count
FROM Receipts r
JOIN ReceiptItems ri ON r._id = ri.receiptId
JOIN Brands b ON ri.brandId = b._id
WHERE r.createDate >= DATE_SUB(CURDATE(), INTERVAL 1 MONTH)
GROUP BY b.name
ORDER BY receipt_count DESC
LIMIT 5;