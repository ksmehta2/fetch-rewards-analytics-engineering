
SELECT rewardsReceiptStatus, SUM(purchasedItemCount) AS total_items
FROM Receipts
WHERE rewardsReceiptStatus IN ('Accepted', 'Rejected')
GROUP BY rewardsReceiptStatus;