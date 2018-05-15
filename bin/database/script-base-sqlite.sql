CREATE TABLE xf_auth_api (
    internal      CHAR (32) NOT NULL,
    created       DATETIME,
    client_secret VARCHAR   NOT NULL,
    api_key       VARCHAR   NOT NULL,
    PRIMARY KEY (
        internal
    ),
    UNIQUE (
        api_key
    ),
    UNIQUE (
        client_secret
    )
);

CREATE TABLE xf_user (
    id            INTEGER       NOT NULL
                                PRIMARY KEY AUTOINCREMENT,
    internal      CHAR (32),
    created       DATETIME,
    active        BOOLEAN       NOT NULL,
    name          VARCHAR (200) NOT NULL,
    user_name     VARCHAR (100),
    user_email    VARCHAR (200),
    user_password VARCHAR (200) NOT NULL,
    is_admin      BOOLEAN,
    file_name     VARCHAR,
    file_url      VARCHAR,
    company       VARCHAR,
    occupation    VARCHAR,
    CHECK (active IN (0, 1) ),
    CHECK (is_admin IN (0, 1) )
);

CREATE TABLE xf_login_activities (
    internal   CHAR (32) NOT NULL,
    created    DATETIME,
    user_id    INTEGER,
    [action]   VARCHAR   NOT NULL,
    ip_address VARCHAR   NOT NULL,
    ua_header  VARCHAR   NOT NULL,
    ua_device  VARCHAR   NOT NULL,
    PRIMARY KEY (
        internal
    ),
    FOREIGN KEY (
        user_id
    )
    REFERENCES xf_user (id)
);
