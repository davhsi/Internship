-- customers(id, name, email, city, created_at)
-- orders(id, customer_id, total, status, ordered_at)

create table if not exists customers (
id int primary key,
name varchar(255) not null,
email varchar(255) not null,
city varchar(255) not null,
created_at timestamp default current_timestamp
);

create table if not exists orders (
id int primary key,
customer_id int not null,
total int not null,
status varchar(50) not null,
ordered_at timestamp default current_timestamp,
foreign key (customer_id) references customers(id)
);

insert into customers (id, name, city, email) values 
(101, 'Davish', 'Erode', 'davish@gmail.com'),
(102, 'Vignesh', 'Karur', 'vignesh@gmail.com'),
(103, 'Kishore', 'Namakkal', 'kishore@gmail.com');


insert into orders (id, customer_id, total, status) values
(1, 101, 2000, 'delivered'),
(2, 101, 1000, 'shipped'),
(3, 102, 5000, 'delivered'),
(4, 102, 8000, 'cancelled');


-- Write a query to list the names and emails of all customers who have never placed an order.

select c.name, c.email
from customers c
left join orders o
on c.id = o.customer_id
where o.id is null;


