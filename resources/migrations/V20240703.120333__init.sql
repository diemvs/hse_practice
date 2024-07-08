CREATE TABLE users (
    id          BIGSERIAL       PRIMARY KEY,
    name        varchar(255),
    surname     varchar(255),
    patronymic  varchar(255)
);

CREATE TABLE tools (
    id      BIGSERIAL       PRIMARY KEY,
    name    varchar(255)    NOT NULL
);

CREATE TABLE tools_journal(
    id          BIGSERIAL   PRIMARY KEY,
    datetime    TIMESTAMP   NOT NULL,
    tool_id     BIGINT      NOT NULL
        CONSTRAINT tools_journal_tool_id_fk
            REFERENCES tools ON UPDATE CASCADE ON DELETE CASCADE,
    user_id     BIGINT
        CONSTRAINT tools_journal_user_id_fk
            REFERENCES users ON UPDATE CASCADE ON DELETE CASCADE
);