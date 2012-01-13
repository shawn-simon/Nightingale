create table user (
    id integer primary key,
    name varchar(40),
    hash varchar(60),
    created datetime,
    lastlogin datetime
);
-- 
create table usercookie (
    userid int,
    cookie varchar(40),
    expires datetime
);

insert into user (name, hash, created)
select 'kdeloach', '$2a$12$gTQ9b5wt5GJMvhsk2JebFOFSRJC1ydNKPr56CJD3bkdtIUwEwSkMy', datetime();