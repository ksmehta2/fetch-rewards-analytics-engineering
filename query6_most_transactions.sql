SELECT b.name, COUNT(r._id) AS transaction_count
FROM Users u
JOIN Receipts r ON u._id = r.userId
JOIN ReceiptItems ri ON r._id = ri.receiptId
JOIN Brands b ON ri.brandId = b._id
WHERE u.createdDate >= DATE_SUB(CURDATE(), INTERVAL 6 MONTH)
GROUP BY b.name
ORDER BY transaction_count DESC
LIMIT 1;