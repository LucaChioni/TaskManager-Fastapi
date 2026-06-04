SELECT *
FROM orders
WHERE user_id = 1;

SELECT order_items.order_id, SUM(products.price * order_items.quantity) AS total_price
FROM order_items
JOIN products ON order_items.product_id = products.id
GROUP BY order_items.order_id;

SELECT DISTINCT users.*
FROM users
JOIN orders ON users.id = orders.user_id;

SELECT users.*
FROM users
LEFT JOIN orders ON users.id = orders.user_id
WHERE orders.id IS NULL;
