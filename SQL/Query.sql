-- customers
create table if not exists customers (
    id int primary key,
    name varchar(255) not null,
    email varchar(255) unique not null,
    city varchar(255) not null,
    created_at timestamp default current_timestamp
);

-- orders
create table if not exists orders (
    id int primary key,
    customer_id int not null,
    total numeric(10,2) not null,
    status varchar(50) not null,
    ordered_at timestamp default current_timestamp,
    foreign key (customer_id) references customers(id)
);

-- products
create table if not exists products(
    id int primary key,
    name varchar(255) not null,
    category varchar(255) not null,
    price numeric(10,2) not null
);

-- order_items
create table if not exists order_items (
    id int primary key,
    order_id int not null,
    product_id int not null,
    quantity int not null,
    unit_price numeric(10,2) not null,
    foreign key (order_id) references orders(id),
    foreign key (product_id) references products(id)
);


insert into customers (id, name, email, city) values
(101, 'davish', 'davish@gmail.com', 'erode'),
(102, 'vignesh', 'vignesh@gmail.com', 'karur'),
(103, 'kishore', 'kishore@gmail.com', 'namakkal'),
(104, 'arun', 'arun@gmail.com', 'chennai'),
(105, 'meena', 'meena@gmail.com', 'salem');


insert into orders (id, customer_id, total, status, ordered_at) values
(1, 101, 2000, 'completed', '2024-01-10'),
(2, 101, 1500, 'completed', '2024-01-12'),
(3, 102, 3000, 'completed', '2024-02-01'),
(4, 104, 2500, 'pending',   '2024-02-05');

insert into products (id, name, category, price) values
(101, 'macbook pro m1', 'electronics', 198000),
(102, 'oneplus buds 3', 'electronics', 3000),
(103, 'dermaco sunscreen', 'cosmetics', 500),
(104, 'facewash', 'cosmetics', 300),
(105, 'pedigree dog food', 'pets', 700),
(106, 't-shirt', 'clothing', 500),
(107, 'pillow cover', 'clothing', 600);


insert into order_items (id, order_id, product_id, quantity, unit_price) values
(1, 1, 101, 1, 198000),
(2, 1, 103, 3, 500),
(3, 2, 106, 4, 500),
(4, 2, 107, 3, 600),
(5, 3, 102, 3, 3000),
(6, 3, 103, 5, 500),
(7, 3, 105, 2, 700),
(8, 3, 106, 5, 500),
(9, 4, 104, 6, 300),
(10, 4, 105, 3, 700),
(11, 4, 103, 4, 500);


-- TASK-1 : Write a query to list the names and emails of all customers who have never placed an order.
select c.name, c.email
from customers c
left join orders o
on c.id = o.customer_id
where o.id is null;


-- TASK-2 : Write a query to return the top 5 products by total quantity sold, sorted in descending order.

select p.name, sum(o.quantity) as total_units_sold
from products p
join order_items o
on p.id = o.product_id
group by p.id, p.name
order by total_units_sold desc
limit 5;

-- TASK-3: Write a query to show total revenue per month for the year 2024.
-- Only include orders with status = 'completed'.
-- Format the month as YYYY-MM.

select to_char(o.ordered_at, 'YYYY-MM') as order_month, sum(o.total) as total_revenue
from orders o
where o.status = 'completed'
and o.ordered_at >= '2024-01-01'
and o.ordered_at <= '2024-12-31'
group by to_char(o.ordered_at, 'YYYY-MM')
order by order_month;


-- TASK-4: List the names of customers whose total lifetime spend (sum of all completed orders) 
-- is greater than the average lifetime spend across all customers.

with lifetime_spend_per_customer as (
	select c.name, sum(total) as lifetime_spend
	from customers c
	left join orders o
	on c.id = o.customer_id
	where o.status = 'completed'
	group by c.id, c.name
)
select name
from lifetime_spend_per_customer
where lifetime_spend > (
select avg(lifetime_spend) 
from lifetime_spend_per_customer
);


