### Task 1: Find customers who never ordered
- Common business need — identify inactive customers for a re-engagement campaign.

- Schema

customers(id, name, email, city, created_at)
orders(id, customer_id, total, status, ordered_at)

- Question
- Write a query to list the names and emails of all customers who have never placed an order.