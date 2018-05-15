
-- enable extensions --
-- full-text search on postgresql
-- enable features
CREATE TEXT SEARCH CONFIGURATION pt ( COPY = portuguese );
CREATE EXTENSION unaccent;

-- default features enabled on 'pt'
ALTER TEXT SEARCH CONFIGURATION pt ALTER MAPPING
FOR hword, hword_part, word WITH unaccent, portuguese_stem;

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";


-- table: user-group
DROP TABLE IF EXISTS xf_user_group;
CREATE TABLE IF NOT EXISTS xf_user_group(
    id bigserial not null primary key,
    internal uuid not null unique default uuid_generate_v4(),
    created timestamp not null default now(),
    created_user text not null,
    modified timestamp,
    modified_user text,
	name text not null,
	type text not null unique,
	description text
);

insert into xf_user_group(name, type) values ('Profile Root', 'ROO'),('Profile User', 'STD');

-- table: user
DROP TABLE IF EXISTS xf_user;
CREATE TABLE IF NOT EXISTS xf_user(
    id bigserial not null primary key,
    internal uuid not null unique default uuid_generate_v4(),
    created timestamp not null default now(),
    created_user text not null,
    modified timestamp,
    modified_user text,
	active boolean not null default false,
	name text not null,
	user_name text not null unique,
	user_email text not null unique,
	user_password text not null,
	phone text,
	document_main text,
	file_name text,
	file_url text,
	company text,
	occupation text,
	user_group_id bigint not null
);

alter table xf_user add constraint fk_user_group foreign key (user_group_id) references xf_user_group(id);

-- table: login-activities
DROP TABLE IF EXISTS xf_login_activities;
CREATE TABLE IF NOT EXISTS xf_login_activities (
    internal uuid not null primary key default uuid_generate_v4(),
    created timestamp not null default now(),
    user_id bigint not null,
    action text not null,
    ip_address text not null,
    ua_header text not null,
    ua_device text not null
);

alter table xf_login_activities add constraint fk_login_user foreign key (user_id) references xf_user(id);

-- table: authentication-api
DROP TABLE IF EXISTS xf_auth_api;
CREATE TABLE IF NOT EXISTS xf_auth_api (
    internal uuid not null primary key default uuid_generate_v4(),
	created timestamp not null default now(),
	created_user text not null,
    modified timestamp,
    modified_user text,
	client_secret text not null unique,
	api_key text not null unique
);

-- table: state
DROP TABLE IF EXISTS xf_state;
CREATE TABLE IF NOT EXISTS xf_state(
    initials text not null primary key,
    state text not null,
    capital text not null,
    region text not null
);

INSERT INTO xf_state VALUES ('AC','Acre','Rio Branco','Norte'),('AL','Alagoas','Maceió','Nordeste'),('AM','Amazonas','Manaus','Norte'),('AP','Amapá','Macapá','Norte'),('BA','Bahia','Salvador','Nordeste'),('CE','Ceará','Fortaleza','Nordeste'),('DF','Distrito Federal','Brasília','Centro-Oeste'),('ES','Espírito Santo','Vitória','Sudeste'),('GO','Goiás','Goiânia','Centro-Oeste'),('MA','Maranhão','São Luís','Nordeste'),('MG','Minas Gerais','Belo Horizonte','Sudeste'),('MS','Mato Grosso do Sul','Campo Grande','Centro-Oeste'),('MT','Mato Grosso','Cuiabá','Centro-Oeste'),('PA','Pará','Belém','Norte'),('PB','Paraíba','João Pessoa','Nordeste'),('PE','Pernambuco','Recife','Nordeste'),('PI','Piauí','Teresina','Nordeste'),('PR','Paraná','Curitiba','Sul'),('RJ','Rio de Janeiro','Rio de Janeiro','Sudeste'),('RN','Rio Grande do Norte','Natal','Nordeste'),('RO','Rondônia','Porto Velho','Nordeste'),('RR','Roraima','Boa Vista','Norte'),('RS','Rio Grande do Sul','Porto Alegre','Sul'),('SC','Santa Catarina','Florianópolis','Sul'),('SE','Sergipe','Aracaju','Nordeste'),('SP','São Paulo','São Paulo','Sudeste'),('TO','Tocantins','Palmas','Norte');

-- table: client-global
DROP TABLE IF EXISTS xf_client_global;
CREATE TABLE IF NOT EXISTS xf_client_global(
    id bigserial not null primary key,
    internal uuid not null unique default uuid_generate_v4(),
    created timestamp not null default now(),
    created_user text not null,
    modified timestamp,
    modified_user text,
    name text not null,
    document_main text not null,
    address_street text,
    address_complement text,
    address_zip text,
    address_district text,
    address_city text,
    address_state text,
    date_start date not null,
    date_end date not null
);