-- TASK-5: Slow Query - Fix the N+1 Problem
-- Slow query
SELECT 
    o.id, 
    o.total,
    (SELECT name 
     FROM customers 
     WHERE id = o.customer_id) AS customer_name
FROM orders o
WHERE o.ordered_at >= '2021-01-01';

-- When you fetch N rows from DB, and then for each row you make one more query to get related data — that's N+1. 
-- One query to get the list, N queries to fill in the details. 
-- It compounds fast — 1000 rows means 1001 DB hits instead of 1.

-- Usually happens when you put a subquery inside SELECT that references the outer row — so the DB re-runs it per row. 
-- Fix is a JOIN, which resolves everything in one shot at the FROM stage.

select o.id, o.total, c.name
from orders o
join customers c
on o.customer_id = c.id
where o.ordered_at >= '2021-01-01';


-- TASK-6: Using a window function, rank products within each category by total units sold.

-- Return:
-- product name
-- category
-- total units sold
-- rank within the category (based on total units sold)

with products_total_units as (
	select p.name, p.category, sum(oi.quantity) as total_units
	from products p
	left join order_items oi
	on p.id = oi.product_id
	group by p.id, p.name, p.category
)
select
name,
category, 
total_units,
rank() over (partition by category order by total_units desc) as product_rank
from products_total_units;

-- Task 7: Missing Index — Diagnose and Fix
-- Given a slow report query, identify what index would help and write the CREATE INDEX statement.

-- slow query
-- SELECT 
--     c.city, 
--     SUM(o.total) AS revenue
-- FROM orders o
-- JOIN customers c 
--     ON c.id = o.customer_id
-- WHERE 
--     o.status = 'completed'
--     AND o.ordered_at BETWEEN '2024-01-01' AND '2024-12-31'
-- GROUP BY 
--     c.city
-- ORDER BY 
--     revenue DESC;

CREATE INDEX idx_orders_status_date 
ON orders (status, ordered_at);


-- TASK-8: Write a query that returns each completed order date and a
-- running cumulative total of revenue up to and including that date, ordered chronologically.

select date(o.ordered_at) as order_date,
sum(sum(o.total)) over (order by date(ordered_at)) as cumulative_revenue 
from orders o
where o.status = 'completed'
group by date(o.ordered_at)
order by order_date;


-- TASK-9: Write a query to find all customers who placed more than one order on the same calendar day.
-- Return:
-- customer name
-- order date
-- order count (number of orders on that day)

select c.id, c.name, date(o.ordered_at) as order_date, count(o.id) as order_count
from customers c
join orders o
on c.id = o.customer_id
group  by c.id, c.name, date(o.ordered_at)
having count(o.id) > 1;

-- TASK-10: Without using window functions or LIMIT/OFFSET, write a query to find the
-- second highest order total from the orders table.

select max(total)
from orders
where total < (select max(total) from orders);

-- TASK-11: Using CTEs:
-- First, calculate each customer's lifetime spend (only completed orders).
-- Then, from that result, label customers as:
-- 'gold' → spend > 10000
-- 'silver' → spend between 5000 and 10000
-- 'bronze' → spend below 5000

-- Return:
-- name
-- city
-- total spend
-- tier

with lifetime_spend as (
	select c.id, c.name, c.city,
	sum(o.total) as total_spend
	from customers c
	left join orders o 
	on c.id = o.customer_id 
	where o.status = 'completed'
	group by c.id, c.name, c.city
)
select name, city, total_spend,
case 
	when total_spend > 10000 then 'gold'
	when total_spend between 5000 and 10000 then 'silver'
	else 'bronze'
end as tier
from lifetime_spend
order by total_spend desc;


