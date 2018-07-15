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
  due_date varchar(20),
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

insert into steps(id, name) values(0, 'Rédaction');
insert into steps(id, name) values(1, 'Correction');
insert into steps(id, name) values(2, 'Integration');
insert into steps(id, name) values(3, 'Archive');
insert into steps(id, name) values(10, 'Émission');
insert into steps(id, name) values(11, 'Archive radio');

insert into articles(title, format, type, due_date, content, exergue, step_id, max_lenght, min_lenght, author) values ('Il y a 30 ans', 'Edito', 'article', '2018-07-15 21:26:00', 'blablabla', 'bla', 0, 100, 30, 'lucie');
insert into articles(title, format, type, due_date, content, exergue, step_id, max_lenght, min_lenght, author) values ('Il y a 30 heures', 'Concert', 'article', '2018-07-15 21:26:00', 'bla2blabla', 'bla2', 0, 100, 30, 'Rose');
insert into articles(title, format, type, due_date, content, exergue, step_id, max_lenght, min_lenght, author) values ('Il y a 30 radios', 'Concert', 'article', '2018-07-15 21:26:00', 'bla2blabla', 'bla2', 10, 100, 30, 'Rose');
