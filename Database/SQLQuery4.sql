create database Socket_MMT
go

use Socket_MMT
go

create table account(
	username varchar(16) NOT NULL,
	"password" varchar(16) NOT NULL
)
go

insert account values ('hoang', '123456')
insert account values ('viet', 'viet2002')
insert account values ('user', '123456')
