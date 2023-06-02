create table if not exists search_history (
  trackid text primary key,
  userid integer,
  foreign key(userid) references users(id)
);
