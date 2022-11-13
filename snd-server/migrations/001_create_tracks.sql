create table if not exists tracks (
  id text primary key,
  song_name text,
  popularity real not null,
  release_date text,
  acousticness real not null,
  danceability real not null,
  duration_ms integer not null,
  energy real not null,
  instrumentalness real not null,
  song_key integer not null,
  liveness real not null,
  loudness real not null,
  mode integer not null,
  speechiness real not null,
  tempo real not null,
  time_signature integer not null,
  valence real not null
);
