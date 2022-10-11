create table if not exists users (
  id integer primary key,
  email text not null,
  access_key_hash text
);
