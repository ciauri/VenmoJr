PRAGMA foreign_keys=ON;
BEGIN TRANSACTION;
CREATE TABLE cc(
cid integer primary key, number int not null unique, uid int references user(uid) on delete cascade);
CREATE TABLE user(
uid integer primary key, username text not null unique check(length(username)>=4 and length(username) <= 15), balance real default 0, card integer references cc(cid));
CREATE TABLE trans(
tid integer primary key, src int, dst int, amount real, ts datetime default current_timestamp, note text, foreign key(src) references user(uid), foreign key(dst) references user(uid));
COMMIT;
