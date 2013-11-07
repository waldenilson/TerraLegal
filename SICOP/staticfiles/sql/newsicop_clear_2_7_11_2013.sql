--
-- PostgreSQL database dump
--

-- Dumped from database version 9.2.4
-- Dumped by pg_dump version 9.2.4
-- Started on 2013-11-07 12:14:45

SET statement_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

DROP DATABASE newsicop;
--
-- TOC entry 2382 (class 1262 OID 71995)
-- Name: newsicop; Type: DATABASE; Schema: -; Owner: admin
--

CREATE DATABASE newsicop WITH TEMPLATE = template0 ENCODING = 'UTF8' LC_COLLATE = 'Portuguese_Brazil.1252' LC_CTYPE = 'Portuguese_Brazil.1252';


ALTER DATABASE newsicop OWNER TO admin;

\connect newsicop

SET statement_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

--
-- TOC entry 5 (class 2615 OID 2200)
-- Name: public; Type: SCHEMA; Schema: -; Owner: postgres
--

CREATE SCHEMA public;


ALTER SCHEMA public OWNER TO postgres;

--
-- TOC entry 2383 (class 0 OID 0)
-- Dependencies: 5
-- Name: SCHEMA public; Type: COMMENT; Schema: -; Owner: postgres
--

COMMENT ON SCHEMA public IS 'standard public schema';


--
-- TOC entry 228 (class 3079 OID 11727)
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- TOC entry 2385 (class 0 OID 0)
-- Dependencies: 228
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- TOC entry 168 (class 1259 OID 72139)
-- Name: auth_group; Type: TABLE; Schema: public; Owner: admin; Tablespace: 
--

CREATE TABLE auth_group (
    id integer NOT NULL,
    name character varying(80) NOT NULL
);


ALTER TABLE public.auth_group OWNER TO admin;

--
-- TOC entry 169 (class 1259 OID 72146)
-- Name: auth_group_permissions; Type: TABLE; Schema: public; Owner: admin; Tablespace: 
--

