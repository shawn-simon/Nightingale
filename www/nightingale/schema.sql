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
