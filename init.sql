create table alembic_version
(
    version_num varchar(32) not null
        constraint alembic_version_pkc
            primary key
);

create table users
(
    id            serial
        primary key,
    username      varchar(50)             not null
        unique,
    password_hash varchar(255)            not null,
    nickname      varchar(50),
    last_login_ip inet,
    created_at    timestamp default now() not null,
    updated_at    timestamp default now() not null
);

create table conversations
(
    id         serial
        primary key,
    user_id    integer                 not null
        references users
            on delete cascade,
    title      varchar(100)            not null,
    created_at timestamp default now() not null,
    updated_at timestamp default now() not null
);

create table messages
(
    id              serial
        primary key,
    conversation_id integer                 not null
        references conversations
            on delete cascade,
    role            varchar(20)             not null,
    content         text                    not null,
    created_at      timestamp default now() not null
);


