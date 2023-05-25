create table if not exists users (
  id integer primary key,
  username text not null,
  email text not null,
  hashed_password text
);
