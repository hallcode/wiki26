--- Users table
CREATE TABLE users (
    id            integer primary key autoincrement,
    username      text    unique not null,
    email_address text    unique,
    password_hash text,
    active        boolean not null default false,
    totp_secret   text,
    totp_enabled  boolean not null default false,
    page_title    text,
    created_at    text    default current_timestamp
);


--- Sessions table for authentication
CREATE TABLE sessions (
    id               text primary key,
    user_id          integer,
    ip_address       text,
    user_agent       text,
    remember_me      boolean not null default false,
    created_at       text default current_timestamp,
    expires_at       text,
    totp_verified_at text,
    totp_expires_at  text,
    last_activity    text not null default current_timestamp,

    foreign key (user_id)
        references users (id)
        on delete cascade
        on update cascade
);