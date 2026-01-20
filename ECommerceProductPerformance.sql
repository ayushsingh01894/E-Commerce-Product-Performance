-- E-COMMERCE PRODUCT PERFORMANCE ANALYSIS
-- 1 View first 10 records
SELECT * 
FROM products 
LIMIT 10;

-- 2 Total Revenue per Category
SELECT 
    Category, 
    SUM(Selling_Price) AS Total_Revenue
FROM products
GROUP BY Category
ORDER BY Total_Revenue DESC;

-- 3 Average Rating by Brand
SELECT 
    Brand, 
    ROUND(AVG(Rating), 2) AS Avg_Rating
FROM products
GROUP BY Brand
ORDER BY Avg_Rating DESC;

-- 4 Top 10 Most Profitable Products
SELECT 
    Product_Name, 
    Profit
FROM products
ORDER BY Profit DESC
LIMIT 10;

-- 5 Return Rate per Category
SELECT 
    Category,
    SUM(CASE WHEN Return_Status = 'Yes' THEN 1 ELSE 0 END)*100.0 / COUNT(*) AS Return_Rate
FROM products
GROUP BY Category;

-- 6 On-Time Delivery Rate
SELECT 
    Delivery_Status,
    COUNT(*) * 100.0 / (SELECT COUNT(*) FROM products) AS Delivery_Percentage
FROM products
GROUP BY Delivery_Status;
