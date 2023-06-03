create table if not exists search_history (
  track_id text primary key,
  user_id integer,
  foreign key(user_id) references users(id)
);
