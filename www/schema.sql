create table user (
    id integer primary key,
    usertype varchar(16),
    name varchar(40),
    namecss varchar(16),
    hash varchar(60),
    created datetime,
    lastlogin datetime,
    status varchar(10)
);

create table usercookie (
    userid int,
    cookie varchar(40),
    expires datetime
);

insert into user (usertype, name, namecss, hash, created, status)
select '', 'kdeloach', 'f2 c3', '$2a$12$gTQ9b5wt5GJMvhsk2JebFOFSRJC1ydNKPr56CJD3bkdtIUwEwSkMy', datetime(), 'offline' union all
select 'model', 'Chrysanthemum', 'f6 c6', null, datetime(), 'online' union all
select 'model', 'Desert', 'f2 c8', null, datetime(), 'online' union all
select 'model', 'Hydrangeas', 'f5 c10', null, datetime(), 'online' union all
select 'model', 'Jellyfish', 'f9 c11', null, datetime(), 'online' union all
select 'model', 'Koala', 'f14 c12', null, datetime(), 'online' union all
select 'model', 'Lighthouse', 'f12 c14', null, datetime(), 'online' union all
select 'model', 'Penguins', 'f10 c15', null, datetime(), 'online' union all
select 'model', 'Tulips', 'f11 c16', null, datetime(), 'online';