create table if not exists search_history (
  userid integer primary key,
  foreign key(trackid) references users(id)
);
