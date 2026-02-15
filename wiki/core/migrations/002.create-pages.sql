--- Create pages table
CREATE TABLE pages (
    id                 integer primary key autoincrement,
    namespace          text,
    title              text unique not null,
    normalised_title   text unique not null,
    current_version_id text not null,
    updated_at         text not null,
    imported_at        text,
    source             text,
    redirect_to        integer,
    locked_by          integer,

    foreign key (redirect_to) references pages (id),
    foreign key (locked_by) references users (id)
        on delete set null
        on update cascade
);


-- Revisions table
CREATE TABLE revisions (
    id                text primary key,
    page_id           integer not null,
    user_id           integer not null,
    parent_id         text,
    delta             blob,
    content           blob,
    full_content_hash text not null,
    parent_hash       text,
    created_at        text not null default current_timestamp,
    updated_at        text,
    draft             boolean not null default true,
    imported          boolean not null default false,
    size              integer,
    change            integer,

    foreign key (page_id) references pages (id)
        on delete cascade
        on update cascade,

    foreign key (user_id) references users (id)
        on delete restrict
        on update cascade,

    foreign key (parent_id) references revisions (id)
        on delete restrict
        on update cascade
);

--- Categories
CREATE TABLE categories (
    id               integer primary key autoincrement,
    title            text unique not null,
    normalised_title text unique not null
);

CREATE TABLE category_page (
    category_id integer,
    page_id     integer,

    primary key (category_id, page_id),
    foreign key (category_id) references categories (id),
    foreign key (page_id) references pages (id)
);

--- Interlinks table
CREATE TABLE interlinks (
    link_from integer,
    link_to   text,

    primary key(link_from, link_to),
    foreign key (link_from) references pages (id)
        on delete cascade
        on update cascade
);

--- Templates
CREATE TABLE page_templates (
    title       text primary key,
    description text,
    body        text not null
);

--- Templates
CREATE TABLE meta (
    id          integer primary key,
    parent_type text not null,
    parent_id   integer not null,
    type        text,
    key         text not null,
    value       text not null,

    unique (parent_type, parent_id, type, key)
);