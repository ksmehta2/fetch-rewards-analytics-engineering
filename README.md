# Fetch Rewards Coding Exercise - Analytics Engineer

## Overview

This repository contains the solution for the Fetch Rewards Coding Exercise for the Analytics Engineer role. The solution includes:
- An ER diagram representing the structured relational data model
- SQL queries to answer business questions
- Python script to evaluate data quality issues

## ER Diagram

![ER Diagram](https://github.com/ksmehta2/fetch-rewards-analytics-engineering/blob/main/ER%20Diagram.png)

## SQL Queries

### Query 1: Top 5 Brands by Receipts Scanned for the Most Recent Month

```sql
SELECT b.name, COUNT(r._id) AS receipt_count
FROM Receipts r
JOIN ReceiptItems ri ON r._id = ri.receiptId
JOIN Brands b ON ri.brandId = b._id
WHERE r.createDate >= DATE_SUB(CURDATE(), INTERVAL 1 MONTH)
GROUP BY b.name
ORDER BY receipt_count DESC
LIMIT 5;
```

### Query 2: Ranking Comparison of Top 5 Brands by Receipts Scanned for Recent and Previous Months
```sql
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
```
Query 3: Average Spend from Receipts with 'Accepted' or 'Rejected' Status
```sql
SELECT rewardsReceiptStatus, AVG(totalSpent) AS average_spend
FROM Receipts
WHERE rewardsReceiptStatus IN ('Accepted', 'Rejected')
GROUP BY rewardsReceiptStatus;
```
Query 4: Total Number of Items Purchased from Receipts with 'Accepted' or 'Rejected' Status
```sql

SELECT rewardsReceiptStatus, SUM(purchasedItemCount) AS total_items
FROM Receipts
WHERE rewardsReceiptStatus IN ('Accepted', 'Rejected')
GROUP BY rewardsReceiptStatus;
```
Query 5: Brand with the Most Spend Among Users Created Within the Past 6 Months
```sql
SELECT b.name, SUM(r.totalSpent) AS total_spend
FROM Users u
JOIN Receipts r ON u._id = r.userId
JOIN ReceiptItems ri ON r._id = ri.receiptId
JOIN Brands b ON ri.brandId = b._id
WHERE u.createdDate >= DATE_SUB(CURDATE(), INTERVAL 6 MONTH)
GROUP BY b.name
ORDER BY total_spend DESC
LIMIT 1;
```
Query 6: Brand with the Most Transactions Among Users Created Within the Past 6 Months
```sql
SELECT b.name, COUNT(r._id) AS transaction_count
FROM Users u
JOIN Receipts r ON u._id = r.userId
JOIN ReceiptItems ri ON r._id = ri.receiptId
JOIN Brands b ON ri.brandId = b._id
WHERE u.createdDate >= DATE_SUB(CURDATE(), INTERVAL 6 MONTH)
GROUP BY b.name
ORDER BY transaction_count DESC
LIMIT 1;
```

Data Quality Evaluation Script : 
The data_quality.py script evaluates the data quality of the provided JSON files. It identifies missing values, duplicate records, and data type inconsistencies.

```
python data_quality.py
```
