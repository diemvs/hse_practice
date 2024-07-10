CREATE TABLE files (
    id           bigserial not null
        constraint files_pkey primary key,

    name         varchar(255)
);

CREATE TABLE users_images (
    id          bigserial       primary key,

    file_id     BIGINT          NOT NULL
        CONSTRAINT users_images_file_id_fk
            REFERENCES files ON UPDATE CASCADE ON DELETE CASCADE,

    user_id     BIGINT          NOT NULL
        CONSTRAINT users_images_user_id_fk
            REFERENCES users ON UPDATE CASCADE ON DELETE CASCADE,

    embedding   NUMERIC(9,2)[]
);