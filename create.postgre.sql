create  table steps (
  id serial primary key,
  name varchar(100)
);

create  table steps_steps (
  id serial primary key,
  step integer,
  next integer,
  foreign key(step) references steps(id),
  foreign key(next) references steps(id)
);

create  table users (
  id serial primary key,
  username varchar(255) unique,
  password varchar(255) default null
);

create  table articles (
  id serial primary key,
  title varchar(255),
  format varchar(20),
  type varchar(20),
  due_date  timestamp,
  content text,
  exergue text,
  step_id int,
  max_lenght int default 0,
  min_lenght int default 0,
  author varchar(100),
  
  foreign key (step_id) references steps (id)
);

insert into users(username) values('guest');
insert into users(username) values('admin');

