create table steps (
  id serial primary key,
  name varchar(100),
  parent_step int default null,
  
  foreign key (parent_step) references steps (id),
);

create table users (
  id serial primary key,
  username varchar(255),
  password varchar(255) default null
);

create table groups (
  id serial primary key,
  name varchar(100)
);

-- who have the rights
create table steps_groups (
  group_id int,
  step_id int,
  can_read boolean,
  can_write boolean,
  can_create boolean,
  can_delete boolean,
  can_validate boolean,

  foreign key (group_id) references groups (id),
  foreign key (step_id) references steps (id)
);

-- who can manage rights
create table groups_groups (
  admin_id int,
  group_id int,

  foreign key (admin_id) references groups (id),
  foreign key (group_id) references groups (id),
);

create table formats (
  id serial primary key,
  name varchar(255)
);

create table articles (
  id serial primary key,
  title varchar(255),
  type varchar(255),
  format_id int,
  due_date  timestamp,
  content text,
  step_id int,
  max_char int default 0,
  min_char int default 0,
  author varchar(100),
  
  foreign key (step_id) references steps (id),
  foreign key (format_id) references formats (id)
);

insert into users(username) values('guest');
insert into users(username) values('admin');
