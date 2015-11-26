drop table if exists entries;
create table trends (
  id integer primary key autoincrement,
  keyword text unique not null,
  woeid int not null
);