CREATE TABLE auth_group_permissions (
    id integer NOT NULL,
    group_id integer NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE public.auth_group_permissions OWNER TO admin;

--
-- TOC entry 170 (class 1259 OID 72156)
-- Name: auth_permission; Type: TABLE; Schema: public; Owner: admin; Tablespace: 
--

CREATE TABLE auth_permission (
    id integer NOT NULL,
    name character varying(50) NOT NULL,
    content_type_id integer NOT NULL,
    codename character varying(100) NOT NULL
);


ALTER TABLE public.auth_permission OWNER TO admin;

--
-- TOC entry 172 (class 1259 OID 72168)
-- Name: auth_user; Type: TABLE; Schema: public; Owner: admin; Tablespace: 
--

CREATE TABLE auth_user (
    password character varying(128) NOT NULL,
    last_login timestamp with time zone NOT NULL,
    is_superuser boolean NOT NULL,
    username character varying(30) NOT NULL,
    first_name character varying(30) NOT NULL,
    last_name character varying(30) NOT NULL,
    email character varying(75) NOT NULL,
    is_staff boolean NOT NULL,
    is_active boolean NOT NULL,
    date_joined timestamp with time zone NOT NULL,
    tbdivisao_id integer NOT NULL,
    id integer NOT NULL
);


ALTER TABLE public.auth_user OWNER TO admin;

--
-- TOC entry 174 (class 1259 OID 72178)
-- Name: auth_user_groups; Type: TABLE; Schema: public; Owner: admin; Tablespace: 
--

CREATE TABLE auth_user_groups (
    id integer NOT NULL,
    user_id integer NOT NULL,
    group_id integer NOT NULL
);


ALTER TABLE public.auth_user_groups OWNER TO admin;

--
-- TOC entry 173 (class 1259 OID 72176)
-- Name: auth_user_groups_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE auth_user_groups_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_user_groups_id_seq OWNER TO admin;

--
-- TOC entry 2386 (class 0 OID 0)
-- Dependencies: 173
-- Name: auth_user_groups_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE auth_user_groups_id_seq OWNED BY auth_user_groups.id;


--
-- TOC entry 171 (class 1259 OID 72166)
-- Name: auth_user_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE auth_user_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_user_id_seq OWNER TO admin;

--
-- TOC entry 2387 (class 0 OID 0)
-- Dependencies: 171
-- Name: auth_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE auth_user_id_seq OWNED BY auth_user.id;


--
-- TOC entry 175 (class 1259 OID 72194)
-- Name: auth_user_user_permissions; Type: TABLE; Schema: public; Owner: admin; Tablespace: 
--

CREATE TABLE auth_user_user_permissions (
    id integer NOT NULL,
    user_id integer NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE public.auth_user_user_permissions OWNER TO admin;

--
-- TOC entry 176 (class 1259 OID 72209)
-- Name: django_admin_log; Type: TABLE; Schema: public; Owner: admin; Tablespace: 
--

CREATE TABLE django_admin_log (
    id integer NOT NULL,
    action_time timestamp with time zone NOT NULL,
    user_id integer NOT NULL,
    content_type_id integer,
    object_id text NOT NULL,
    object_repr character varying(200) NOT NULL,
    action_flag smallint NOT NULL,
    change_message text NOT NULL
);


ALTER TABLE public.django_admin_log OWNER TO admin;

--
-- TOC entry 177 (class 1259 OID 72222)
-- Name: django_content_type; Type: TABLE; Schema: public; Owner: admin; Tablespace: 
--

CREATE TABLE django_content_type (
    id integer NOT NULL,
    name character varying(100) NOT NULL,
    app_label character varying(100) NOT NULL,
    model character varying(100) NOT NULL
);


ALTER TABLE public.django_content_type OWNER TO admin;

--
-- TOC entry 178 (class 1259 OID 72237)
-- Name: django_session; Type: TABLE; Schema: public; Owner: admin; Tablespace: 
--

CREATE TABLE django_session (
    session_key character varying(40) NOT NULL,
    session_data text NOT NULL,
    expire_date timestamp with time zone NOT NULL
);


ALTER TABLE public.django_session OWNER TO admin;

--
-- TOC entry 179 (class 1259 OID 72245)
-- Name: django_site; Type: TABLE; Schema: public; Owner: admin; Tablespace: 
--

CREATE TABLE django_site (
    id integer NOT NULL,
    domain character varying(100) NOT NULL,
    name character varying(50) NOT NULL
);


ALTER TABLE public.django_site OWNER TO admin;

--
-- TOC entry 181 (class 1259 OID 72252)
-- Name: tbcaixa; Type: TABLE; Schema: public; Owner: admin; Tablespace: 
--

CREATE TABLE tbcaixa (
    nmlocalarquivo character varying(80) NOT NULL,
    tbtipocaixa_id integer NOT NULL,
    id integer NOT NULL
);


ALTER TABLE public.tbcaixa OWNER TO admin;

--
-- TOC entry 180 (class 1259 OID 72250)
-- Name: tbcaixa_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE tbcaixa_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.tbcaixa_id_seq OWNER TO admin;

--
-- TOC entry 2388 (class 0 OID 0)
-- Dependencies: 180
-- Name: tbcaixa_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE tbcaixa_id_seq OWNED BY tbcaixa.id;


--
-- TOC entry 183 (class 1259 OID 72260)
-- Name: tbclassificacaoprocesso; Type: TABLE; Schema: public; Owner: admin; Tablespace: 
--

CREATE TABLE tbclassificacaoprocesso (
    nmclassificacao character varying(80) NOT NULL,
    tbdivisao_id integer,
    id integer NOT NULL
);


ALTER TABLE public.tbclassificacaoprocesso OWNER TO admin;

--
-- TOC entry 182 (class 1259 OID 72258)
-- Name: tbclassificacaoprocesso_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE tbclassificacaoprocesso_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.tbclassificacaoprocesso_id_seq OWNER TO admin;

--
-- TOC entry 2389 (class 0 OID 0)
-- Dependencies: 182
-- Name: tbclassificacaoprocesso_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE tbclassificacaoprocesso_id_seq OWNED BY tbclassificacaoprocesso.id;


--
-- TOC entry 185 (class 1259 OID 72268)
-- Name: tbcontrato; Type: TABLE; Schema: public; Owner: admin; Tablespace: 
--

CREATE TABLE tbcontrato (
    nrcontrato character varying(10) NOT NULL,
    nmempresa character varying(100) NOT NULL,
    tbdivisao_id integer,
    id integer NOT NULL
);


ALTER TABLE public.tbcontrato OWNER TO admin;

--
-- TOC entry 184 (class 1259 OID 72266)
-- Name: tbcontrato_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE tbcontrato_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.tbcontrato_id_seq OWNER TO admin;

--
-- TOC entry 2390 (class 0 OID 0)
-- Dependencies: 184
-- Name: tbcontrato_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE tbcontrato_id_seq OWNED BY tbcontrato.id;


--
-- TOC entry 187 (class 1259 OID 72276)
-- Name: tbdivisao; Type: TABLE; Schema: public; Owner: admin; Tablespace: 
--

CREATE TABLE tbdivisao (
    nmdivisao character varying(80) NOT NULL,
    dsdivisao text NOT NULL,
    tbuf_id integer,
    id integer NOT NULL
);


ALTER TABLE public.tbdivisao OWNER TO admin;

--
-- TOC entry 186 (class 1259 OID 72274)
-- Name: tbdivisao_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE tbdivisao_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.tbdivisao_id_seq OWNER TO admin;

--
-- TOC entry 2391 (class 0 OID 0)
-- Dependencies: 186
-- Name: tbdivisao_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE tbdivisao_id_seq OWNED BY tbdivisao.id;


--
-- TOC entry 189 (class 1259 OID 72302)
-- Name: tbgleba; Type: TABLE; Schema: public; Owner: admin; Tablespace: 
--

CREATE TABLE tbgleba (
    cdgleba integer,
    nmgleba character varying(80) NOT NULL,
    tbsubarea_id integer NOT NULL,
    id integer NOT NULL
);


ALTER TABLE public.tbgleba OWNER TO admin;

--
-- TOC entry 188 (class 1259 OID 72300)
-- Name: tbgleba_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE tbgleba_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.tbgleba_id_seq OWNER TO admin;

--
-- TOC entry 2392 (class 0 OID 0)
-- Dependencies: 188
-- Name: tbgleba_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE tbgleba_id_seq OWNED BY tbgleba.id;


--
-- TOC entry 191 (class 1259 OID 72310)
-- Name: tbmovimentacao; Type: TABLE; Schema: public; Owner: admin; Tablespace: 
--

CREATE TABLE tbmovimentacao (
    tbprocessobase_id integer NOT NULL,
    dtmovimentacao timestamp with time zone,
    tbcaixa_id_origem integer NOT NULL,
    tbcaixa_id integer NOT NULL,
    auth_user_id integer NOT NULL,
    nrdias integer,
    id integer NOT NULL
);


ALTER TABLE public.tbmovimentacao OWNER TO admin;

--
-- TOC entry 190 (class 1259 OID 72308)
-- Name: tbmovimentacao_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE tbmovimentacao_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.tbmovimentacao_id_seq OWNER TO admin;

--
-- TOC entry 2393 (class 0 OID 0)
-- Dependencies: 190
-- Name: tbmovimentacao_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE tbmovimentacao_id_seq OWNED BY tbmovimentacao.id;


--
-- TOC entry 193 (class 1259 OID 72333)
-- Name: tbmunicipio; Type: TABLE; Schema: public; Owner: admin; Tablespace: 
--

CREATE TABLE tbmunicipio (
    "Nome_Mun_Maiusculo" character varying(50) NOT NULL,
    "Nome_Mun" character varying(50) NOT NULL,
    "Codigo_Mun" integer,
    "Regiao" character varying(50),
    "Nome_Estado" character varying(50),
    "UF" character varying(2) NOT NULL,
    "SR" character varying(50),
    "Codigo_UF" integer,
    "Populacao" character varying(50),
    nrmodulofiscal integer,
    nrfracaominima integer,
    id integer NOT NULL
);


ALTER TABLE public.tbmunicipio OWNER TO admin;

--
-- TOC entry 192 (class 1259 OID 72331)
-- Name: tbmunicipio_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE tbmunicipio_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.tbmunicipio_id_seq OWNER TO admin;

--
-- TOC entry 2394 (class 0 OID 0)
-- Dependencies: 192
-- Name: tbmunicipio_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE tbmunicipio_id_seq OWNED BY tbmunicipio.id;


--
-- TOC entry 195 (class 1259 OID 72341)
-- Name: tbpecastecnicas; Type: TABLE; Schema: public; Owner: admin; Tablespace: 
--

CREATE TABLE tbpecastecnicas (
    cdpeca character varying(50) NOT NULL,
    tbcontrato_id integer NOT NULL,
    nrentrega character varying(10) NOT NULL,
    nrcpfrequerente character varying(14) NOT NULL,
    nmrequerente character varying(80) NOT NULL,
    stenviadobrasilia boolean NOT NULL,
    stpecatecnica boolean NOT NULL,
    stanexadoprocesso boolean NOT NULL,
    dsobservacao text NOT NULL,
    tbcaixa_id integer NOT NULL,
    nrarea numeric(10,4),
    nrperimetro numeric(18,4),
    tbgleba_id integer NOT NULL,
    tbdivisao_id integer,
    id integer NOT NULL
);


ALTER TABLE public.tbpecastecnicas OWNER TO admin;

--
-- TOC entry 194 (class 1259 OID 72339)
-- Name: tbpecastecnicas_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE tbpecastecnicas_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.tbpecastecnicas_id_seq OWNER TO admin;

--
-- TOC entry 2395 (class 0 OID 0)
-- Dependencies: 194
-- Name: tbpecastecnicas_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE tbpecastecnicas_id_seq OWNED BY tbpecastecnicas.id;


--
-- TOC entry 197 (class 1259 OID 72372)
-- Name: tbpendencia; Type: TABLE; Schema: public; Owner: admin; Tablespace: 
--

CREATE TABLE tbpendencia (
    nrcodigo character varying(50) NOT NULL,
    tbprocessobase_id integer NOT NULL,
    tbtipopendencia_id integer NOT NULL,
    dsdescricao text NOT NULL,
    dtpendencia timestamp with time zone,
    auth_user_id integer NOT NULL,
    tbstatuspendencia_id integer NOT NULL,
    id integer NOT NULL
);


ALTER TABLE public.tbpendencia OWNER TO admin;

--
-- TOC entry 196 (class 1259 OID 72370)
-- Name: tbpendencia_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE tbpendencia_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.tbpendencia_id_seq OWNER TO admin;

--
-- TOC entry 2396 (class 0 OID 0)
-- Dependencies: 196
-- Name: tbpendencia_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE tbpendencia_id_seq OWNED BY tbpendencia.id;


--
-- TOC entry 227 (class 1259 OID 72675)
-- Name: tbpregao; Type: TABLE; Schema: public; Owner: admin; Tablespace: 
--

CREATE TABLE tbpregao (
    nrpregao character varying(30) NOT NULL,
    dspregao text NOT NULL,
    tbdivisao_id integer,
    id integer NOT NULL
);


ALTER TABLE public.tbpregao OWNER TO admin;

--
-- TOC entry 226 (class 1259 OID 72673)
-- Name: tbpregao_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE tbpregao_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.tbpregao_id_seq OWNER TO admin;

--
-- TOC entry 2397 (class 0 OID 0)
-- Dependencies: 226
-- Name: tbpregao_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE tbpregao_id_seq OWNED BY tbpregao.id;


--
-- TOC entry 199 (class 1259 OID 72388)
-- Name: tbprocessobase; Type: TABLE; Schema: public; Owner: admin; Tablespace: 
--

CREATE TABLE tbprocessobase (
    nrprocesso character varying(17) NOT NULL,
    tbgleba_id integer NOT NULL,
    tbcaixa_id integer NOT NULL,
    tbmunicipio_id integer NOT NULL,
    auth_user_id integer NOT NULL,
    tbtipoprocesso_id integer NOT NULL,
    tbsituacaoprocesso_id integer,
    dtcadastrosistema timestamp with time zone,
    tbclassificacaoprocesso_id integer,
    tbdivisao_id integer NOT NULL,
    id integer NOT NULL
);


ALTER TABLE public.tbprocessobase OWNER TO admin;

--
-- TOC entry 198 (class 1259 OID 72386)
-- Name: tbprocessobase_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE tbprocessobase_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.tbprocessobase_id_seq OWNER TO admin;

--
-- TOC entry 2398 (class 0 OID 0)
-- Dependencies: 198
-- Name: tbprocessobase_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE tbprocessobase_id_seq OWNED BY tbprocessobase.id;


--
-- TOC entry 201 (class 1259 OID 72436)
-- Name: tbprocessoclausula; Type: TABLE; Schema: public; Owner: admin; Tablespace: 
--

CREATE TABLE tbprocessoclausula (
    tbprocessobase_id integer NOT NULL,
    nmrequerente character varying(100) NOT NULL,
    nminteressado character varying(100) NOT NULL,
    nrcpfrequerente character varying(11) NOT NULL,
    nrcpfinteressado character varying(11) NOT NULL,
    nrarea numeric(10,4),
    cdstatus integer,
    dsobs text NOT NULL,
    stprocuracao boolean NOT NULL,
    dttitulacao timestamp with time zone,
    id integer NOT NULL
);


ALTER TABLE public.tbprocessoclausula OWNER TO admin;

--
-- TOC entry 200 (class 1259 OID 72434)
-- Name: tbprocessoclausula_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE tbprocessoclausula_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.tbprocessoclausula_id_seq OWNER TO admin;

--
-- TOC entry 2399 (class 0 OID 0)
-- Dependencies: 200
-- Name: tbprocessoclausula_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE tbprocessoclausula_id_seq OWNED BY tbprocessoclausula.id;


--
-- TOC entry 203 (class 1259 OID 72452)
-- Name: tbprocessorural; Type: TABLE; Schema: public; Owner: admin; Tablespace: 
--

CREATE TABLE tbprocessorural (
    tbprocessobase_id integer NOT NULL,
    nmrequerente character varying(100) NOT NULL,
    nrcpfrequerente character varying(11) NOT NULL,
    blconjuge boolean NOT NULL,
    cdstatus integer,
    nrcpfconjuge character varying(11) NOT NULL,
    nmconjuge character varying(50) NOT NULL,
    id integer NOT NULL
);


ALTER TABLE public.tbprocessorural OWNER TO admin;

--
-- TOC entry 202 (class 1259 OID 72450)
-- Name: tbprocessorural_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE tbprocessorural_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.tbprocessorural_id_seq OWNER TO admin;

--
-- TOC entry 2400 (class 0 OID 0)
-- Dependencies: 202
-- Name: tbprocessorural_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE tbprocessorural_id_seq OWNED BY tbprocessorural.id;


--
-- TOC entry 205 (class 1259 OID 72465)
-- Name: tbprocessosanexos; Type: TABLE; Schema: public; Owner: admin; Tablespace: 
--

CREATE TABLE tbprocessosanexos (
    tbprocessobase_id integer NOT NULL,
    tbprocessobase_id_anexo integer NOT NULL,
    dtanexado timestamp with time zone,
    auth_user_id integer NOT NULL,
    id integer NOT NULL
);


ALTER TABLE public.tbprocessosanexos OWNER TO admin;

--
-- TOC entry 204 (class 1259 OID 72463)
-- Name: tbprocessosanexos_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE tbprocessosanexos_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.tbprocessosanexos_id_seq OWNER TO admin;

--
-- TOC entry 2401 (class 0 OID 0)
-- Dependencies: 204
-- Name: tbprocessosanexos_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE tbprocessosanexos_id_seq OWNED BY tbprocessosanexos.id;


--
-- TOC entry 207 (class 1259 OID 72488)
-- Name: tbprocessourbano; Type: TABLE; Schema: public; Owner: admin; Tablespace: 
--

CREATE TABLE tbprocessourbano (
    tbprocessobase_id integer NOT NULL,
    nmpovoado character varying(80) NOT NULL,
    nrcnpj character varying(14) NOT NULL,
    dtaberturaprocesso timestamp with time zone,
    dttitulacao timestamp with time zone,
    nrarea numeric(10,4),
    nrperimetro numeric(18,4),
    nrdomicilios integer,
    nrhabitantes integer,
    tbpregao_id integer NOT NULL,
    tbcontrato_id integer NOT NULL,
    tbsituacaogeo_id integer,
    dsprojetoassentamento character varying(80) NOT NULL,
    id integer NOT NULL
);


ALTER TABLE public.tbprocessourbano OWNER TO admin;

--
-- TOC entry 206 (class 1259 OID 72486)
-- Name: tbprocessourbano_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE tbprocessourbano_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.tbprocessourbano_id_seq OWNER TO admin;

--
-- TOC entry 2402 (class 0 OID 0)
-- Dependencies: 206
-- Name: tbprocessourbano_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE tbprocessourbano_id_seq OWNED BY tbprocessourbano.id;


--
-- TOC entry 209 (class 1259 OID 72506)
-- Name: tbservidor; Type: TABLE; Schema: public; Owner: admin; Tablespace: 
--

CREATE TABLE tbservidor (
    nmservidor character varying(100) NOT NULL,
    nmunidade character varying(100) NOT NULL,
    nmlotacao character varying(30) NOT NULL,
    cdsiape character varying(7) NOT NULL,
    nrcpf character varying(11) NOT NULL,
    dsportariacargo text NOT NULL,
    dsportaria text NOT NULL,
    nmcargo character varying(80) NOT NULL,
    nrtelefone1 character varying(10) NOT NULL,
    nrtelefone2 character varying(10) NOT NULL,
    email character varying(75) NOT NULL,
    dsatividades text NOT NULL,
    id integer NOT NULL
);


ALTER TABLE public.tbservidor OWNER TO admin;

--
-- TOC entry 208 (class 1259 OID 72504)
-- Name: tbservidor_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE tbservidor_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.tbservidor_id_seq OWNER TO admin;

--
-- TOC entry 2403 (class 0 OID 0)
-- Dependencies: 208
-- Name: tbservidor_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE tbservidor_id_seq OWNED BY tbservidor.id;


--
-- TOC entry 211 (class 1259 OID 72517)
-- Name: tbsituacaogeo; Type: TABLE; Schema: public; Owner: admin; Tablespace: 
--

CREATE TABLE tbsituacaogeo (
    nmsituacaogeo character varying(80) NOT NULL,
    dssituacaogeo text NOT NULL,
    tbdivisao_id integer,
    id integer NOT NULL
);


ALTER TABLE public.tbsituacaogeo OWNER TO admin;

--
-- TOC entry 210 (class 1259 OID 72515)
-- Name: tbsituacaogeo_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE tbsituacaogeo_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.tbsituacaogeo_id_seq OWNER TO admin;

--
-- TOC entry 2404 (class 0 OID 0)
-- Dependencies: 210
-- Name: tbsituacaogeo_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE tbsituacaogeo_id_seq OWNED BY tbsituacaogeo.id;


--
-- TOC entry 213 (class 1259 OID 72538)
-- Name: tbsituacaoprocesso; Type: TABLE; Schema: public; Owner: admin; Tablespace: 
--

CREATE TABLE tbsituacaoprocesso (
    nmsituacao character varying(80) NOT NULL,
    dssituacao text NOT NULL,
    tbdivisao_id integer,
    id integer NOT NULL
);


ALTER TABLE public.tbsituacaoprocesso OWNER TO admin;

--
-- TOC entry 212 (class 1259 OID 72536)
-- Name: tbsituacaoprocesso_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE tbsituacaoprocesso_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.tbsituacaoprocesso_id_seq OWNER TO admin;

--
-- TOC entry 2405 (class 0 OID 0)
-- Dependencies: 212
-- Name: tbsituacaoprocesso_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE tbsituacaoprocesso_id_seq OWNED BY tbsituacaoprocesso.id;


--
-- TOC entry 215 (class 1259 OID 72559)
-- Name: tbstatuspendencia; Type: TABLE; Schema: public; Owner: admin; Tablespace: 
--

CREATE TABLE tbstatuspendencia (
    stpendencia integer,
    dspendencia character varying(100) NOT NULL,
    tbdivisao_id integer,
    id integer NOT NULL
);


ALTER TABLE public.tbstatuspendencia OWNER TO admin;

--
-- TOC entry 214 (class 1259 OID 72557)
-- Name: tbstatuspendencia_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE tbstatuspendencia_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.tbstatuspendencia_id_seq OWNER TO admin;

--
-- TOC entry 2406 (class 0 OID 0)
-- Dependencies: 214
-- Name: tbstatuspendencia_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE tbstatuspendencia_id_seq OWNED BY tbstatuspendencia.id;


--
-- TOC entry 217 (class 1259 OID 72577)
-- Name: tbsubarea; Type: TABLE; Schema: public; Owner: admin; Tablespace: 
--

CREATE TABLE tbsubarea (
    cdsubarea character varying(10) NOT NULL,
    nmsubarea character varying(80) NOT NULL,
    tbdivisao_id integer,
    id integer NOT NULL
);


ALTER TABLE public.tbsubarea OWNER TO admin;

--
-- TOC entry 216 (class 1259 OID 72575)
-- Name: tbsubarea_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE tbsubarea_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.tbsubarea_id_seq OWNER TO admin;

--
-- TOC entry 2407 (class 0 OID 0)
-- Dependencies: 216
-- Name: tbsubarea_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE tbsubarea_id_seq OWNED BY tbsubarea.id;


--
-- TOC entry 219 (class 1259 OID 72595)
-- Name: tbtipocaixa; Type: TABLE; Schema: public; Owner: admin; Tablespace: 
--

CREATE TABLE tbtipocaixa (
    nmtipocaixa character varying(80) NOT NULL,
    desctipocaixa text NOT NULL,
    tbdivisao_id integer,
    id integer NOT NULL
);


ALTER TABLE public.tbtipocaixa OWNER TO admin;

--
-- TOC entry 218 (class 1259 OID 72593)
-- Name: tbtipocaixa_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE tbtipocaixa_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.tbtipocaixa_id_seq OWNER TO admin;

--
-- TOC entry 2408 (class 0 OID 0)
-- Dependencies: 218
-- Name: tbtipocaixa_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE tbtipocaixa_id_seq OWNED BY tbtipocaixa.id;


--
-- TOC entry 221 (class 1259 OID 72616)
-- Name: tbtipopendencia; Type: TABLE; Schema: public; Owner: admin; Tablespace: 
--

CREATE TABLE tbtipopendencia (
    cdtipopend integer,
    dspendencia character varying(50) NOT NULL,
    cdgrupo character varying(20) NOT NULL,
    tbdivisao_id integer,
    tbtipoprocesso_id integer NOT NULL,
    id integer NOT NULL
);


ALTER TABLE public.tbtipopendencia OWNER TO admin;

--
-- TOC entry 220 (class 1259 OID 72614)
-- Name: tbtipopendencia_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE tbtipopendencia_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.tbtipopendencia_id_seq OWNER TO admin;

--
-- TOC entry 2409 (class 0 OID 0)
-- Dependencies: 220
-- Name: tbtipopendencia_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE tbtipopendencia_id_seq OWNED BY tbtipopendencia.id;


--
-- TOC entry 223 (class 1259 OID 72634)
-- Name: tbtipoprocesso; Type: TABLE; Schema: public; Owner: admin; Tablespace: 
--

CREATE TABLE tbtipoprocesso (
    nome character varying(80) NOT NULL,
    tabela character varying(50) NOT NULL,
    coridentificacao character varying(20) NOT NULL,
    tbdivisao_id integer,
    id integer NOT NULL
);


ALTER TABLE public.tbtipoprocesso OWNER TO admin;

--
-- TOC entry 222 (class 1259 OID 72632)
-- Name: tbtipoprocesso_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE tbtipoprocesso_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.tbtipoprocesso_id_seq OWNER TO admin;

--
-- TOC entry 2410 (class 0 OID 0)
-- Dependencies: 222
-- Name: tbtipoprocesso_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE tbtipoprocesso_id_seq OWNED BY tbtipoprocesso.id;


--
-- TOC entry 225 (class 1259 OID 72657)
-- Name: tbuf; Type: TABLE; Schema: public; Owner: admin; Tablespace: 
--

CREATE TABLE tbuf (
    sigla character varying(2) NOT NULL,
    nmuf character varying(50) NOT NULL,
    id integer NOT NULL
);


ALTER TABLE public.tbuf OWNER TO admin;

--
-- TOC entry 224 (class 1259 OID 72655)
-- Name: tbuf_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE tbuf_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.tbuf_id_seq OWNER TO admin;

--
-- TOC entry 2411 (class 0 OID 0)
-- Dependencies: 224
-- Name: tbuf_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE tbuf_id_seq OWNED BY tbuf.id;


--
-- TOC entry 2109 (class 2604 OID 72171)
-- Name: id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY auth_user ALTER COLUMN id SET DEFAULT nextval('auth_user_id_seq'::regclass);


--
-- TOC entry 2110 (class 2604 OID 72181)
-- Name: id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY auth_user_groups ALTER COLUMN id SET DEFAULT nextval('auth_user_groups_id_seq'::regclass);


--
-- TOC entry 2111 (class 2604 OID 72255)
-- Name: id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbcaixa ALTER COLUMN id SET DEFAULT nextval('tbcaixa_id_seq'::regclass);


--
-- TOC entry 2112 (class 2604 OID 72263)
-- Name: id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbclassificacaoprocesso ALTER COLUMN id SET DEFAULT nextval('tbclassificacaoprocesso_id_seq'::regclass);


--
-- TOC entry 2113 (class 2604 OID 72271)
-- Name: id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbcontrato ALTER COLUMN id SET DEFAULT nextval('tbcontrato_id_seq'::regclass);


--
-- TOC entry 2114 (class 2604 OID 72279)
-- Name: id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbdivisao ALTER COLUMN id SET DEFAULT nextval('tbdivisao_id_seq'::regclass);


--
-- TOC entry 2115 (class 2604 OID 72305)
-- Name: id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbgleba ALTER COLUMN id SET DEFAULT nextval('tbgleba_id_seq'::regclass);


--
-- TOC entry 2116 (class 2604 OID 72313)
-- Name: id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbmovimentacao ALTER COLUMN id SET DEFAULT nextval('tbmovimentacao_id_seq'::regclass);


--
-- TOC entry 2117 (class 2604 OID 72336)
-- Name: id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbmunicipio ALTER COLUMN id SET DEFAULT nextval('tbmunicipio_id_seq'::regclass);


--
-- TOC entry 2118 (class 2604 OID 72344)
-- Name: id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbpecastecnicas ALTER COLUMN id SET DEFAULT nextval('tbpecastecnicas_id_seq'::regclass);


--
-- TOC entry 2119 (class 2604 OID 72375)
-- Name: id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbpendencia ALTER COLUMN id SET DEFAULT nextval('tbpendencia_id_seq'::regclass);


--
-- TOC entry 2134 (class 2604 OID 72678)
-- Name: id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbpregao ALTER COLUMN id SET DEFAULT nextval('tbpregao_id_seq'::regclass);


--
-- TOC entry 2120 (class 2604 OID 72391)
-- Name: id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbprocessobase ALTER COLUMN id SET DEFAULT nextval('tbprocessobase_id_seq'::regclass);


--
-- TOC entry 2121 (class 2604 OID 72439)
-- Name: id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbprocessoclausula ALTER COLUMN id SET DEFAULT nextval('tbprocessoclausula_id_seq'::regclass);


--
-- TOC entry 2122 (class 2604 OID 72455)
-- Name: id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbprocessorural ALTER COLUMN id SET DEFAULT nextval('tbprocessorural_id_seq'::regclass);


--
-- TOC entry 2123 (class 2604 OID 72468)
-- Name: id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbprocessosanexos ALTER COLUMN id SET DEFAULT nextval('tbprocessosanexos_id_seq'::regclass);


--
-- TOC entry 2124 (class 2604 OID 72491)
-- Name: id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbprocessourbano ALTER COLUMN id SET DEFAULT nextval('tbprocessourbano_id_seq'::regclass);


--
-- TOC entry 2125 (class 2604 OID 72509)
-- Name: id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbservidor ALTER COLUMN id SET DEFAULT nextval('tbservidor_id_seq'::regclass);


--
-- TOC entry 2126 (class 2604 OID 72520)
-- Name: id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbsituacaogeo ALTER COLUMN id SET DEFAULT nextval('tbsituacaogeo_id_seq'::regclass);


--
-- TOC entry 2127 (class 2604 OID 72541)
-- Name: id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbsituacaoprocesso ALTER COLUMN id SET DEFAULT nextval('tbsituacaoprocesso_id_seq'::regclass);


--
-- TOC entry 2128 (class 2604 OID 72562)
-- Name: id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbstatuspendencia ALTER COLUMN id SET DEFAULT nextval('tbstatuspendencia_id_seq'::regclass);


--
-- TOC entry 2129 (class 2604 OID 72580)
-- Name: id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbsubarea ALTER COLUMN id SET DEFAULT nextval('tbsubarea_id_seq'::regclass);


--
-- TOC entry 2130 (class 2604 OID 72598)
-- Name: id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbtipocaixa ALTER COLUMN id SET DEFAULT nextval('tbtipocaixa_id_seq'::regclass);


--
-- TOC entry 2131 (class 2604 OID 72619)
-- Name: id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbtipopendencia ALTER COLUMN id SET DEFAULT nextval('tbtipopendencia_id_seq'::regclass);


--
-- TOC entry 2132 (class 2604 OID 72637)
-- Name: id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbtipoprocesso ALTER COLUMN id SET DEFAULT nextval('tbtipoprocesso_id_seq'::regclass);


--
-- TOC entry 2133 (class 2604 OID 72660)
-- Name: id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbuf ALTER COLUMN id SET DEFAULT nextval('tbuf_id_seq'::regclass);


--
-- TOC entry 2318 (class 0 OID 72139)
-- Dependencies: 168
-- Data for Name: auth_group; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY auth_group (id, name) FROM stdin;
\.


--
-- TOC entry 2319 (class 0 OID 72146)
-- Dependencies: 169
-- Data for Name: auth_group_permissions; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY auth_group_permissions (id, group_id, permission_id) FROM stdin;
\.


--
-- TOC entry 2320 (class 0 OID 72156)
-- Dependencies: 170
-- Data for Name: auth_permission; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY auth_permission (id, name, content_type_id, codename) FROM stdin;
\.


--
-- TOC entry 2322 (class 0 OID 72168)
-- Dependencies: 172
-- Data for Name: auth_user; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY auth_user (password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined, tbdivisao_id, id) FROM stdin;
\.


--
-- TOC entry 2324 (class 0 OID 72178)
-- Dependencies: 174
-- Data for Name: auth_user_groups; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY auth_user_groups (id, user_id, group_id) FROM stdin;
\.


--
-- TOC entry 2412 (class 0 OID 0)
-- Dependencies: 173
-- Name: auth_user_groups_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('auth_user_groups_id_seq', 1, false);


--
-- TOC entry 2413 (class 0 OID 0)
-- Dependencies: 171
-- Name: auth_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('auth_user_id_seq', 1, false);


--
-- TOC entry 2325 (class 0 OID 72194)
-- Dependencies: 175
-- Data for Name: auth_user_user_permissions; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY auth_user_user_permissions (id, user_id, permission_id) FROM stdin;
\.


--
-- TOC entry 2326 (class 0 OID 72209)
-- Dependencies: 176
-- Data for Name: django_admin_log; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY django_admin_log (id, action_time, user_id, content_type_id, object_id, object_repr, action_flag, change_message) FROM stdin;
\.


--
-- TOC entry 2327 (class 0 OID 72222)
-- Dependencies: 177
-- Data for Name: django_content_type; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY django_content_type (id, name, app_label, model) FROM stdin;
\.


--
-- TOC entry 2328 (class 0 OID 72237)
-- Dependencies: 178
-- Data for Name: django_session; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY django_session (session_key, session_data, expire_date) FROM stdin;
mue4jzlj4463s8xp8qno3euahooryvdw	NWE5NmE2NTc3MWFkYTI5ODgyOGQ3OWE0ZjgxMzQwZmYzMTg0YmJhNDqAAn1xAS4=	2013-11-21 11:04:53.914-02
\.


--
-- TOC entry 2329 (class 0 OID 72245)
-- Dependencies: 179
-- Data for Name: django_site; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY django_site (id, domain, name) FROM stdin;
\.


--
-- TOC entry 2331 (class 0 OID 72252)
-- Dependencies: 181
-- Data for Name: tbcaixa; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY tbcaixa (nmlocalarquivo, tbtipocaixa_id, id) FROM stdin;
\.


--
-- TOC entry 2414 (class 0 OID 0)
-- Dependencies: 180
-- Name: tbcaixa_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('tbcaixa_id_seq', 1, false);


--
-- TOC entry 2333 (class 0 OID 72260)
-- Dependencies: 183
-- Data for Name: tbclassificacaoprocesso; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY tbclassificacaoprocesso (nmclassificacao, tbdivisao_id, id) FROM stdin;
\.


--
-- TOC entry 2415 (class 0 OID 0)
-- Dependencies: 182
-- Name: tbclassificacaoprocesso_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('tbclassificacaoprocesso_id_seq', 1, false);


--
-- TOC entry 2335 (class 0 OID 72268)
-- Dependencies: 185
-- Data for Name: tbcontrato; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY tbcontrato (nrcontrato, nmempresa, tbdivisao_id, id) FROM stdin;
\.


--
-- TOC entry 2416 (class 0 OID 0)
-- Dependencies: 184
-- Name: tbcontrato_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('tbcontrato_id_seq', 1, false);


--
-- TOC entry 2337 (class 0 OID 72276)
-- Dependencies: 187
-- Data for Name: tbdivisao; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY tbdivisao (nmdivisao, dsdivisao, tbuf_id, id) FROM stdin;
\.


--
-- TOC entry 2417 (class 0 OID 0)
-- Dependencies: 186
-- Name: tbdivisao_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('tbdivisao_id_seq', 1, false);


--
-- TOC entry 2339 (class 0 OID 72302)
-- Dependencies: 189
-- Data for Name: tbgleba; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY tbgleba (cdgleba, nmgleba, tbsubarea_id, id) FROM stdin;
\.


--
-- TOC entry 2418 (class 0 OID 0)
-- Dependencies: 188
-- Name: tbgleba_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('tbgleba_id_seq', 1, false);


--
-- TOC entry 2341 (class 0 OID 72310)
-- Dependencies: 191
-- Data for Name: tbmovimentacao; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY tbmovimentacao (tbprocessobase_id, dtmovimentacao, tbcaixa_id_origem, tbcaixa_id, auth_user_id, nrdias, id) FROM stdin;
\.


--
-- TOC entry 2419 (class 0 OID 0)
-- Dependencies: 190
-- Name: tbmovimentacao_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('tbmovimentacao_id_seq', 1, false);


--
-- TOC entry 2343 (class 0 OID 72333)
-- Dependencies: 193
-- Data for Name: tbmunicipio; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY tbmunicipio ("Nome_Mun_Maiusculo", "Nome_Mun", "Codigo_Mun", "Regiao", "Nome_Estado", "UF", "SR", "Codigo_UF", "Populacao", nrmodulofiscal, nrfracaominima, id) FROM stdin;
\.


--
-- TOC entry 2420 (class 0 OID 0)
-- Dependencies: 192
-- Name: tbmunicipio_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('tbmunicipio_id_seq', 1, false);


--
-- TOC entry 2345 (class 0 OID 72341)
-- Dependencies: 195
-- Data for Name: tbpecastecnicas; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY tbpecastecnicas (cdpeca, tbcontrato_id, nrentrega, nrcpfrequerente, nmrequerente, stenviadobrasilia, stpecatecnica, stanexadoprocesso, dsobservacao, tbcaixa_id, nrarea, nrperimetro, tbgleba_id, tbdivisao_id, id) FROM stdin;
\.


--
-- TOC entry 2421 (class 0 OID 0)
-- Dependencies: 194
-- Name: tbpecastecnicas_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('tbpecastecnicas_id_seq', 1, false);


--
-- TOC entry 2347 (class 0 OID 72372)
-- Dependencies: 197
-- Data for Name: tbpendencia; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY tbpendencia (nrcodigo, tbprocessobase_id, tbtipopendencia_id, dsdescricao, dtpendencia, auth_user_id, tbstatuspendencia_id, id) FROM stdin;
\.


--
-- TOC entry 2422 (class 0 OID 0)
-- Dependencies: 196
-- Name: tbpendencia_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('tbpendencia_id_seq', 1, false);


--
-- TOC entry 2377 (class 0 OID 72675)
-- Dependencies: 227
-- Data for Name: tbpregao; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY tbpregao (nrpregao, dspregao, tbdivisao_id, id) FROM stdin;
\.


--
-- TOC entry 2423 (class 0 OID 0)
-- Dependencies: 226
-- Name: tbpregao_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('tbpregao_id_seq', 1, false);


--
-- TOC entry 2349 (class 0 OID 72388)
-- Dependencies: 199
-- Data for Name: tbprocessobase; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY tbprocessobase (nrprocesso, tbgleba_id, tbcaixa_id, tbmunicipio_id, auth_user_id, tbtipoprocesso_id, tbsituacaoprocesso_id, dtcadastrosistema, tbclassificacaoprocesso_id, tbdivisao_id, id) FROM stdin;
\.


--
-- TOC entry 2424 (class 0 OID 0)
-- Dependencies: 198
-- Name: tbprocessobase_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('tbprocessobase_id_seq', 1, false);


--
-- TOC entry 2351 (class 0 OID 72436)
-- Dependencies: 201
-- Data for Name: tbprocessoclausula; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY tbprocessoclausula (tbprocessobase_id, nmrequerente, nminteressado, nrcpfrequerente, nrcpfinteressado, nrarea, cdstatus, dsobs, stprocuracao, dttitulacao, id) FROM stdin;
\.


--
-- TOC entry 2425 (class 0 OID 0)
-- Dependencies: 200
-- Name: tbprocessoclausula_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('tbprocessoclausula_id_seq', 1, false);


--
-- TOC entry 2353 (class 0 OID 72452)
-- Dependencies: 203
-- Data for Name: tbprocessorural; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY tbprocessorural (tbprocessobase_id, nmrequerente, nrcpfrequerente, blconjuge, cdstatus, nrcpfconjuge, nmconjuge, id) FROM stdin;
\.


--
-- TOC entry 2426 (class 0 OID 0)
-- Dependencies: 202
-- Name: tbprocessorural_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('tbprocessorural_id_seq', 1, false);


--
-- TOC entry 2355 (class 0 OID 72465)
-- Dependencies: 205
-- Data for Name: tbprocessosanexos; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY tbprocessosanexos (tbprocessobase_id, tbprocessobase_id_anexo, dtanexado, auth_user_id, id) FROM stdin;
\.


--
-- TOC entry 2427 (class 0 OID 0)
-- Dependencies: 204
-- Name: tbprocessosanexos_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('tbprocessosanexos_id_seq', 1, false);


--
-- TOC entry 2357 (class 0 OID 72488)
-- Dependencies: 207
-- Data for Name: tbprocessourbano; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY tbprocessourbano (tbprocessobase_id, nmpovoado, nrcnpj, dtaberturaprocesso, dttitulacao, nrarea, nrperimetro, nrdomicilios, nrhabitantes, tbpregao_id, tbcontrato_id, tbsituacaogeo_id, dsprojetoassentamento, id) FROM stdin;
\.


--
-- TOC entry 2428 (class 0 OID 0)
-- Dependencies: 206
-- Name: tbprocessourbano_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('tbprocessourbano_id_seq', 1, false);


--
-- TOC entry 2359 (class 0 OID 72506)
-- Dependencies: 209
-- Data for Name: tbservidor; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY tbservidor (nmservidor, nmunidade, nmlotacao, cdsiape, nrcpf, dsportariacargo, dsportaria, nmcargo, nrtelefone1, nrtelefone2, email, dsatividades, id) FROM stdin;
\.


--
-- TOC entry 2429 (class 0 OID 0)
-- Dependencies: 208
-- Name: tbservidor_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('tbservidor_id_seq', 1, false);


--
-- TOC entry 2361 (class 0 OID 72517)
-- Dependencies: 211
-- Data for Name: tbsituacaogeo; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY tbsituacaogeo (nmsituacaogeo, dssituacaogeo, tbdivisao_id, id) FROM stdin;
\.


--
-- TOC entry 2430 (class 0 OID 0)
-- Dependencies: 210
-- Name: tbsituacaogeo_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('tbsituacaogeo_id_seq', 1, false);


--
-- TOC entry 2363 (class 0 OID 72538)
-- Dependencies: 213
-- Data for Name: tbsituacaoprocesso; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY tbsituacaoprocesso (nmsituacao, dssituacao, tbdivisao_id, id) FROM stdin;
\.


--
-- TOC entry 2431 (class 0 OID 0)
-- Dependencies: 212
-- Name: tbsituacaoprocesso_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('tbsituacaoprocesso_id_seq', 1, false);


--
-- TOC entry 2365 (class 0 OID 72559)
-- Dependencies: 215
-- Data for Name: tbstatuspendencia; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY tbstatuspendencia (stpendencia, dspendencia, tbdivisao_id, id) FROM stdin;
\.


--
-- TOC entry 2432 (class 0 OID 0)
-- Dependencies: 214
-- Name: tbstatuspendencia_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('tbstatuspendencia_id_seq', 1, false);


--
-- TOC entry 2367 (class 0 OID 72577)
-- Dependencies: 217
-- Data for Name: tbsubarea; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY tbsubarea (cdsubarea, nmsubarea, tbdivisao_id, id) FROM stdin;
\.


--
-- TOC entry 2433 (class 0 OID 0)
-- Dependencies: 216
-- Name: tbsubarea_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('tbsubarea_id_seq', 1, false);


--
-- TOC entry 2369 (class 0 OID 72595)
-- Dependencies: 219
-- Data for Name: tbtipocaixa; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY tbtipocaixa (nmtipocaixa, desctipocaixa, tbdivisao_id, id) FROM stdin;
\.


--
-- TOC entry 2434 (class 0 OID 0)
-- Dependencies: 218
-- Name: tbtipocaixa_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('tbtipocaixa_id_seq', 1, false);


--
-- TOC entry 2371 (class 0 OID 72616)
-- Dependencies: 221
-- Data for Name: tbtipopendencia; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY tbtipopendencia (cdtipopend, dspendencia, cdgrupo, tbdivisao_id, tbtipoprocesso_id, id) FROM stdin;
\.


--
-- TOC entry 2435 (class 0 OID 0)
-- Dependencies: 220
-- Name: tbtipopendencia_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('tbtipopendencia_id_seq', 1, false);


--
-- TOC entry 2373 (class 0 OID 72634)
-- Dependencies: 223
-- Data for Name: tbtipoprocesso; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY tbtipoprocesso (nome, tabela, coridentificacao, tbdivisao_id, id) FROM stdin;
\.


--
-- TOC entry 2436 (class 0 OID 0)
-- Dependencies: 222
-- Name: tbtipoprocesso_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('tbtipoprocesso_id_seq', 1, false);


--
-- TOC entry 2375 (class 0 OID 72657)
-- Dependencies: 225
-- Data for Name: tbuf; Type: TABLE DATA; Schema: public; Owner: admin
--

COPY tbuf (sigla, nmuf, id) FROM stdin;
\.


--
-- TOC entry 2437 (class 0 OID 0)
-- Dependencies: 224
-- Name: tbuf_id_seq; Type: SEQUENCE SET; Schema: public; Owner: admin
--

SELECT pg_catalog.setval('tbuf_id_seq', 1, false);


--
-- TOC entry 2136 (class 2606 OID 72145)
-- Name: auth_group_name_key; Type: CONSTRAINT; Schema: public; Owner: admin; Tablespace: 
--

ALTER TABLE ONLY auth_group
    ADD CONSTRAINT auth_group_name_key UNIQUE (name);


--
-- TOC entry 2143 (class 2606 OID 72150)
-- Name: auth_group_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: admin; Tablespace: 
--

ALTER TABLE ONLY auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_pkey PRIMARY KEY (id);


--
-- TOC entry 2139 (class 2606 OID 72143)
-- Name: auth_group_pkey; Type: CONSTRAINT; Schema: public; Owner: admin; Tablespace: 
--

ALTER TABLE ONLY auth_group
    ADD CONSTRAINT auth_group_pkey PRIMARY KEY (id);


--
-- TOC entry 2146 (class 2606 OID 72160)
-- Name: auth_permission_pkey; Type: CONSTRAINT; Schema: public; Owner: admin; Tablespace: 
--

ALTER TABLE ONLY auth_permission
    ADD CONSTRAINT auth_permission_pkey PRIMARY KEY (id);


--
-- TOC entry 2155 (class 2606 OID 72183)
-- Name: auth_user_groups_pkey; Type: CONSTRAINT; Schema: public; Owner: admin; Tablespace: 
--

ALTER TABLE ONLY auth_user_groups
    ADD CONSTRAINT auth_user_groups_pkey PRIMARY KEY (id);


--
-- TOC entry 2148 (class 2606 OID 72173)
-- Name: auth_user_pkey; Type: CONSTRAINT; Schema: public; Owner: admin; Tablespace: 
--

ALTER TABLE ONLY auth_user
    ADD CONSTRAINT auth_user_pkey PRIMARY KEY (id);


--
-- TOC entry 2159 (class 2606 OID 72198)
-- Name: auth_user_user_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: admin; Tablespace: 
--

ALTER TABLE ONLY auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_pkey PRIMARY KEY (id);


--
-- TOC entry 2151 (class 2606 OID 72175)
-- Name: auth_user_username_key; Type: CONSTRAINT; Schema: public; Owner: admin; Tablespace: 
--

ALTER TABLE ONLY auth_user
    ADD CONSTRAINT auth_user_username_key UNIQUE (username);


--
-- TOC entry 2163 (class 2606 OID 72216)
-- Name: django_admin_log_pkey; Type: CONSTRAINT; Schema: public; Owner: admin; Tablespace: 
--

ALTER TABLE ONLY django_admin_log
    ADD CONSTRAINT django_admin_log_pkey PRIMARY KEY (id);


--
-- TOC entry 2166 (class 2606 OID 72226)
-- Name: django_content_type_pkey; Type: CONSTRAINT; Schema: public; Owner: admin; Tablespace: 
--

ALTER TABLE ONLY django_content_type
    ADD CONSTRAINT django_content_type_pkey PRIMARY KEY (id);


--
-- TOC entry 2168 (class 2606 OID 72244)
-- Name: django_session_pkey; Type: CONSTRAINT; Schema: public; Owner: admin; Tablespace: 
--

ALTER TABLE ONLY django_session
    ADD CONSTRAINT django_session_pkey PRIMARY KEY (session_key);


--
-- TOC entry 2171 (class 2606 OID 72249)
-- Name: django_site_pkey; Type: CONSTRAINT; Schema: public; Owner: admin; Tablespace: 
--

ALTER TABLE ONLY django_site
    ADD CONSTRAINT django_site_pkey PRIMARY KEY (id);


--
-- TOC entry 2173 (class 2606 OID 72257)
-- Name: tbcaixa_pkey; Type: CONSTRAINT; Schema: public; Owner: admin; Tablespace: 
--

ALTER TABLE ONLY tbcaixa
    ADD CONSTRAINT tbcaixa_pkey PRIMARY KEY (id);


--
-- TOC entry 2176 (class 2606 OID 72265)
-- Name: tbclassificacaoprocesso_pkey; Type: CONSTRAINT; Schema: public; Owner: admin; Tablespace: 
--

ALTER TABLE ONLY tbclassificacaoprocesso
    ADD CONSTRAINT tbclassificacaoprocesso_pkey PRIMARY KEY (id);


--
-- TOC entry 2179 (class 2606 OID 72273)
-- Name: tbcontrato_pkey; Type: CONSTRAINT; Schema: public; Owner: admin; Tablespace: 
--

ALTER TABLE ONLY tbcontrato
    ADD CONSTRAINT tbcontrato_pkey PRIMARY KEY (id);


--
-- TOC entry 2182 (class 2606 OID 72284)
-- Name: tbdivisao_pkey; Type: CONSTRAINT; Schema: public; Owner: admin; Tablespace: 
--

ALTER TABLE ONLY tbdivisao
    ADD CONSTRAINT tbdivisao_pkey PRIMARY KEY (id);


--
-- TOC entry 2185 (class 2606 OID 72307)
-- Name: tbgleba_pkey; Type: CONSTRAINT; Schema: public; Owner: admin; Tablespace: 
--

ALTER TABLE ONLY tbgleba
    ADD CONSTRAINT tbgleba_pkey PRIMARY KEY (id);


--
-- TOC entry 2189 (class 2606 OID 72315)
-- Name: tbmovimentacao_pkey; Type: CONSTRAINT; Schema: public; Owner: admin; Tablespace: 
--

ALTER TABLE ONLY tbmovimentacao
    ADD CONSTRAINT tbmovimentacao_pkey PRIMARY KEY (id);


--
-- TOC entry 2195 (class 2606 OID 72338)
-- Name: tbmunicipio_pkey; Type: CONSTRAINT; Schema: public; Owner: admin; Tablespace: 
--

ALTER TABLE ONLY tbmunicipio
    ADD CONSTRAINT tbmunicipio_pkey PRIMARY KEY (id);


--
-- TOC entry 2197 (class 2606 OID 72349)
-- Name: tbpecastecnicas_pkey; Type: CONSTRAINT; Schema: public; Owner: admin; Tablespace: 
--

ALTER TABLE ONLY tbpecastecnicas
    ADD CONSTRAINT tbpecastecnicas_pkey PRIMARY KEY (id);


--
-- TOC entry 2204 (class 2606 OID 72380)
-- Name: tbpendencia_pkey; Type: CONSTRAINT; Schema: public; Owner: admin; Tablespace: 
--

ALTER TABLE ONLY tbpendencia
    ADD CONSTRAINT tbpendencia_pkey PRIMARY KEY (id);


--
-- TOC entry 2262 (class 2606 OID 72683)
-- Name: tbpregao_pkey; Type: CONSTRAINT; Schema: public; Owner: admin; Tablespace: 
--

ALTER TABLE ONLY tbpregao
    ADD CONSTRAINT tbpregao_pkey PRIMARY KEY (id);


--
-- TOC entry 2210 (class 2606 OID 72393)
-- Name: tbprocessobase_pkey; Type: CONSTRAINT; Schema: public; Owner: admin; Tablespace: 
--

ALTER TABLE ONLY tbprocessobase
    ADD CONSTRAINT tbprocessobase_pkey PRIMARY KEY (id);


--
-- TOC entry 2219 (class 2606 OID 72444)
-- Name: tbprocessoclausula_pkey; Type: CONSTRAINT; Schema: public; Owner: admin; Tablespace: 
--

ALTER TABLE ONLY tbprocessoclausula
    ADD CONSTRAINT tbprocessoclausula_pkey PRIMARY KEY (id);


--
-- TOC entry 2222 (class 2606 OID 72457)
-- Name: tbprocessorural_pkey; Type: CONSTRAINT; Schema: public; Owner: admin; Tablespace: 
--

ALTER TABLE ONLY tbprocessorural
    ADD CONSTRAINT tbprocessorural_pkey PRIMARY KEY (id);


--
-- TOC entry 2226 (class 2606 OID 72470)
-- Name: tbprocessosanexos_pkey; Type: CONSTRAINT; Schema: public; Owner: admin; Tablespace: 
--

ALTER TABLE ONLY tbprocessosanexos
    ADD CONSTRAINT tbprocessosanexos_pkey PRIMARY KEY (id);


--
-- TOC entry 2230 (class 2606 OID 72493)
-- Name: tbprocessourbano_pkey; Type: CONSTRAINT; Schema: public; Owner: admin; Tablespace: 
--

ALTER TABLE ONLY tbprocessourbano
    ADD CONSTRAINT tbprocessourbano_pkey PRIMARY KEY (id);


--
-- TOC entry 2236 (class 2606 OID 72514)
-- Name: tbservidor_pkey; Type: CONSTRAINT; Schema: public; Owner: admin; Tablespace: 
--

ALTER TABLE ONLY tbservidor
    ADD CONSTRAINT tbservidor_pkey PRIMARY KEY (id);


--
-- TOC entry 2238 (class 2606 OID 72525)
-- Name: tbsituacaogeo_pkey; Type: CONSTRAINT; Schema: public; Owner: admin; Tablespace: 
--

ALTER TABLE ONLY tbsituacaogeo
    ADD CONSTRAINT tbsituacaogeo_pkey PRIMARY KEY (id);


--
-- TOC entry 2241 (class 2606 OID 72546)
-- Name: tbsituacaoprocesso_pkey; Type: CONSTRAINT; Schema: public; Owner: admin; Tablespace: 
--

ALTER TABLE ONLY tbsituacaoprocesso
    ADD CONSTRAINT tbsituacaoprocesso_pkey PRIMARY KEY (id);


--
-- TOC entry 2244 (class 2606 OID 72564)
-- Name: tbstatuspendencia_pkey; Type: CONSTRAINT; Schema: public; Owner: admin; Tablespace: 
--

ALTER TABLE ONLY tbstatuspendencia
    ADD CONSTRAINT tbstatuspendencia_pkey PRIMARY KEY (id);


--
-- TOC entry 2247 (class 2606 OID 72582)
-- Name: tbsubarea_pkey; Type: CONSTRAINT; Schema: public; Owner: admin; Tablespace: 
--

ALTER TABLE ONLY tbsubarea
    ADD CONSTRAINT tbsubarea_pkey PRIMARY KEY (id);


--
-- TOC entry 2250 (class 2606 OID 72603)
-- Name: tbtipocaixa_pkey; Type: CONSTRAINT; Schema: public; Owner: admin; Tablespace: 
--

ALTER TABLE ONLY tbtipocaixa
    ADD CONSTRAINT tbtipocaixa_pkey PRIMARY KEY (id);


--
-- TOC entry 2253 (class 2606 OID 72621)
-- Name: tbtipopendencia_pkey; Type: CONSTRAINT; Schema: public; Owner: admin; Tablespace: 
--

ALTER TABLE ONLY tbtipopendencia
    ADD CONSTRAINT tbtipopendencia_pkey PRIMARY KEY (id);


--
-- TOC entry 2257 (class 2606 OID 72639)
-- Name: tbtipoprocesso_pkey; Type: CONSTRAINT; Schema: public; Owner: admin; Tablespace: 
--

ALTER TABLE ONLY tbtipoprocesso
    ADD CONSTRAINT tbtipoprocesso_pkey PRIMARY KEY (id);


--
-- TOC entry 2260 (class 2606 OID 72662)
-- Name: tbuf_pkey; Type: CONSTRAINT; Schema: public; Owner: admin; Tablespace: 
--

ALTER TABLE ONLY tbuf
    ADD CONSTRAINT tbuf_pkey PRIMARY KEY (id);


--
-- TOC entry 2137 (class 1259 OID 72694)
-- Name: auth_group_name_like; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX auth_group_name_like ON auth_group USING btree (name varchar_pattern_ops);


--
-- TOC entry 2140 (class 1259 OID 72695)
-- Name: auth_group_permissions_group_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX auth_group_permissions_group_id ON auth_group_permissions USING btree (group_id);


--
-- TOC entry 2141 (class 1259 OID 72696)
-- Name: auth_group_permissions_permission_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX auth_group_permissions_permission_id ON auth_group_permissions USING btree (permission_id);


--
-- TOC entry 2144 (class 1259 OID 72697)
-- Name: auth_permission_content_type_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX auth_permission_content_type_id ON auth_permission USING btree (content_type_id);


--
-- TOC entry 2153 (class 1259 OID 72701)
-- Name: auth_user_groups_group_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX auth_user_groups_group_id ON auth_user_groups USING btree (group_id);


--
-- TOC entry 2156 (class 1259 OID 72700)
-- Name: auth_user_groups_user_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX auth_user_groups_user_id ON auth_user_groups USING btree (user_id);


--
-- TOC entry 2149 (class 1259 OID 72699)
-- Name: auth_user_tbdivisao_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX auth_user_tbdivisao_id ON auth_user USING btree (tbdivisao_id);


--
-- TOC entry 2157 (class 1259 OID 72703)
-- Name: auth_user_user_permissions_permission_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX auth_user_user_permissions_permission_id ON auth_user_user_permissions USING btree (permission_id);


--
-- TOC entry 2160 (class 1259 OID 72702)
-- Name: auth_user_user_permissions_user_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX auth_user_user_permissions_user_id ON auth_user_user_permissions USING btree (user_id);


--
-- TOC entry 2152 (class 1259 OID 72698)
-- Name: auth_user_username_like; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX auth_user_username_like ON auth_user USING btree (username varchar_pattern_ops);


--
-- TOC entry 2161 (class 1259 OID 72705)
-- Name: django_admin_log_content_type_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX django_admin_log_content_type_id ON django_admin_log USING btree (content_type_id);


--
-- TOC entry 2164 (class 1259 OID 72704)
-- Name: django_admin_log_user_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX django_admin_log_user_id ON django_admin_log USING btree (user_id);


--
-- TOC entry 2169 (class 1259 OID 72706)
-- Name: django_session_session_key_like; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX django_session_session_key_like ON django_session USING btree (session_key varchar_pattern_ops);


--
-- TOC entry 2174 (class 1259 OID 72707)
-- Name: tbcaixa_tbtipocaixa_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX tbcaixa_tbtipocaixa_id ON tbcaixa USING btree (tbtipocaixa_id);


--
-- TOC entry 2177 (class 1259 OID 72708)
-- Name: tbclassificacaoprocesso_tbdivisao_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX tbclassificacaoprocesso_tbdivisao_id ON tbclassificacaoprocesso USING btree (tbdivisao_id);


--
-- TOC entry 2180 (class 1259 OID 72709)
-- Name: tbcontrato_tbdivisao_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX tbcontrato_tbdivisao_id ON tbcontrato USING btree (tbdivisao_id);


--
-- TOC entry 2183 (class 1259 OID 72710)
-- Name: tbdivisao_tbuf_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX tbdivisao_tbuf_id ON tbdivisao USING btree (tbuf_id);


--
-- TOC entry 2186 (class 1259 OID 72711)
-- Name: tbgleba_tbsubarea_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX tbgleba_tbsubarea_id ON tbgleba USING btree (tbsubarea_id);


--
-- TOC entry 2187 (class 1259 OID 72715)
-- Name: tbmovimentacao_auth_user_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX tbmovimentacao_auth_user_id ON tbmovimentacao USING btree (auth_user_id);


--
-- TOC entry 2190 (class 1259 OID 72714)
-- Name: tbmovimentacao_tbcaixa_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX tbmovimentacao_tbcaixa_id ON tbmovimentacao USING btree (tbcaixa_id);


--
-- TOC entry 2191 (class 1259 OID 72713)
-- Name: tbmovimentacao_tbcaixa_id_origem; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX tbmovimentacao_tbcaixa_id_origem ON tbmovimentacao USING btree (tbcaixa_id_origem);


--
-- TOC entry 2192 (class 1259 OID 72712)
-- Name: tbmovimentacao_tbprocessobase_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX tbmovimentacao_tbprocessobase_id ON tbmovimentacao USING btree (tbprocessobase_id);


--
-- TOC entry 2193 (class 1259 OID 72716)
-- Name: tbmunicipio_Codigo_UF; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX "tbmunicipio_Codigo_UF" ON tbmunicipio USING btree ("Codigo_UF");


--
-- TOC entry 2198 (class 1259 OID 72718)
-- Name: tbpecastecnicas_tbcaixa_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX tbpecastecnicas_tbcaixa_id ON tbpecastecnicas USING btree (tbcaixa_id);


--
-- TOC entry 2199 (class 1259 OID 72717)
-- Name: tbpecastecnicas_tbcontrato_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX tbpecastecnicas_tbcontrato_id ON tbpecastecnicas USING btree (tbcontrato_id);


--
-- TOC entry 2200 (class 1259 OID 72720)
-- Name: tbpecastecnicas_tbdivisao_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX tbpecastecnicas_tbdivisao_id ON tbpecastecnicas USING btree (tbdivisao_id);


--
-- TOC entry 2201 (class 1259 OID 72719)
-- Name: tbpecastecnicas_tbgleba_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX tbpecastecnicas_tbgleba_id ON tbpecastecnicas USING btree (tbgleba_id);


--
-- TOC entry 2202 (class 1259 OID 72723)
-- Name: tbpendencia_auth_user_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX tbpendencia_auth_user_id ON tbpendencia USING btree (auth_user_id);


--
-- TOC entry 2205 (class 1259 OID 72721)
-- Name: tbpendencia_tbprocessobase_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX tbpendencia_tbprocessobase_id ON tbpendencia USING btree (tbprocessobase_id);


--
-- TOC entry 2206 (class 1259 OID 72724)
-- Name: tbpendencia_tbstatuspendencia_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX tbpendencia_tbstatuspendencia_id ON tbpendencia USING btree (tbstatuspendencia_id);


--
-- TOC entry 2207 (class 1259 OID 72722)
-- Name: tbpendencia_tbtipopendencia_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX tbpendencia_tbtipopendencia_id ON tbpendencia USING btree (tbtipopendencia_id);


--
-- TOC entry 2263 (class 1259 OID 72750)
-- Name: tbpregao_tbdivisao_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX tbpregao_tbdivisao_id ON tbpregao USING btree (tbdivisao_id);


--
-- TOC entry 2208 (class 1259 OID 72728)
-- Name: tbprocessobase_auth_user_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX tbprocessobase_auth_user_id ON tbprocessobase USING btree (auth_user_id);


--
-- TOC entry 2211 (class 1259 OID 72726)
-- Name: tbprocessobase_tbcaixa_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX tbprocessobase_tbcaixa_id ON tbprocessobase USING btree (tbcaixa_id);


--
-- TOC entry 2212 (class 1259 OID 72731)
-- Name: tbprocessobase_tbclassificacaoprocesso_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX tbprocessobase_tbclassificacaoprocesso_id ON tbprocessobase USING btree (tbclassificacaoprocesso_id);


--
-- TOC entry 2213 (class 1259 OID 72732)
-- Name: tbprocessobase_tbdivisao_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX tbprocessobase_tbdivisao_id ON tbprocessobase USING btree (tbdivisao_id);


--
-- TOC entry 2214 (class 1259 OID 72725)
-- Name: tbprocessobase_tbgleba_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX tbprocessobase_tbgleba_id ON tbprocessobase USING btree (tbgleba_id);


--
-- TOC entry 2215 (class 1259 OID 72727)
-- Name: tbprocessobase_tbmunicipio_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX tbprocessobase_tbmunicipio_id ON tbprocessobase USING btree (tbmunicipio_id);


--
-- TOC entry 2216 (class 1259 OID 72730)
-- Name: tbprocessobase_tbsituacaoprocesso_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX tbprocessobase_tbsituacaoprocesso_id ON tbprocessobase USING btree (tbsituacaoprocesso_id);


--
-- TOC entry 2217 (class 1259 OID 72729)
-- Name: tbprocessobase_tbtipoprocesso_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX tbprocessobase_tbtipoprocesso_id ON tbprocessobase USING btree (tbtipoprocesso_id);


--
-- TOC entry 2220 (class 1259 OID 72733)
-- Name: tbprocessoclausula_tbprocessobase_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX tbprocessoclausula_tbprocessobase_id ON tbprocessoclausula USING btree (tbprocessobase_id);


--
-- TOC entry 2223 (class 1259 OID 72734)
-- Name: tbprocessorural_tbprocessobase_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX tbprocessorural_tbprocessobase_id ON tbprocessorural USING btree (tbprocessobase_id);


--
-- TOC entry 2224 (class 1259 OID 72737)
-- Name: tbprocessosanexos_auth_user_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX tbprocessosanexos_auth_user_id ON tbprocessosanexos USING btree (auth_user_id);


--
-- TOC entry 2227 (class 1259 OID 72735)
-- Name: tbprocessosanexos_tbprocessobase_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX tbprocessosanexos_tbprocessobase_id ON tbprocessosanexos USING btree (tbprocessobase_id);


--
-- TOC entry 2228 (class 1259 OID 72736)
-- Name: tbprocessosanexos_tbprocessobase_id_anexo; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX tbprocessosanexos_tbprocessobase_id_anexo ON tbprocessosanexos USING btree (tbprocessobase_id_anexo);


--
-- TOC entry 2231 (class 1259 OID 72740)
-- Name: tbprocessourbano_tbcontrato_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX tbprocessourbano_tbcontrato_id ON tbprocessourbano USING btree (tbcontrato_id);


--
-- TOC entry 2232 (class 1259 OID 72739)
-- Name: tbprocessourbano_tbpregao_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX tbprocessourbano_tbpregao_id ON tbprocessourbano USING btree (tbpregao_id);


--
-- TOC entry 2233 (class 1259 OID 72738)
-- Name: tbprocessourbano_tbprocessobase_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX tbprocessourbano_tbprocessobase_id ON tbprocessourbano USING btree (tbprocessobase_id);


--
-- TOC entry 2234 (class 1259 OID 72741)
-- Name: tbprocessourbano_tbsituacaogeo_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX tbprocessourbano_tbsituacaogeo_id ON tbprocessourbano USING btree (tbsituacaogeo_id);


--
-- TOC entry 2239 (class 1259 OID 72742)
-- Name: tbsituacaogeo_tbdivisao_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX tbsituacaogeo_tbdivisao_id ON tbsituacaogeo USING btree (tbdivisao_id);


--
-- TOC entry 2242 (class 1259 OID 72743)
-- Name: tbsituacaoprocesso_tbdivisao_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX tbsituacaoprocesso_tbdivisao_id ON tbsituacaoprocesso USING btree (tbdivisao_id);


--
-- TOC entry 2245 (class 1259 OID 72744)
-- Name: tbstatuspendencia_tbdivisao_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX tbstatuspendencia_tbdivisao_id ON tbstatuspendencia USING btree (tbdivisao_id);


--
-- TOC entry 2248 (class 1259 OID 72745)
-- Name: tbsubarea_tbdivisao_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX tbsubarea_tbdivisao_id ON tbsubarea USING btree (tbdivisao_id);


--
-- TOC entry 2251 (class 1259 OID 72746)
-- Name: tbtipocaixa_tbdivisao_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX tbtipocaixa_tbdivisao_id ON tbtipocaixa USING btree (tbdivisao_id);


--
-- TOC entry 2254 (class 1259 OID 72747)
-- Name: tbtipopendencia_tbdivisao_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX tbtipopendencia_tbdivisao_id ON tbtipopendencia USING btree (tbdivisao_id);


--
-- TOC entry 2255 (class 1259 OID 72748)
-- Name: tbtipopendencia_tbtipoprocesso_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX tbtipopendencia_tbtipoprocesso_id ON tbtipopendencia USING btree (tbtipoprocesso_id);


--
-- TOC entry 2258 (class 1259 OID 72749)
-- Name: tbtipoprocesso_tbdivisao_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX tbtipoprocesso_tbdivisao_id ON tbtipoprocesso USING btree (tbdivisao_id);


--
-- TOC entry 2283 (class 2606 OID 72668)
-- Name: Codigo_UF_refs_id_29984a75; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbmunicipio
    ADD CONSTRAINT "Codigo_UF_refs_id_29984a75" FOREIGN KEY ("Codigo_UF") REFERENCES tbuf(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2264 (class 2606 OID 72151)
-- Name: auth_group_permissions_group_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_fkey FOREIGN KEY (group_id) REFERENCES auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2269 (class 2606 OID 72189)
-- Name: auth_user_groups_group_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY auth_user_groups
    ADD CONSTRAINT auth_user_groups_group_id_fkey FOREIGN KEY (group_id) REFERENCES auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2268 (class 2606 OID 72184)
-- Name: auth_user_groups_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY auth_user_groups
    ADD CONSTRAINT auth_user_groups_user_id_fkey FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2271 (class 2606 OID 72204)
-- Name: auth_user_user_permissions_permission_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_permission_id_fkey FOREIGN KEY (permission_id) REFERENCES auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2270 (class 2606 OID 72199)
-- Name: auth_user_user_permissions_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_user_id_fkey FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2273 (class 2606 OID 72232)
-- Name: content_type_id_refs_id_93d2d1f8; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY django_admin_log
    ADD CONSTRAINT content_type_id_refs_id_93d2d1f8 FOREIGN KEY (content_type_id) REFERENCES django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2266 (class 2606 OID 72227)
-- Name: content_type_id_refs_id_d043b34a; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY auth_permission
    ADD CONSTRAINT content_type_id_refs_id_d043b34a FOREIGN KEY (content_type_id) REFERENCES django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2272 (class 2606 OID 72217)
-- Name: django_admin_log_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY django_admin_log
    ADD CONSTRAINT django_admin_log_user_id_fkey FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2265 (class 2606 OID 72161)
-- Name: permission_id_refs_id_6ba0f519; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY auth_group_permissions
    ADD CONSTRAINT permission_id_refs_id_6ba0f519 FOREIGN KEY (permission_id) REFERENCES auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2275 (class 2606 OID 72290)
-- Name: tbdivisao_id_refs_id_00d25a11; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbclassificacaoprocesso
    ADD CONSTRAINT tbdivisao_id_refs_id_00d25a11 FOREIGN KEY (tbdivisao_id) REFERENCES tbdivisao(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2267 (class 2606 OID 72285)
-- Name: tbdivisao_id_refs_id_209f7cf0; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY auth_user
    ADD CONSTRAINT tbdivisao_id_refs_id_209f7cf0 FOREIGN KEY (tbdivisao_id) REFERENCES tbdivisao(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2276 (class 2606 OID 72295)
-- Name: tbdivisao_id_refs_id_c808e225; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbcontrato
    ADD CONSTRAINT tbdivisao_id_refs_id_c808e225 FOREIGN KEY (tbdivisao_id) REFERENCES tbdivisao(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2281 (class 2606 OID 72326)
-- Name: tbmovimentacao_auth_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbmovimentacao
    ADD CONSTRAINT tbmovimentacao_auth_user_id_fkey FOREIGN KEY (auth_user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2280 (class 2606 OID 72321)
-- Name: tbmovimentacao_tbcaixa_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbmovimentacao
    ADD CONSTRAINT tbmovimentacao_tbcaixa_id_fkey FOREIGN KEY (tbcaixa_id) REFERENCES tbcaixa(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2279 (class 2606 OID 72316)
-- Name: tbmovimentacao_tbcaixa_id_origem_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbmovimentacao
    ADD CONSTRAINT tbmovimentacao_tbcaixa_id_origem_fkey FOREIGN KEY (tbcaixa_id_origem) REFERENCES tbcaixa(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2285 (class 2606 OID 72355)
-- Name: tbpecastecnicas_tbcaixa_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbpecastecnicas
    ADD CONSTRAINT tbpecastecnicas_tbcaixa_id_fkey FOREIGN KEY (tbcaixa_id) REFERENCES tbcaixa(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2284 (class 2606 OID 72350)
-- Name: tbpecastecnicas_tbcontrato_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbpecastecnicas
    ADD CONSTRAINT tbpecastecnicas_tbcontrato_id_fkey FOREIGN KEY (tbcontrato_id) REFERENCES tbcontrato(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2287 (class 2606 OID 72365)
-- Name: tbpecastecnicas_tbdivisao_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbpecastecnicas
    ADD CONSTRAINT tbpecastecnicas_tbdivisao_id_fkey FOREIGN KEY (tbdivisao_id) REFERENCES tbdivisao(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2286 (class 2606 OID 72360)
-- Name: tbpecastecnicas_tbgleba_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbpecastecnicas
    ADD CONSTRAINT tbpecastecnicas_tbgleba_id_fkey FOREIGN KEY (tbgleba_id) REFERENCES tbgleba(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2288 (class 2606 OID 72381)
-- Name: tbpendencia_auth_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbpendencia
    ADD CONSTRAINT tbpendencia_auth_user_id_fkey FOREIGN KEY (auth_user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2308 (class 2606 OID 72689)
-- Name: tbpregao_id_refs_id_f323926f; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbprocessourbano
    ADD CONSTRAINT tbpregao_id_refs_id_f323926f FOREIGN KEY (tbpregao_id) REFERENCES tbpregao(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2317 (class 2606 OID 72684)
-- Name: tbpregao_tbdivisao_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbpregao
    ADD CONSTRAINT tbpregao_tbdivisao_id_fkey FOREIGN KEY (tbdivisao_id) REFERENCES tbdivisao(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2295 (class 2606 OID 72409)
-- Name: tbprocessobase_auth_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbprocessobase
    ADD CONSTRAINT tbprocessobase_auth_user_id_fkey FOREIGN KEY (auth_user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2282 (class 2606 OID 72424)
-- Name: tbprocessobase_id_refs_id_5aebc46a; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbmovimentacao
    ADD CONSTRAINT tbprocessobase_id_refs_id_5aebc46a FOREIGN KEY (tbprocessobase_id) REFERENCES tbprocessobase(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2289 (class 2606 OID 72429)
-- Name: tbprocessobase_id_refs_id_86d3804c; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbpendencia
    ADD CONSTRAINT tbprocessobase_id_refs_id_86d3804c FOREIGN KEY (tbprocessobase_id) REFERENCES tbprocessobase(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2293 (class 2606 OID 72399)
-- Name: tbprocessobase_tbcaixa_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbprocessobase
    ADD CONSTRAINT tbprocessobase_tbcaixa_id_fkey FOREIGN KEY (tbcaixa_id) REFERENCES tbcaixa(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2296 (class 2606 OID 72414)
-- Name: tbprocessobase_tbclassificacaoprocesso_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbprocessobase
    ADD CONSTRAINT tbprocessobase_tbclassificacaoprocesso_id_fkey FOREIGN KEY (tbclassificacaoprocesso_id) REFERENCES tbclassificacaoprocesso(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2297 (class 2606 OID 72419)
-- Name: tbprocessobase_tbdivisao_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbprocessobase
    ADD CONSTRAINT tbprocessobase_tbdivisao_id_fkey FOREIGN KEY (tbdivisao_id) REFERENCES tbdivisao(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2292 (class 2606 OID 72394)
-- Name: tbprocessobase_tbgleba_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbprocessobase
    ADD CONSTRAINT tbprocessobase_tbgleba_id_fkey FOREIGN KEY (tbgleba_id) REFERENCES tbgleba(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2294 (class 2606 OID 72404)
-- Name: tbprocessobase_tbmunicipio_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbprocessobase
    ADD CONSTRAINT tbprocessobase_tbmunicipio_id_fkey FOREIGN KEY (tbmunicipio_id) REFERENCES tbmunicipio(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2300 (class 2606 OID 72445)
-- Name: tbprocessoclausula_tbprocessobase_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbprocessoclausula
    ADD CONSTRAINT tbprocessoclausula_tbprocessobase_id_fkey FOREIGN KEY (tbprocessobase_id) REFERENCES tbprocessobase(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2301 (class 2606 OID 72458)
-- Name: tbprocessorural_tbprocessobase_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbprocessorural
    ADD CONSTRAINT tbprocessorural_tbprocessobase_id_fkey FOREIGN KEY (tbprocessobase_id) REFERENCES tbprocessobase(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2304 (class 2606 OID 72481)
-- Name: tbprocessosanexos_auth_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbprocessosanexos
    ADD CONSTRAINT tbprocessosanexos_auth_user_id_fkey FOREIGN KEY (auth_user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2303 (class 2606 OID 72476)
-- Name: tbprocessosanexos_tbprocessobase_id_anexo_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbprocessosanexos
    ADD CONSTRAINT tbprocessosanexos_tbprocessobase_id_anexo_fkey FOREIGN KEY (tbprocessobase_id_anexo) REFERENCES tbprocessobase(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2302 (class 2606 OID 72471)
-- Name: tbprocessosanexos_tbprocessobase_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbprocessosanexos
    ADD CONSTRAINT tbprocessosanexos_tbprocessobase_id_fkey FOREIGN KEY (tbprocessobase_id) REFERENCES tbprocessobase(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2306 (class 2606 OID 72499)
-- Name: tbprocessourbano_tbcontrato_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbprocessourbano
    ADD CONSTRAINT tbprocessourbano_tbcontrato_id_fkey FOREIGN KEY (tbcontrato_id) REFERENCES tbcontrato(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2305 (class 2606 OID 72494)
-- Name: tbprocessourbano_tbprocessobase_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbprocessourbano
    ADD CONSTRAINT tbprocessourbano_tbprocessobase_id_fkey FOREIGN KEY (tbprocessobase_id) REFERENCES tbprocessobase(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2307 (class 2606 OID 72531)
-- Name: tbsituacaogeo_id_refs_id_f9087efb; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbprocessourbano
    ADD CONSTRAINT tbsituacaogeo_id_refs_id_f9087efb FOREIGN KEY (tbsituacaogeo_id) REFERENCES tbsituacaogeo(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2309 (class 2606 OID 72526)
-- Name: tbsituacaogeo_tbdivisao_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbsituacaogeo
    ADD CONSTRAINT tbsituacaogeo_tbdivisao_id_fkey FOREIGN KEY (tbdivisao_id) REFERENCES tbdivisao(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2298 (class 2606 OID 72552)
-- Name: tbsituacaoprocesso_id_refs_id_bfef2fda; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbprocessobase
    ADD CONSTRAINT tbsituacaoprocesso_id_refs_id_bfef2fda FOREIGN KEY (tbsituacaoprocesso_id) REFERENCES tbsituacaoprocesso(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2310 (class 2606 OID 72547)
-- Name: tbsituacaoprocesso_tbdivisao_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbsituacaoprocesso
    ADD CONSTRAINT tbsituacaoprocesso_tbdivisao_id_fkey FOREIGN KEY (tbdivisao_id) REFERENCES tbdivisao(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2290 (class 2606 OID 72570)
-- Name: tbstatuspendencia_id_refs_id_615418ce; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbpendencia
    ADD CONSTRAINT tbstatuspendencia_id_refs_id_615418ce FOREIGN KEY (tbstatuspendencia_id) REFERENCES tbstatuspendencia(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2311 (class 2606 OID 72565)
-- Name: tbstatuspendencia_tbdivisao_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbstatuspendencia
    ADD CONSTRAINT tbstatuspendencia_tbdivisao_id_fkey FOREIGN KEY (tbdivisao_id) REFERENCES tbdivisao(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2278 (class 2606 OID 72588)
-- Name: tbsubarea_id_refs_id_c3c14a3b; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbgleba
    ADD CONSTRAINT tbsubarea_id_refs_id_c3c14a3b FOREIGN KEY (tbsubarea_id) REFERENCES tbsubarea(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2312 (class 2606 OID 72583)
-- Name: tbsubarea_tbdivisao_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbsubarea
    ADD CONSTRAINT tbsubarea_tbdivisao_id_fkey FOREIGN KEY (tbdivisao_id) REFERENCES tbdivisao(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2274 (class 2606 OID 72609)
-- Name: tbtipocaixa_id_refs_id_1f3d944c; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbcaixa
    ADD CONSTRAINT tbtipocaixa_id_refs_id_1f3d944c FOREIGN KEY (tbtipocaixa_id) REFERENCES tbtipocaixa(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2313 (class 2606 OID 72604)
-- Name: tbtipocaixa_tbdivisao_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbtipocaixa
    ADD CONSTRAINT tbtipocaixa_tbdivisao_id_fkey FOREIGN KEY (tbdivisao_id) REFERENCES tbdivisao(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2291 (class 2606 OID 72627)
-- Name: tbtipopendencia_id_refs_id_4f9053c1; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbpendencia
    ADD CONSTRAINT tbtipopendencia_id_refs_id_4f9053c1 FOREIGN KEY (tbtipopendencia_id) REFERENCES tbtipopendencia(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2314 (class 2606 OID 72622)
-- Name: tbtipopendencia_tbdivisao_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbtipopendencia
    ADD CONSTRAINT tbtipopendencia_tbdivisao_id_fkey FOREIGN KEY (tbdivisao_id) REFERENCES tbdivisao(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2315 (class 2606 OID 72650)
-- Name: tbtipoprocesso_id_refs_id_14dae0cf; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbtipopendencia
    ADD CONSTRAINT tbtipoprocesso_id_refs_id_14dae0cf FOREIGN KEY (tbtipoprocesso_id) REFERENCES tbtipoprocesso(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2299 (class 2606 OID 72645)
-- Name: tbtipoprocesso_id_refs_id_64d671a3; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbprocessobase
    ADD CONSTRAINT tbtipoprocesso_id_refs_id_64d671a3 FOREIGN KEY (tbtipoprocesso_id) REFERENCES tbtipoprocesso(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2316 (class 2606 OID 72640)
-- Name: tbtipoprocesso_tbdivisao_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbtipoprocesso
    ADD CONSTRAINT tbtipoprocesso_tbdivisao_id_fkey FOREIGN KEY (tbdivisao_id) REFERENCES tbdivisao(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2277 (class 2606 OID 72663)
-- Name: tbuf_id_refs_id_c8d633fb; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbdivisao
    ADD CONSTRAINT tbuf_id_refs_id_c8d633fb FOREIGN KEY (tbuf_id) REFERENCES tbuf(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2384 (class 0 OID 0)
-- Dependencies: 5
-- Name: public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM postgres;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO PUBLIC;


-- Completed on 2013-11-07 12:14:46

--
-- PostgreSQL database dump complete
--

