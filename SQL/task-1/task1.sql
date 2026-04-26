drop table if exists orders;
drop table if exists customers;

create table customers (
    id int primary key,
    name varchar(255) not null,
    email varchar(255) unique not null,
    city varchar(255) not null,
    created_at timestamp default current_timestamp
);

create table orders (
    id int primary key,
    customer_id int not null,
    total numeric(10,2) not null,
    status varchar(50) not null,
    ordered_at timestamp default current_timestamp,
    foreign key (customer_id) references customers(id)
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


select c.name, c.email
from customers c
left join orders o
on c.id = o.customer_id
where o.id is null;