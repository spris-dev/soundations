create table if not exists users (
  id integer primary key,
  username text not null unique,
  hashed_password text
);