-- Task 12: Debug — wrong JOIN type
-- This query is supposed to list ALL products and how many times each has been ordered, 
-- including products that have never been ordered. It is returning fewer rows than expected — find and fix the bug.
-- Buggy query:
		-- SELECT p.name, COUNT(oi.id) AS times_ordered
		-- FROM order_items oi
		-- INNER JOIN products p
		-- ON p.id = oi.product_id
		-- GROUP BY p.id, p.name
		-- ORDER BY times_ordered DESC;
-- Issue:
-- Using INNER JOIN removes products that have no matching rows in order_items.
-- Fixed query:
select p.name, count(oi.id) as times_ordered
from products p
left join order_items oi
on p.id = oi.product_id
group by p.id, p.name
order by times_ordered desc;

-- Task 13: Self-join: find referred customers
-- The customers table has a referred_by_customer_id column pointing to another row in the same table. 
-- Write a query to list each referrer’s name alongside the names of the customers they referred. 
-- Only include referrers who have referred at least 2 people.

alter table customers add column referred_by_customer_id int;
alter table customers add foreign key (referred_by_customer_id) references customers(id);

update customers set referred_by_customer_id = 101 where id in (102, 103);
update customers set referred_by_customer_id = 104 where id = 105;

insert into customers (id, name, email, city, referred_by_customer_id) values
(106, 'priya', 'priya@gmail.com', 'coimbatore', 101),
(107, 'divya', 'divya@gmail.com', 'madurai', 101),
(108, 'kavin', 'kavin@gmail.com', 'trichy', 102),
(109, 'anbu', 'anbu@gmail.com', 'erode', 104),
(110, 'selvi', 'selvi@gmail.com', 'salem', 104);

select 
r.name as referrer_name,
c.name as referred_customer_name
from customers r
join customers c on r.id = c.referred_by_customer_id
where (
    select count(*) 
    from customers c2 
    where c2.referred_by_customer_id = r.id
) >= 2
order by r.name, c.name;


-- Task 14: Slow query — redundant subquery in FROM
-- Identify a performance anti-pattern where a full table scan is wrapped unnecessarily.

-- Question:
-- This query calculates total revenue per order for completed orders in 2024. It runs for 20+ seconds on large data. Identify the inefficiency and rewrite it:

-- SELECT o.id, o.ordered_at,
-- (SELECT SUM(oi.quantity * oi.unit_price)
-- FROM order_items oi
-- WHERE oi.order_id = o.id) AS order_revenue
-- FROM (
-- SELECT * FROM orders
-- WHERE status = 'completed'
-- AND YEAR(ordered_at) = 2024
-- ) o;

select o.id, o.ordered_at, sum(oi.quantity * oi.unit_price) as order_revenue
from orders o
join order_items oi on oi.order_id = o.id
where o.status = 'completed' and o.ordered_at >= '2024-01-01' and o.ordered_at < '2025-01-01'
group by o.id, o.ordered_at;


-- Task 15: Pivot — Category Sales by Quarter
-- Write a query that produces one row per product category and
-- four columns — Q1, Q2, Q3, Q4 — each showing the total revenue (quantity * unit_price) 
-- for that quarter in 2024.

select 
    p.category,
    sum(case 
        when extract(quarter from o.ordered_at) = 1 
        then oi.quantity * oi.unit_price 
        else 0 
    end) as q1,
    sum(case 
        when extract(quarter from o.ordered_at) = 2 
        then oi.quantity * oi.unit_price 
        else 0 
    end) as q2,
    sum(case 
        when extract(quarter from o.ordered_at) = 3 
        then oi.quantity * oi.unit_price 
        else 0 
    end) as q3,
    sum(case 
        when extract(quarter from o.ordered_at) = 4 
        then oi.quantity * oi.unit_price 
        else 0 
    end) as q4
from products p
join order_items oi on p.id = oi.product_id
join orders o on o.id = oi.order_id
where 
    o.status = 'completed'
    and o.ordered_at >= '2024-01-01'
    and o.ordered_at < '2025-01-01'
group by p.category
order by p.category;