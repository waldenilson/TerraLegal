--
-- PostgreSQL database dump
--

-- Dumped from database version 9.1.6
-- Dumped by pg_dump version 9.1.6
-- Started on 2014-01-14 23:22:20 BRT

SET statement_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

--
-- TOC entry 231 (class 3079 OID 11684)
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- TOC entry 2357 (class 0 OID 0)
-- Dependencies: 231
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- TOC entry 161 (class 1259 OID 5867847)
-- Dependencies: 6
-- Name: auth_group; Type: TABLE; Schema: public; Owner: admin; Tablespace: 
--

CREATE TABLE auth_group (
    id integer NOT NULL,
    name character varying(80) NOT NULL,
    tbdivisao_id integer NOT NULL
);


ALTER TABLE public.auth_group OWNER TO admin;

--
-- TOC entry 162 (class 1259 OID 5867850)
-- Dependencies: 6 161
-- Name: auth_group_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE auth_group_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_group_id_seq OWNER TO admin;

--
-- TOC entry 2358 (class 0 OID 0)
-- Dependencies: 162
-- Name: auth_group_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE auth_group_id_seq OWNED BY auth_group.id;


--
-- TOC entry 163 (class 1259 OID 5867852)
-- Dependencies: 6
-- Name: auth_group_permissions; Type: TABLE; Schema: public; Owner: admin; Tablespace: 
--

CREATE TABLE auth_group_permissions (
    id integer NOT NULL,
    group_id integer NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE public.auth_group_permissions OWNER TO admin;

--
-- TOC entry 164 (class 1259 OID 5867855)
-- Dependencies: 163 6
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE auth_group_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_group_permissions_id_seq OWNER TO admin;

--
-- TOC entry 2359 (class 0 OID 0)
-- Dependencies: 164
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE auth_group_permissions_id_seq OWNED BY auth_group_permissions.id;


--
-- TOC entry 165 (class 1259 OID 5867857)
-- Dependencies: 6
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
-- TOC entry 166 (class 1259 OID 5867860)
-- Dependencies: 165 6
-- Name: auth_permission_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE auth_permission_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_permission_id_seq OWNER TO admin;

--
-- TOC entry 2360 (class 0 OID 0)
-- Dependencies: 166
-- Name: auth_permission_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE auth_permission_id_seq OWNED BY auth_permission.id;


--
-- TOC entry 167 (class 1259 OID 5867862)
-- Dependencies: 6
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
-- TOC entry 168 (class 1259 OID 5867865)
-- Dependencies: 6
-- Name: auth_user_groups; Type: TABLE; Schema: public; Owner: admin; Tablespace: 
--

CREATE TABLE auth_user_groups (
    id integer NOT NULL,
    user_id integer NOT NULL,
    group_id integer NOT NULL
);


ALTER TABLE public.auth_user_groups OWNER TO admin;

--
-- TOC entry 169 (class 1259 OID 5867868)
-- Dependencies: 6 168
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
-- TOC entry 2361 (class 0 OID 0)
-- Dependencies: 169
-- Name: auth_user_groups_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE auth_user_groups_id_seq OWNED BY auth_user_groups.id;


--
-- TOC entry 170 (class 1259 OID 5867870)
-- Dependencies: 167 6
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
-- TOC entry 2362 (class 0 OID 0)
-- Dependencies: 170
-- Name: auth_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE auth_user_id_seq OWNED BY auth_user.id;


--
-- TOC entry 171 (class 1259 OID 5867872)
-- Dependencies: 6
-- Name: auth_user_user_permissions; Type: TABLE; Schema: public; Owner: admin; Tablespace: 
--

CREATE TABLE auth_user_user_permissions (
    id integer NOT NULL,
    user_id integer NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE public.auth_user_user_permissions OWNER TO admin;

--
-- TOC entry 172 (class 1259 OID 5867875)
-- Dependencies: 6 171
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE auth_user_user_permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.auth_user_user_permissions_id_seq OWNER TO admin;

--
-- TOC entry 2363 (class 0 OID 0)
-- Dependencies: 172
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE auth_user_user_permissions_id_seq OWNED BY auth_user_user_permissions.id;


--
-- TOC entry 173 (class 1259 OID 5867877)
-- Dependencies: 6
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
-- TOC entry 174 (class 1259 OID 5867883)
-- Dependencies: 6
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
-- TOC entry 175 (class 1259 OID 5867886)
-- Dependencies: 6
-- Name: django_session; Type: TABLE; Schema: public; Owner: admin; Tablespace: 
--

CREATE TABLE django_session (
    session_key character varying(40) NOT NULL,
    session_data text NOT NULL,
    expire_date timestamp with time zone NOT NULL
);


ALTER TABLE public.django_session OWNER TO admin;

--
-- TOC entry 176 (class 1259 OID 5867892)
-- Dependencies: 6
-- Name: django_site; Type: TABLE; Schema: public; Owner: admin; Tablespace: 
--

CREATE TABLE django_site (
    id integer NOT NULL,
    domain character varying(100) NOT NULL,
    name character varying(50) NOT NULL
);


ALTER TABLE public.django_site OWNER TO admin;

--
-- TOC entry 177 (class 1259 OID 5867895)
-- Dependencies: 6
-- Name: tbcaixa; Type: TABLE; Schema: public; Owner: admin; Tablespace: 
--

CREATE TABLE tbcaixa (
    nmlocalarquivo character varying(80) NOT NULL,
    tbtipocaixa_id integer NOT NULL,
    id integer NOT NULL
);


ALTER TABLE public.tbcaixa OWNER TO admin;

--
-- TOC entry 178 (class 1259 OID 5867898)
-- Dependencies: 6 177
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
-- TOC entry 2364 (class 0 OID 0)
-- Dependencies: 178
-- Name: tbcaixa_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE tbcaixa_id_seq OWNED BY tbcaixa.id;


--
-- TOC entry 179 (class 1259 OID 5867900)
-- Dependencies: 6
-- Name: tbclassificacaoprocesso; Type: TABLE; Schema: public; Owner: admin; Tablespace: 
--

CREATE TABLE tbclassificacaoprocesso (
    nmclassificacao character varying(80) NOT NULL,
    tbdivisao_id integer,
    id integer NOT NULL
);


ALTER TABLE public.tbclassificacaoprocesso OWNER TO admin;

--
-- TOC entry 180 (class 1259 OID 5867903)
-- Dependencies: 179 6
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
-- TOC entry 2365 (class 0 OID 0)
-- Dependencies: 180
-- Name: tbclassificacaoprocesso_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE tbclassificacaoprocesso_id_seq OWNED BY tbclassificacaoprocesso.id;


--
-- TOC entry 181 (class 1259 OID 5867905)
-- Dependencies: 6
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
-- TOC entry 182 (class 1259 OID 5867908)
-- Dependencies: 181 6
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
-- TOC entry 2366 (class 0 OID 0)
-- Dependencies: 182
-- Name: tbcontrato_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE tbcontrato_id_seq OWNED BY tbcontrato.id;


--
-- TOC entry 183 (class 1259 OID 5867910)
-- Dependencies: 6
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
-- TOC entry 184 (class 1259 OID 5867916)
-- Dependencies: 183 6
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
-- TOC entry 2367 (class 0 OID 0)
-- Dependencies: 184
-- Name: tbdivisao_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE tbdivisao_id_seq OWNED BY tbdivisao.id;


--
-- TOC entry 185 (class 1259 OID 5867918)
-- Dependencies: 6
-- Name: tbdocumentobase; Type: TABLE; Schema: public; Owner: admin; Tablespace: 
--

CREATE TABLE tbdocumentobase (
    nmdocumento character varying(80) NOT NULL,
    tbtipodocumento_id integer NOT NULL,
    dtdocumento timestamp with time zone,
    linkdocumento text NOT NULL,
    auth_user_id integer NOT NULL,
    tbdivisao_id integer NOT NULL,
    id integer NOT NULL
);


ALTER TABLE public.tbdocumentobase OWNER TO admin;

--
-- TOC entry 186 (class 1259 OID 5867924)
-- Dependencies: 185 6
-- Name: tbdocumentobase_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE tbdocumentobase_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.tbdocumentobase_id_seq OWNER TO admin;

--
-- TOC entry 2368 (class 0 OID 0)
-- Dependencies: 186
-- Name: tbdocumentobase_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE tbdocumentobase_id_seq OWNED BY tbdocumentobase.id;


--
-- TOC entry 187 (class 1259 OID 5867926)
-- Dependencies: 6
-- Name: tbdocumentomemorando; Type: TABLE; Schema: public; Owner: admin; Tablespace: 
--

CREATE TABLE tbdocumentomemorando (
    tbdocumentobase_id integer NOT NULL,
    nmassunto character varying(100) NOT NULL,
    nmlocal character varying(100) NOT NULL,
    nmremetente character varying(100) NOT NULL,
    nmdestinatario character varying(100) NOT NULL,
    nmmensagem text NOT NULL,
    id integer NOT NULL
);


ALTER TABLE public.tbdocumentomemorando OWNER TO admin;

--
-- TOC entry 188 (class 1259 OID 5867932)
-- Dependencies: 187 6
-- Name: tbdocumentomemorando_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE tbdocumentomemorando_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.tbdocumentomemorando_id_seq OWNER TO admin;

--
-- TOC entry 2369 (class 0 OID 0)
-- Dependencies: 188
-- Name: tbdocumentomemorando_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE tbdocumentomemorando_id_seq OWNED BY tbdocumentomemorando.id;


--
-- TOC entry 189 (class 1259 OID 5867934)
-- Dependencies: 6
-- Name: tbgleba; Type: TABLE; Schema: public; Owner: admin; Tablespace: 
--

CREATE TABLE tbgleba (
    cdgleba integer,
    nmgleba character varying(80) NOT NULL,
    tbsubarea_id integer NOT NULL,
    tbuf_id integer,
    id integer NOT NULL
);


ALTER TABLE public.tbgleba OWNER TO admin;

--
-- TOC entry 190 (class 1259 OID 5867937)
-- Dependencies: 189 6
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
-- TOC entry 2370 (class 0 OID 0)
-- Dependencies: 190
-- Name: tbgleba_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE tbgleba_id_seq OWNED BY tbgleba.id;


--
-- TOC entry 191 (class 1259 OID 5867939)
-- Dependencies: 6
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
-- TOC entry 192 (class 1259 OID 5867942)
-- Dependencies: 191 6
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
-- TOC entry 2371 (class 0 OID 0)
-- Dependencies: 192
-- Name: tbmovimentacao_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE tbmovimentacao_id_seq OWNED BY tbmovimentacao.id;


--
-- TOC entry 193 (class 1259 OID 5867944)
-- Dependencies: 6
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
-- TOC entry 194 (class 1259 OID 5867947)
-- Dependencies: 193 6
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
-- TOC entry 2372 (class 0 OID 0)
-- Dependencies: 194
-- Name: tbmunicipio_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE tbmunicipio_id_seq OWNED BY tbmunicipio.id;


--
-- TOC entry 195 (class 1259 OID 5867949)
-- Dependencies: 6
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
-- TOC entry 196 (class 1259 OID 5867955)
-- Dependencies: 195 6
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
-- TOC entry 2373 (class 0 OID 0)
-- Dependencies: 196
-- Name: tbpecastecnicas_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE tbpecastecnicas_id_seq OWNED BY tbpecastecnicas.id;


--
-- TOC entry 197 (class 1259 OID 5867957)
-- Dependencies: 6
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
-- TOC entry 198 (class 1259 OID 5867963)
-- Dependencies: 6 197
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
-- TOC entry 2374 (class 0 OID 0)
-- Dependencies: 198
-- Name: tbpendencia_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE tbpendencia_id_seq OWNED BY tbpendencia.id;


--
-- TOC entry 199 (class 1259 OID 5867965)
-- Dependencies: 6
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
-- TOC entry 200 (class 1259 OID 5867971)
-- Dependencies: 199 6
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
-- TOC entry 2375 (class 0 OID 0)
-- Dependencies: 200
-- Name: tbpregao_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE tbpregao_id_seq OWNED BY tbpregao.id;


--
-- TOC entry 201 (class 1259 OID 5867973)
-- Dependencies: 6
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
-- TOC entry 202 (class 1259 OID 5867976)
-- Dependencies: 6 201
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
-- TOC entry 2376 (class 0 OID 0)
-- Dependencies: 202
-- Name: tbprocessobase_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE tbprocessobase_id_seq OWNED BY tbprocessobase.id;


--
-- TOC entry 203 (class 1259 OID 5867978)
-- Dependencies: 6
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
-- TOC entry 204 (class 1259 OID 5867984)
-- Dependencies: 203 6
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
-- TOC entry 2377 (class 0 OID 0)
-- Dependencies: 204
-- Name: tbprocessoclausula_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE tbprocessoclausula_id_seq OWNED BY tbprocessoclausula.id;


--
-- TOC entry 205 (class 1259 OID 5867986)
-- Dependencies: 6
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
-- TOC entry 206 (class 1259 OID 5867989)
-- Dependencies: 205 6
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
-- TOC entry 2378 (class 0 OID 0)
-- Dependencies: 206
-- Name: tbprocessorural_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE tbprocessorural_id_seq OWNED BY tbprocessorural.id;


--
-- TOC entry 207 (class 1259 OID 5867991)
-- Dependencies: 6
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
-- TOC entry 208 (class 1259 OID 5867994)
-- Dependencies: 207 6
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
-- TOC entry 2379 (class 0 OID 0)
-- Dependencies: 208
-- Name: tbprocessosanexos_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE tbprocessosanexos_id_seq OWNED BY tbprocessosanexos.id;


--
-- TOC entry 209 (class 1259 OID 5867996)
-- Dependencies: 6
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
-- TOC entry 210 (class 1259 OID 5867999)
-- Dependencies: 209 6
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
-- TOC entry 2380 (class 0 OID 0)
-- Dependencies: 210
-- Name: tbprocessourbano_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE tbprocessourbano_id_seq OWNED BY tbprocessourbano.id;


--
-- TOC entry 211 (class 1259 OID 5868001)
-- Dependencies: 6
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
    tbdivisao_id integer NOT NULL,
    id integer NOT NULL
);


ALTER TABLE public.tbservidor OWNER TO admin;

--
-- TOC entry 212 (class 1259 OID 5868007)
-- Dependencies: 6 211
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
-- TOC entry 2381 (class 0 OID 0)
-- Dependencies: 212
-- Name: tbservidor_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE tbservidor_id_seq OWNED BY tbservidor.id;


--
-- TOC entry 213 (class 1259 OID 5868009)
-- Dependencies: 6
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
-- TOC entry 214 (class 1259 OID 5868015)
-- Dependencies: 213 6
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
-- TOC entry 2382 (class 0 OID 0)
-- Dependencies: 214
-- Name: tbsituacaogeo_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE tbsituacaogeo_id_seq OWNED BY tbsituacaogeo.id;


--
-- TOC entry 215 (class 1259 OID 5868017)
-- Dependencies: 6
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
-- TOC entry 216 (class 1259 OID 5868023)
-- Dependencies: 215 6
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
-- TOC entry 2383 (class 0 OID 0)
-- Dependencies: 216
-- Name: tbsituacaoprocesso_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE tbsituacaoprocesso_id_seq OWNED BY tbsituacaoprocesso.id;


--
-- TOC entry 217 (class 1259 OID 5868025)
-- Dependencies: 6
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
-- TOC entry 218 (class 1259 OID 5868028)
-- Dependencies: 217 6
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
-- TOC entry 2384 (class 0 OID 0)
-- Dependencies: 218
-- Name: tbstatuspendencia_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE tbstatuspendencia_id_seq OWNED BY tbstatuspendencia.id;


--
-- TOC entry 219 (class 1259 OID 5868030)
-- Dependencies: 6
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
-- TOC entry 220 (class 1259 OID 5868033)
-- Dependencies: 219 6
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
-- TOC entry 2385 (class 0 OID 0)
-- Dependencies: 220
-- Name: tbsubarea_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE tbsubarea_id_seq OWNED BY tbsubarea.id;


--
-- TOC entry 221 (class 1259 OID 5868035)
-- Dependencies: 6
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
-- TOC entry 222 (class 1259 OID 5868041)
-- Dependencies: 221 6
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
-- TOC entry 2386 (class 0 OID 0)
-- Dependencies: 222
-- Name: tbtipocaixa_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE tbtipocaixa_id_seq OWNED BY tbtipocaixa.id;


--
-- TOC entry 223 (class 1259 OID 5868043)
-- Dependencies: 6
-- Name: tbtipodocumento; Type: TABLE; Schema: public; Owner: admin; Tablespace: 
--

CREATE TABLE tbtipodocumento (
    nmtipodocumento character varying(80) NOT NULL,
    desctipodocumento text NOT NULL,
    tabela character varying(50) NOT NULL,
    coridentificacao character varying(20) NOT NULL,
    tbdivisao_id integer,
    id integer NOT NULL
);


ALTER TABLE public.tbtipodocumento OWNER TO admin;

--
-- TOC entry 224 (class 1259 OID 5868049)
-- Dependencies: 6 223
-- Name: tbtipodocumento_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE tbtipodocumento_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.tbtipodocumento_id_seq OWNER TO admin;

--
-- TOC entry 2387 (class 0 OID 0)
-- Dependencies: 224
-- Name: tbtipodocumento_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE tbtipodocumento_id_seq OWNED BY tbtipodocumento.id;


--
-- TOC entry 225 (class 1259 OID 5868051)
-- Dependencies: 6
-- Name: tbtipopendencia; Type: TABLE; Schema: public; Owner: admin; Tablespace: 
--

CREATE TABLE tbtipopendencia (
    dspendencia character varying(50) NOT NULL,
    tbtipoprocesso_id integer NOT NULL,
    tbdivisao_id integer,
    id integer NOT NULL
);


ALTER TABLE public.tbtipopendencia OWNER TO admin;

--
-- TOC entry 226 (class 1259 OID 5868054)
-- Dependencies: 225 6
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
-- TOC entry 2388 (class 0 OID 0)
-- Dependencies: 226
-- Name: tbtipopendencia_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE tbtipopendencia_id_seq OWNED BY tbtipopendencia.id;


--
-- TOC entry 227 (class 1259 OID 5868056)
-- Dependencies: 6
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
-- TOC entry 228 (class 1259 OID 5868059)
-- Dependencies: 6 227
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
-- TOC entry 2389 (class 0 OID 0)
-- Dependencies: 228
-- Name: tbtipoprocesso_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE tbtipoprocesso_id_seq OWNED BY tbtipoprocesso.id;


--
-- TOC entry 229 (class 1259 OID 5868061)
-- Dependencies: 6
-- Name: tbuf; Type: TABLE; Schema: public; Owner: admin; Tablespace: 
--

CREATE TABLE tbuf (
    sigla character varying(2) NOT NULL,
    nmuf character varying(50) NOT NULL,
    id integer NOT NULL
);


ALTER TABLE public.tbuf OWNER TO admin;

--
-- TOC entry 230 (class 1259 OID 5868064)
-- Dependencies: 229 6
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
-- TOC entry 2390 (class 0 OID 0)
-- Dependencies: 230
-- Name: tbuf_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE tbuf_id_seq OWNED BY tbuf.id;


--
-- TOC entry 2114 (class 2604 OID 5868066)
-- Dependencies: 162 161
-- Name: id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY auth_group ALTER COLUMN id SET DEFAULT nextval('auth_group_id_seq'::regclass);


--
-- TOC entry 2115 (class 2604 OID 5868067)
-- Dependencies: 164 163
-- Name: id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY auth_group_permissions ALTER COLUMN id SET DEFAULT nextval('auth_group_permissions_id_seq'::regclass);


--
-- TOC entry 2116 (class 2604 OID 5868068)
-- Dependencies: 166 165
-- Name: id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY auth_permission ALTER COLUMN id SET DEFAULT nextval('auth_permission_id_seq'::regclass);


--
-- TOC entry 2117 (class 2604 OID 5868069)
-- Dependencies: 170 167
-- Name: id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY auth_user ALTER COLUMN id SET DEFAULT nextval('auth_user_id_seq'::regclass);


--
-- TOC entry 2118 (class 2604 OID 5868070)
-- Dependencies: 169 168
-- Name: id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY auth_user_groups ALTER COLUMN id SET DEFAULT nextval('auth_user_groups_id_seq'::regclass);


--
-- TOC entry 2119 (class 2604 OID 5868071)
-- Dependencies: 172 171
-- Name: id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY auth_user_user_permissions ALTER COLUMN id SET DEFAULT nextval('auth_user_user_permissions_id_seq'::regclass);


--
-- TOC entry 2120 (class 2604 OID 5868072)
-- Dependencies: 178 177
-- Name: id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbcaixa ALTER COLUMN id SET DEFAULT nextval('tbcaixa_id_seq'::regclass);


--
-- TOC entry 2121 (class 2604 OID 5868073)
-- Dependencies: 180 179
-- Name: id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbclassificacaoprocesso ALTER COLUMN id SET DEFAULT nextval('tbclassificacaoprocesso_id_seq'::regclass);


--
-- TOC entry 2122 (class 2604 OID 5868074)
-- Dependencies: 182 181
-- Name: id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbcontrato ALTER COLUMN id SET DEFAULT nextval('tbcontrato_id_seq'::regclass);


--
-- TOC entry 2123 (class 2604 OID 5868075)
-- Dependencies: 184 183
-- Name: id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbdivisao ALTER COLUMN id SET DEFAULT nextval('tbdivisao_id_seq'::regclass);


--
-- TOC entry 2124 (class 2604 OID 5868076)
-- Dependencies: 186 185
-- Name: id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbdocumentobase ALTER COLUMN id SET DEFAULT nextval('tbdocumentobase_id_seq'::regclass);


--
-- TOC entry 2125 (class 2604 OID 5868077)
-- Dependencies: 188 187
-- Name: id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbdocumentomemorando ALTER COLUMN id SET DEFAULT nextval('tbdocumentomemorando_id_seq'::regclass);


--
-- TOC entry 2126 (class 2604 OID 5868078)
-- Dependencies: 190 189
-- Name: id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbgleba ALTER COLUMN id SET DEFAULT nextval('tbgleba_id_seq'::regclass);


--
-- TOC entry 2127 (class 2604 OID 5868079)
-- Dependencies: 192 191
-- Name: id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbmovimentacao ALTER COLUMN id SET DEFAULT nextval('tbmovimentacao_id_seq'::regclass);


--
-- TOC entry 2128 (class 2604 OID 5868080)
-- Dependencies: 194 193
-- Name: id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbmunicipio ALTER COLUMN id SET DEFAULT nextval('tbmunicipio_id_seq'::regclass);


--
-- TOC entry 2129 (class 2604 OID 5868081)
-- Dependencies: 196 195
-- Name: id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbpecastecnicas ALTER COLUMN id SET DEFAULT nextval('tbpecastecnicas_id_seq'::regclass);


--
-- TOC entry 2130 (class 2604 OID 5868082)
-- Dependencies: 198 197
-- Name: id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbpendencia ALTER COLUMN id SET DEFAULT nextval('tbpendencia_id_seq'::regclass);


--
-- TOC entry 2131 (class 2604 OID 5868083)
-- Dependencies: 200 199
-- Name: id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbpregao ALTER COLUMN id SET DEFAULT nextval('tbpregao_id_seq'::regclass);


--
-- TOC entry 2132 (class 2604 OID 5868084)
-- Dependencies: 202 201
-- Name: id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbprocessobase ALTER COLUMN id SET DEFAULT nextval('tbprocessobase_id_seq'::regclass);


--
-- TOC entry 2133 (class 2604 OID 5868085)
-- Dependencies: 204 203
-- Name: id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbprocessoclausula ALTER COLUMN id SET DEFAULT nextval('tbprocessoclausula_id_seq'::regclass);


--
-- TOC entry 2134 (class 2604 OID 5868086)
-- Dependencies: 206 205
-- Name: id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbprocessorural ALTER COLUMN id SET DEFAULT nextval('tbprocessorural_id_seq'::regclass);


--
-- TOC entry 2135 (class 2604 OID 5868087)
-- Dependencies: 208 207
-- Name: id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbprocessosanexos ALTER COLUMN id SET DEFAULT nextval('tbprocessosanexos_id_seq'::regclass);


--
-- TOC entry 2136 (class 2604 OID 5868088)
-- Dependencies: 210 209
-- Name: id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbprocessourbano ALTER COLUMN id SET DEFAULT nextval('tbprocessourbano_id_seq'::regclass);


--
-- TOC entry 2137 (class 2604 OID 5868089)
-- Dependencies: 212 211
-- Name: id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbservidor ALTER COLUMN id SET DEFAULT nextval('tbservidor_id_seq'::regclass);


--
-- TOC entry 2138 (class 2604 OID 5868090)
-- Dependencies: 214 213
-- Name: id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbsituacaogeo ALTER COLUMN id SET DEFAULT nextval('tbsituacaogeo_id_seq'::regclass);


--
-- TOC entry 2139 (class 2604 OID 5868091)
-- Dependencies: 216 215
-- Name: id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbsituacaoprocesso ALTER COLUMN id SET DEFAULT nextval('tbsituacaoprocesso_id_seq'::regclass);


--
-- TOC entry 2140 (class 2604 OID 5868092)
-- Dependencies: 218 217
-- Name: id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbstatuspendencia ALTER COLUMN id SET DEFAULT nextval('tbstatuspendencia_id_seq'::regclass);


--
-- TOC entry 2141 (class 2604 OID 5868093)
-- Dependencies: 220 219
-- Name: id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbsubarea ALTER COLUMN id SET DEFAULT nextval('tbsubarea_id_seq'::regclass);


--
-- TOC entry 2142 (class 2604 OID 5868094)
-- Dependencies: 222 221
-- Name: id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbtipocaixa ALTER COLUMN id SET DEFAULT nextval('tbtipocaixa_id_seq'::regclass);


--
-- TOC entry 2143 (class 2604 OID 5868095)
-- Dependencies: 224 223
-- Name: id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbtipodocumento ALTER COLUMN id SET DEFAULT nextval('tbtipodocumento_id_seq'::regclass);


--
-- TOC entry 2144 (class 2604 OID 5868096)
-- Dependencies: 226 225
-- Name: id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbtipopendencia ALTER COLUMN id SET DEFAULT nextval('tbtipopendencia_id_seq'::regclass);


--
-- TOC entry 2145 (class 2604 OID 5868097)
-- Dependencies: 228 227
-- Name: id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbtipoprocesso ALTER COLUMN id SET DEFAULT nextval('tbtipoprocesso_id_seq'::regclass);


--
-- TOC entry 2146 (class 2604 OID 5868098)
-- Dependencies: 230 229
-- Name: id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbuf ALTER COLUMN id SET DEFAULT nextval('tbuf_id_seq'::regclass);


--
-- TOC entry 2148 (class 2606 OID 5868100)
-- Dependencies: 161 161 2351
-- Name: auth_group_name_key; Type: CONSTRAINT; Schema: public; Owner: admin; Tablespace: 
--

ALTER TABLE ONLY auth_group
    ADD CONSTRAINT auth_group_name_key UNIQUE (name);


--
-- TOC entry 2156 (class 2606 OID 5868102)
-- Dependencies: 163 163 2351
-- Name: auth_group_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: admin; Tablespace: 
--

ALTER TABLE ONLY auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_pkey PRIMARY KEY (id);


--
-- TOC entry 2151 (class 2606 OID 5868104)
-- Dependencies: 161 161 2351
-- Name: auth_group_pkey; Type: CONSTRAINT; Schema: public; Owner: admin; Tablespace: 
--

ALTER TABLE ONLY auth_group
    ADD CONSTRAINT auth_group_pkey PRIMARY KEY (id);


--
-- TOC entry 2159 (class 2606 OID 5868106)
-- Dependencies: 165 165 2351
-- Name: auth_permission_pkey; Type: CONSTRAINT; Schema: public; Owner: admin; Tablespace: 
--

ALTER TABLE ONLY auth_permission
    ADD CONSTRAINT auth_permission_pkey PRIMARY KEY (id);


--
-- TOC entry 2168 (class 2606 OID 5868108)
-- Dependencies: 168 168 2351
-- Name: auth_user_groups_pkey; Type: CONSTRAINT; Schema: public; Owner: admin; Tablespace: 
--

ALTER TABLE ONLY auth_user_groups
    ADD CONSTRAINT auth_user_groups_pkey PRIMARY KEY (id);


--
-- TOC entry 2161 (class 2606 OID 5868110)
-- Dependencies: 167 167 2351
-- Name: auth_user_pkey; Type: CONSTRAINT; Schema: public; Owner: admin; Tablespace: 
--

ALTER TABLE ONLY auth_user
    ADD CONSTRAINT auth_user_pkey PRIMARY KEY (id);


--
-- TOC entry 2172 (class 2606 OID 5868112)
-- Dependencies: 171 171 2351
-- Name: auth_user_user_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: admin; Tablespace: 
--

ALTER TABLE ONLY auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_pkey PRIMARY KEY (id);


--
-- TOC entry 2164 (class 2606 OID 5868114)
-- Dependencies: 167 167 2351
-- Name: auth_user_username_key; Type: CONSTRAINT; Schema: public; Owner: admin; Tablespace: 
--

ALTER TABLE ONLY auth_user
    ADD CONSTRAINT auth_user_username_key UNIQUE (username);


--
-- TOC entry 2176 (class 2606 OID 5868116)
-- Dependencies: 173 173 2351
-- Name: django_admin_log_pkey; Type: CONSTRAINT; Schema: public; Owner: admin; Tablespace: 
--

ALTER TABLE ONLY django_admin_log
    ADD CONSTRAINT django_admin_log_pkey PRIMARY KEY (id);


--
-- TOC entry 2179 (class 2606 OID 5868118)
-- Dependencies: 174 174 2351
-- Name: django_content_type_pkey; Type: CONSTRAINT; Schema: public; Owner: admin; Tablespace: 
--

ALTER TABLE ONLY django_content_type
    ADD CONSTRAINT django_content_type_pkey PRIMARY KEY (id);


--
-- TOC entry 2181 (class 2606 OID 5868120)
-- Dependencies: 175 175 2351
-- Name: django_session_pkey; Type: CONSTRAINT; Schema: public; Owner: admin; Tablespace: 
--

ALTER TABLE ONLY django_session
    ADD CONSTRAINT django_session_pkey PRIMARY KEY (session_key);


--
-- TOC entry 2184 (class 2606 OID 5868122)
-- Dependencies: 176 176 2351
-- Name: django_site_pkey; Type: CONSTRAINT; Schema: public; Owner: admin; Tablespace: 
--

ALTER TABLE ONLY django_site
    ADD CONSTRAINT django_site_pkey PRIMARY KEY (id);


--
-- TOC entry 2186 (class 2606 OID 5868124)
-- Dependencies: 177 177 2351
-- Name: tbcaixa_pkey; Type: CONSTRAINT; Schema: public; Owner: admin; Tablespace: 
--

ALTER TABLE ONLY tbcaixa
    ADD CONSTRAINT tbcaixa_pkey PRIMARY KEY (id);


--
-- TOC entry 2189 (class 2606 OID 5868126)
-- Dependencies: 179 179 2351
-- Name: tbclassificacaoprocesso_pkey; Type: CONSTRAINT; Schema: public; Owner: admin; Tablespace: 
--

ALTER TABLE ONLY tbclassificacaoprocesso
    ADD CONSTRAINT tbclassificacaoprocesso_pkey PRIMARY KEY (id);


--
-- TOC entry 2192 (class 2606 OID 5868128)
-- Dependencies: 181 181 2351
-- Name: tbcontrato_pkey; Type: CONSTRAINT; Schema: public; Owner: admin; Tablespace: 
--

ALTER TABLE ONLY tbcontrato
    ADD CONSTRAINT tbcontrato_pkey PRIMARY KEY (id);


--
-- TOC entry 2195 (class 2606 OID 5868130)
-- Dependencies: 183 183 2351
-- Name: tbdivisao_pkey; Type: CONSTRAINT; Schema: public; Owner: admin; Tablespace: 
--

ALTER TABLE ONLY tbdivisao
    ADD CONSTRAINT tbdivisao_pkey PRIMARY KEY (id);


--
-- TOC entry 2199 (class 2606 OID 5868132)
-- Dependencies: 185 185 2351
-- Name: tbdocumentobase_pkey; Type: CONSTRAINT; Schema: public; Owner: admin; Tablespace: 
--

ALTER TABLE ONLY tbdocumentobase
    ADD CONSTRAINT tbdocumentobase_pkey PRIMARY KEY (id);


--
-- TOC entry 2203 (class 2606 OID 5868134)
-- Dependencies: 187 187 2351
-- Name: tbdocumentomemorando_pkey; Type: CONSTRAINT; Schema: public; Owner: admin; Tablespace: 
--

ALTER TABLE ONLY tbdocumentomemorando
    ADD CONSTRAINT tbdocumentomemorando_pkey PRIMARY KEY (id);


--
-- TOC entry 2206 (class 2606 OID 5868136)
-- Dependencies: 189 189 2351
-- Name: tbgleba_pkey; Type: CONSTRAINT; Schema: public; Owner: admin; Tablespace: 
--

ALTER TABLE ONLY tbgleba
    ADD CONSTRAINT tbgleba_pkey PRIMARY KEY (id);


--
-- TOC entry 2210 (class 2606 OID 5868138)
-- Dependencies: 191 191 2351
-- Name: tbmovimentacao_pkey; Type: CONSTRAINT; Schema: public; Owner: admin; Tablespace: 
--

ALTER TABLE ONLY tbmovimentacao
    ADD CONSTRAINT tbmovimentacao_pkey PRIMARY KEY (id);


--
-- TOC entry 2216 (class 2606 OID 5868140)
-- Dependencies: 193 193 2351
-- Name: tbmunicipio_pkey; Type: CONSTRAINT; Schema: public; Owner: admin; Tablespace: 
--

ALTER TABLE ONLY tbmunicipio
    ADD CONSTRAINT tbmunicipio_pkey PRIMARY KEY (id);


--
-- TOC entry 2218 (class 2606 OID 5868142)
-- Dependencies: 195 195 2351
-- Name: tbpecastecnicas_pkey; Type: CONSTRAINT; Schema: public; Owner: admin; Tablespace: 
--

ALTER TABLE ONLY tbpecastecnicas
    ADD CONSTRAINT tbpecastecnicas_pkey PRIMARY KEY (id);


--
-- TOC entry 2225 (class 2606 OID 5868144)
-- Dependencies: 197 197 2351
-- Name: tbpendencia_pkey; Type: CONSTRAINT; Schema: public; Owner: admin; Tablespace: 
--

ALTER TABLE ONLY tbpendencia
    ADD CONSTRAINT tbpendencia_pkey PRIMARY KEY (id);


--
-- TOC entry 2230 (class 2606 OID 5868146)
-- Dependencies: 199 199 2351
-- Name: tbpregao_pkey; Type: CONSTRAINT; Schema: public; Owner: admin; Tablespace: 
--

ALTER TABLE ONLY tbpregao
    ADD CONSTRAINT tbpregao_pkey PRIMARY KEY (id);


--
-- TOC entry 2234 (class 2606 OID 5868148)
-- Dependencies: 201 201 2351
-- Name: tbprocessobase_pkey; Type: CONSTRAINT; Schema: public; Owner: admin; Tablespace: 
--

ALTER TABLE ONLY tbprocessobase
    ADD CONSTRAINT tbprocessobase_pkey PRIMARY KEY (id);


--
-- TOC entry 2243 (class 2606 OID 5868150)
-- Dependencies: 203 203 2351
-- Name: tbprocessoclausula_pkey; Type: CONSTRAINT; Schema: public; Owner: admin; Tablespace: 
--

ALTER TABLE ONLY tbprocessoclausula
    ADD CONSTRAINT tbprocessoclausula_pkey PRIMARY KEY (id);


--
-- TOC entry 2246 (class 2606 OID 5868152)
-- Dependencies: 205 205 2351
-- Name: tbprocessorural_pkey; Type: CONSTRAINT; Schema: public; Owner: admin; Tablespace: 
--

ALTER TABLE ONLY tbprocessorural
    ADD CONSTRAINT tbprocessorural_pkey PRIMARY KEY (id);


--
-- TOC entry 2250 (class 2606 OID 5868154)
-- Dependencies: 207 207 2351
-- Name: tbprocessosanexos_pkey; Type: CONSTRAINT; Schema: public; Owner: admin; Tablespace: 
--

ALTER TABLE ONLY tbprocessosanexos
    ADD CONSTRAINT tbprocessosanexos_pkey PRIMARY KEY (id);


--
-- TOC entry 2254 (class 2606 OID 5868156)
-- Dependencies: 209 209 2351
-- Name: tbprocessourbano_pkey; Type: CONSTRAINT; Schema: public; Owner: admin; Tablespace: 
--

ALTER TABLE ONLY tbprocessourbano
    ADD CONSTRAINT tbprocessourbano_pkey PRIMARY KEY (id);


--
-- TOC entry 2260 (class 2606 OID 5868158)
-- Dependencies: 211 211 2351
-- Name: tbservidor_pkey; Type: CONSTRAINT; Schema: public; Owner: admin; Tablespace: 
--

ALTER TABLE ONLY tbservidor
    ADD CONSTRAINT tbservidor_pkey PRIMARY KEY (id);


--
-- TOC entry 2263 (class 2606 OID 5868160)
-- Dependencies: 213 213 2351
-- Name: tbsituacaogeo_pkey; Type: CONSTRAINT; Schema: public; Owner: admin; Tablespace: 
--

ALTER TABLE ONLY tbsituacaogeo
    ADD CONSTRAINT tbsituacaogeo_pkey PRIMARY KEY (id);


--
-- TOC entry 2266 (class 2606 OID 5868162)
-- Dependencies: 215 215 2351
-- Name: tbsituacaoprocesso_pkey; Type: CONSTRAINT; Schema: public; Owner: admin; Tablespace: 
--

ALTER TABLE ONLY tbsituacaoprocesso
    ADD CONSTRAINT tbsituacaoprocesso_pkey PRIMARY KEY (id);


--
-- TOC entry 2269 (class 2606 OID 5868164)
-- Dependencies: 217 217 2351
-- Name: tbstatuspendencia_pkey; Type: CONSTRAINT; Schema: public; Owner: admin; Tablespace: 
--

ALTER TABLE ONLY tbstatuspendencia
    ADD CONSTRAINT tbstatuspendencia_pkey PRIMARY KEY (id);


--
-- TOC entry 2272 (class 2606 OID 5868166)
-- Dependencies: 219 219 2351
-- Name: tbsubarea_pkey; Type: CONSTRAINT; Schema: public; Owner: admin; Tablespace: 
--

ALTER TABLE ONLY tbsubarea
    ADD CONSTRAINT tbsubarea_pkey PRIMARY KEY (id);


--
-- TOC entry 2275 (class 2606 OID 5868168)
-- Dependencies: 221 221 2351
-- Name: tbtipocaixa_pkey; Type: CONSTRAINT; Schema: public; Owner: admin; Tablespace: 
--

ALTER TABLE ONLY tbtipocaixa
    ADD CONSTRAINT tbtipocaixa_pkey PRIMARY KEY (id);


--
-- TOC entry 2278 (class 2606 OID 5868170)
-- Dependencies: 223 223 2351
-- Name: tbtipodocumento_pkey; Type: CONSTRAINT; Schema: public; Owner: admin; Tablespace: 
--

ALTER TABLE ONLY tbtipodocumento
    ADD CONSTRAINT tbtipodocumento_pkey PRIMARY KEY (id);


--
-- TOC entry 2281 (class 2606 OID 5868172)
-- Dependencies: 225 225 2351
-- Name: tbtipopendencia_pkey; Type: CONSTRAINT; Schema: public; Owner: admin; Tablespace: 
--

ALTER TABLE ONLY tbtipopendencia
    ADD CONSTRAINT tbtipopendencia_pkey PRIMARY KEY (id);


--
-- TOC entry 2285 (class 2606 OID 5868174)
-- Dependencies: 227 227 2351
-- Name: tbtipoprocesso_pkey; Type: CONSTRAINT; Schema: public; Owner: admin; Tablespace: 
--

ALTER TABLE ONLY tbtipoprocesso
    ADD CONSTRAINT tbtipoprocesso_pkey PRIMARY KEY (id);


--
-- TOC entry 2288 (class 2606 OID 5868176)
-- Dependencies: 229 229 2351
-- Name: tbuf_pkey; Type: CONSTRAINT; Schema: public; Owner: admin; Tablespace: 
--

ALTER TABLE ONLY tbuf
    ADD CONSTRAINT tbuf_pkey PRIMARY KEY (id);


--
-- TOC entry 2149 (class 1259 OID 5868177)
-- Dependencies: 161 2351
-- Name: auth_group_name_like; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX auth_group_name_like ON auth_group USING btree (name varchar_pattern_ops);


--
-- TOC entry 2153 (class 1259 OID 5868178)
-- Dependencies: 163 2351
-- Name: auth_group_permissions_group_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX auth_group_permissions_group_id ON auth_group_permissions USING btree (group_id);


--
-- TOC entry 2154 (class 1259 OID 5868179)
-- Dependencies: 163 2351
-- Name: auth_group_permissions_permission_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX auth_group_permissions_permission_id ON auth_group_permissions USING btree (permission_id);


--
-- TOC entry 2157 (class 1259 OID 5868180)
-- Dependencies: 165 2351
-- Name: auth_permission_content_type_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX auth_permission_content_type_id ON auth_permission USING btree (content_type_id);


--
-- TOC entry 2166 (class 1259 OID 5868181)
-- Dependencies: 168 2351
-- Name: auth_user_groups_group_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX auth_user_groups_group_id ON auth_user_groups USING btree (group_id);


--
-- TOC entry 2169 (class 1259 OID 5868182)
-- Dependencies: 168 2351
-- Name: auth_user_groups_user_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX auth_user_groups_user_id ON auth_user_groups USING btree (user_id);


--
-- TOC entry 2162 (class 1259 OID 5868183)
-- Dependencies: 167 2351
-- Name: auth_user_tbdivisao_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX auth_user_tbdivisao_id ON auth_user USING btree (tbdivisao_id);


--
-- TOC entry 2170 (class 1259 OID 5868184)
-- Dependencies: 171 2351
-- Name: auth_user_user_permissions_permission_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX auth_user_user_permissions_permission_id ON auth_user_user_permissions USING btree (permission_id);


--
-- TOC entry 2173 (class 1259 OID 5868185)
-- Dependencies: 171 2351
-- Name: auth_user_user_permissions_user_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX auth_user_user_permissions_user_id ON auth_user_user_permissions USING btree (user_id);


--
-- TOC entry 2165 (class 1259 OID 5868186)
-- Dependencies: 167 2351
-- Name: auth_user_username_like; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX auth_user_username_like ON auth_user USING btree (username varchar_pattern_ops);


--
-- TOC entry 2174 (class 1259 OID 5868187)
-- Dependencies: 173 2351
-- Name: django_admin_log_content_type_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX django_admin_log_content_type_id ON django_admin_log USING btree (content_type_id);


--
-- TOC entry 2177 (class 1259 OID 5868188)
-- Dependencies: 173 2351
-- Name: django_admin_log_user_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX django_admin_log_user_id ON django_admin_log USING btree (user_id);


--
-- TOC entry 2182 (class 1259 OID 5868189)
-- Dependencies: 175 2351
-- Name: django_session_session_key_like; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX django_session_session_key_like ON django_session USING btree (session_key varchar_pattern_ops);


--
-- TOC entry 2152 (class 1259 OID 5868550)
-- Dependencies: 161 2351
-- Name: fki_tbdivisao_id_auth_group; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX fki_tbdivisao_id_auth_group ON auth_group USING btree (tbdivisao_id);


--
-- TOC entry 2187 (class 1259 OID 5868190)
-- Dependencies: 177 2351
-- Name: tbcaixa_tbtipocaixa_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX tbcaixa_tbtipocaixa_id ON tbcaixa USING btree (tbtipocaixa_id);


--
-- TOC entry 2190 (class 1259 OID 5868191)
-- Dependencies: 179 2351
-- Name: tbclassificacaoprocesso_tbdivisao_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX tbclassificacaoprocesso_tbdivisao_id ON tbclassificacaoprocesso USING btree (tbdivisao_id);


--
-- TOC entry 2193 (class 1259 OID 5868192)
-- Dependencies: 181 2351
-- Name: tbcontrato_tbdivisao_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX tbcontrato_tbdivisao_id ON tbcontrato USING btree (tbdivisao_id);


--
-- TOC entry 2196 (class 1259 OID 5868193)
-- Dependencies: 183 2351
-- Name: tbdivisao_tbuf_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX tbdivisao_tbuf_id ON tbdivisao USING btree (tbuf_id);


CREATE INDEX tbgleba_tbuf_id ON tbgleba USING btree (tbuf_id);

--
-- TOC entry 2197 (class 1259 OID 5868194)
-- Dependencies: 185 2351
-- Name: tbdocumentobase_auth_user_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX tbdocumentobase_auth_user_id ON tbdocumentobase USING btree (auth_user_id);


--
-- TOC entry 2200 (class 1259 OID 5868195)
-- Dependencies: 185 2351
-- Name: tbdocumentobase_tbdivisao_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX tbdocumentobase_tbdivisao_id ON tbdocumentobase USING btree (tbdivisao_id);


--
-- TOC entry 2201 (class 1259 OID 5868196)
-- Dependencies: 185 2351
-- Name: tbdocumentobase_tbtipodocumento_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX tbdocumentobase_tbtipodocumento_id ON tbdocumentobase USING btree (tbtipodocumento_id);


--
-- TOC entry 2204 (class 1259 OID 5868197)
-- Dependencies: 187 2351
-- Name: tbdocumentomemorando_tbdocumentobase_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX tbdocumentomemorando_tbdocumentobase_id ON tbdocumentomemorando USING btree (tbdocumentobase_id);


--
-- TOC entry 2207 (class 1259 OID 5868198)
-- Dependencies: 189 2351
-- Name: tbgleba_tbsubarea_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX tbgleba_tbsubarea_id ON tbgleba USING btree (tbsubarea_id);


--
-- TOC entry 2208 (class 1259 OID 5868199)
-- Dependencies: 191 2351
-- Name: tbmovimentacao_auth_user_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX tbmovimentacao_auth_user_id ON tbmovimentacao USING btree (auth_user_id);


--
-- TOC entry 2211 (class 1259 OID 5868200)
-- Dependencies: 191 2351
-- Name: tbmovimentacao_tbcaixa_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX tbmovimentacao_tbcaixa_id ON tbmovimentacao USING btree (tbcaixa_id);


--
-- TOC entry 2212 (class 1259 OID 5868201)
-- Dependencies: 191 2351
-- Name: tbmovimentacao_tbcaixa_id_origem; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX tbmovimentacao_tbcaixa_id_origem ON tbmovimentacao USING btree (tbcaixa_id_origem);


--
-- TOC entry 2213 (class 1259 OID 5868202)
-- Dependencies: 191 2351
-- Name: tbmovimentacao_tbprocessobase_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX tbmovimentacao_tbprocessobase_id ON tbmovimentacao USING btree (tbprocessobase_id);


--
-- TOC entry 2214 (class 1259 OID 5868203)
-- Dependencies: 193 2351
-- Name: tbmunicipio_Codigo_UF; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX "tbmunicipio_Codigo_UF" ON tbmunicipio USING btree ("Codigo_UF");


--
-- TOC entry 2219 (class 1259 OID 5868204)
-- Dependencies: 195 2351
-- Name: tbpecastecnicas_tbcaixa_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX tbpecastecnicas_tbcaixa_id ON tbpecastecnicas USING btree (tbcaixa_id);


--
-- TOC entry 2220 (class 1259 OID 5868205)
-- Dependencies: 195 2351
-- Name: tbpecastecnicas_tbcontrato_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX tbpecastecnicas_tbcontrato_id ON tbpecastecnicas USING btree (tbcontrato_id);


--
-- TOC entry 2221 (class 1259 OID 5868206)
-- Dependencies: 195 2351
-- Name: tbpecastecnicas_tbdivisao_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX tbpecastecnicas_tbdivisao_id ON tbpecastecnicas USING btree (tbdivisao_id);


--
-- TOC entry 2222 (class 1259 OID 5868207)
-- Dependencies: 195 2351
-- Name: tbpecastecnicas_tbgleba_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX tbpecastecnicas_tbgleba_id ON tbpecastecnicas USING btree (tbgleba_id);


--
-- TOC entry 2223 (class 1259 OID 5868208)
-- Dependencies: 197 2351
-- Name: tbpendencia_auth_user_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX tbpendencia_auth_user_id ON tbpendencia USING btree (auth_user_id);


--
-- TOC entry 2226 (class 1259 OID 5868209)
-- Dependencies: 197 2351
-- Name: tbpendencia_tbprocessobase_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX tbpendencia_tbprocessobase_id ON tbpendencia USING btree (tbprocessobase_id);


--
-- TOC entry 2227 (class 1259 OID 5868210)
-- Dependencies: 197 2351
-- Name: tbpendencia_tbstatuspendencia_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX tbpendencia_tbstatuspendencia_id ON tbpendencia USING btree (tbstatuspendencia_id);


--
-- TOC entry 2228 (class 1259 OID 5868211)
-- Dependencies: 197 2351
-- Name: tbpendencia_tbtipopendencia_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX tbpendencia_tbtipopendencia_id ON tbpendencia USING btree (tbtipopendencia_id);


--
-- TOC entry 2231 (class 1259 OID 5868212)
-- Dependencies: 199 2351
-- Name: tbpregao_tbdivisao_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX tbpregao_tbdivisao_id ON tbpregao USING btree (tbdivisao_id);


--
-- TOC entry 2232 (class 1259 OID 5868213)
-- Dependencies: 201 2351
-- Name: tbprocessobase_auth_user_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX tbprocessobase_auth_user_id ON tbprocessobase USING btree (auth_user_id);


--
-- TOC entry 2235 (class 1259 OID 5868214)
-- Dependencies: 201 2351
-- Name: tbprocessobase_tbcaixa_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX tbprocessobase_tbcaixa_id ON tbprocessobase USING btree (tbcaixa_id);


--
-- TOC entry 2236 (class 1259 OID 5868215)
-- Dependencies: 201 2351
-- Name: tbprocessobase_tbclassificacaoprocesso_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX tbprocessobase_tbclassificacaoprocesso_id ON tbprocessobase USING btree (tbclassificacaoprocesso_id);


--
-- TOC entry 2237 (class 1259 OID 5868216)
-- Dependencies: 201 2351
-- Name: tbprocessobase_tbdivisao_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX tbprocessobase_tbdivisao_id ON tbprocessobase USING btree (tbdivisao_id);


--
-- TOC entry 2238 (class 1259 OID 5868217)
-- Dependencies: 201 2351
-- Name: tbprocessobase_tbgleba_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX tbprocessobase_tbgleba_id ON tbprocessobase USING btree (tbgleba_id);


--
-- TOC entry 2239 (class 1259 OID 5868218)
-- Dependencies: 201 2351
-- Name: tbprocessobase_tbmunicipio_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX tbprocessobase_tbmunicipio_id ON tbprocessobase USING btree (tbmunicipio_id);


--
-- TOC entry 2240 (class 1259 OID 5868219)
-- Dependencies: 201 2351
-- Name: tbprocessobase_tbsituacaoprocesso_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX tbprocessobase_tbsituacaoprocesso_id ON tbprocessobase USING btree (tbsituacaoprocesso_id);


--
-- TOC entry 2241 (class 1259 OID 5868220)
-- Dependencies: 201 2351
-- Name: tbprocessobase_tbtipoprocesso_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX tbprocessobase_tbtipoprocesso_id ON tbprocessobase USING btree (tbtipoprocesso_id);


--
-- TOC entry 2244 (class 1259 OID 5868221)
-- Dependencies: 203 2351
-- Name: tbprocessoclausula_tbprocessobase_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX tbprocessoclausula_tbprocessobase_id ON tbprocessoclausula USING btree (tbprocessobase_id);


--
-- TOC entry 2247 (class 1259 OID 5868222)
-- Dependencies: 205 2351
-- Name: tbprocessorural_tbprocessobase_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX tbprocessorural_tbprocessobase_id ON tbprocessorural USING btree (tbprocessobase_id);


--
-- TOC entry 2248 (class 1259 OID 5868223)
-- Dependencies: 207 2351
-- Name: tbprocessosanexos_auth_user_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX tbprocessosanexos_auth_user_id ON tbprocessosanexos USING btree (auth_user_id);


--
-- TOC entry 2251 (class 1259 OID 5868224)
-- Dependencies: 207 2351
-- Name: tbprocessosanexos_tbprocessobase_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX tbprocessosanexos_tbprocessobase_id ON tbprocessosanexos USING btree (tbprocessobase_id);


--
-- TOC entry 2252 (class 1259 OID 5868225)
-- Dependencies: 207 2351
-- Name: tbprocessosanexos_tbprocessobase_id_anexo; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX tbprocessosanexos_tbprocessobase_id_anexo ON tbprocessosanexos USING btree (tbprocessobase_id_anexo);


--
-- TOC entry 2255 (class 1259 OID 5868226)
-- Dependencies: 209 2351
-- Name: tbprocessourbano_tbcontrato_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX tbprocessourbano_tbcontrato_id ON tbprocessourbano USING btree (tbcontrato_id);


--
-- TOC entry 2256 (class 1259 OID 5868227)
-- Dependencies: 209 2351
-- Name: tbprocessourbano_tbpregao_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX tbprocessourbano_tbpregao_id ON tbprocessourbano USING btree (tbpregao_id);


--
-- TOC entry 2257 (class 1259 OID 5868228)
-- Dependencies: 209 2351
-- Name: tbprocessourbano_tbprocessobase_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX tbprocessourbano_tbprocessobase_id ON tbprocessourbano USING btree (tbprocessobase_id);


--
-- TOC entry 2258 (class 1259 OID 5868229)
-- Dependencies: 209 2351
-- Name: tbprocessourbano_tbsituacaogeo_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX tbprocessourbano_tbsituacaogeo_id ON tbprocessourbano USING btree (tbsituacaogeo_id);


--
-- TOC entry 2261 (class 1259 OID 5868230)
-- Dependencies: 211 2351
-- Name: tbservidor_tbdivisao_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX tbservidor_tbdivisao_id ON tbservidor USING btree (tbdivisao_id);


--
-- TOC entry 2264 (class 1259 OID 5868231)
-- Dependencies: 213 2351
-- Name: tbsituacaogeo_tbdivisao_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX tbsituacaogeo_tbdivisao_id ON tbsituacaogeo USING btree (tbdivisao_id);


--
-- TOC entry 2267 (class 1259 OID 5868232)
-- Dependencies: 215 2351
-- Name: tbsituacaoprocesso_tbdivisao_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX tbsituacaoprocesso_tbdivisao_id ON tbsituacaoprocesso USING btree (tbdivisao_id);


--
-- TOC entry 2270 (class 1259 OID 5868233)
-- Dependencies: 217 2351
-- Name: tbstatuspendencia_tbdivisao_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX tbstatuspendencia_tbdivisao_id ON tbstatuspendencia USING btree (tbdivisao_id);


--
-- TOC entry 2273 (class 1259 OID 5868234)
-- Dependencies: 219 2351
-- Name: tbsubarea_tbdivisao_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX tbsubarea_tbdivisao_id ON tbsubarea USING btree (tbdivisao_id);


--
-- TOC entry 2276 (class 1259 OID 5868235)
-- Dependencies: 221 2351
-- Name: tbtipocaixa_tbdivisao_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX tbtipocaixa_tbdivisao_id ON tbtipocaixa USING btree (tbdivisao_id);


--
-- TOC entry 2279 (class 1259 OID 5868236)
-- Dependencies: 223 2351
-- Name: tbtipodocumento_tbdivisao_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX tbtipodocumento_tbdivisao_id ON tbtipodocumento USING btree (tbdivisao_id);


--
-- TOC entry 2282 (class 1259 OID 5868237)
-- Dependencies: 225 2351
-- Name: tbtipopendencia_tbdivisao_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX tbtipopendencia_tbdivisao_id ON tbtipopendencia USING btree (tbdivisao_id);


--
-- TOC entry 2283 (class 1259 OID 5868238)
-- Dependencies: 225 2351
-- Name: tbtipopendencia_tbtipoprocesso_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX tbtipopendencia_tbtipoprocesso_id ON tbtipopendencia USING btree (tbtipoprocesso_id);


--
-- TOC entry 2286 (class 1259 OID 5868239)
-- Dependencies: 227 2351
-- Name: tbtipoprocesso_tbdivisao_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX tbtipoprocesso_tbdivisao_id ON tbtipoprocesso USING btree (tbdivisao_id);


--
-- TOC entry 2313 (class 2606 OID 5868240)
-- Dependencies: 229 193 2287 2351
-- Name: Codigo_UF_refs_id_29984a75; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbmunicipio
    ADD CONSTRAINT "Codigo_UF_refs_id_29984a75" FOREIGN KEY ("Codigo_UF") REFERENCES tbuf(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2290 (class 2606 OID 5868245)
-- Dependencies: 2150 163 161 2351
-- Name: auth_group_permissions_group_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_fkey FOREIGN KEY (group_id) REFERENCES auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2294 (class 2606 OID 5868250)
-- Dependencies: 168 2150 161 2351
-- Name: auth_user_groups_group_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY auth_user_groups
    ADD CONSTRAINT auth_user_groups_group_id_fkey FOREIGN KEY (group_id) REFERENCES auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2295 (class 2606 OID 5868255)
-- Dependencies: 167 2160 168 2351
-- Name: auth_user_groups_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY auth_user_groups
    ADD CONSTRAINT auth_user_groups_user_id_fkey FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2296 (class 2606 OID 5868260)
-- Dependencies: 2158 171 165 2351
-- Name: auth_user_user_permissions_permission_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_permission_id_fkey FOREIGN KEY (permission_id) REFERENCES auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2297 (class 2606 OID 5868265)
-- Dependencies: 167 2160 171 2351
-- Name: auth_user_user_permissions_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_user_id_fkey FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2298 (class 2606 OID 5868270)
-- Dependencies: 2178 173 174 2351
-- Name: content_type_id_refs_id_93d2d1f8; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY django_admin_log
    ADD CONSTRAINT content_type_id_refs_id_93d2d1f8 FOREIGN KEY (content_type_id) REFERENCES django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2292 (class 2606 OID 5868275)
-- Dependencies: 174 165 2178 2351
-- Name: content_type_id_refs_id_d043b34a; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY auth_permission
    ADD CONSTRAINT content_type_id_refs_id_d043b34a FOREIGN KEY (content_type_id) REFERENCES django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2299 (class 2606 OID 5868280)
-- Dependencies: 167 2160 173 2351
-- Name: django_admin_log_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY django_admin_log
    ADD CONSTRAINT django_admin_log_user_id_fkey FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2291 (class 2606 OID 5868285)
-- Dependencies: 165 163 2158 2351
-- Name: permission_id_refs_id_6ba0f519; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY auth_group_permissions
    ADD CONSTRAINT permission_id_refs_id_6ba0f519 FOREIGN KEY (permission_id) REFERENCES auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2289 (class 2606 OID 5868545)
-- Dependencies: 2194 161 183 2351
-- Name: tbdivisao_id_auth_group; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY auth_group
    ADD CONSTRAINT tbdivisao_id_auth_group FOREIGN KEY (tbdivisao_id) REFERENCES tbdivisao(id);


--
-- TOC entry 2301 (class 2606 OID 5868290)
-- Dependencies: 183 179 2194 2351
-- Name: tbdivisao_id_refs_id_00d25a11; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbclassificacaoprocesso
    ADD CONSTRAINT tbdivisao_id_refs_id_00d25a11 FOREIGN KEY (tbdivisao_id) REFERENCES tbdivisao(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2293 (class 2606 OID 5868295)
-- Dependencies: 183 167 2194 2351
-- Name: tbdivisao_id_refs_id_209f7cf0; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY auth_user
    ADD CONSTRAINT tbdivisao_id_refs_id_209f7cf0 FOREIGN KEY (tbdivisao_id) REFERENCES tbdivisao(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2302 (class 2606 OID 5868300)
-- Dependencies: 2194 183 181 2351
-- Name: tbdivisao_id_refs_id_c808e225; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbcontrato
    ADD CONSTRAINT tbdivisao_id_refs_id_c808e225 FOREIGN KEY (tbdivisao_id) REFERENCES tbdivisao(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2304 (class 2606 OID 5868305)
-- Dependencies: 185 2160 167 2351
-- Name: tbdocumentobase_auth_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbdocumentobase
    ADD CONSTRAINT tbdocumentobase_auth_user_id_fkey FOREIGN KEY (auth_user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2305 (class 2606 OID 5868310)
-- Dependencies: 185 2194 183 2351
-- Name: tbdocumentobase_tbdivisao_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbdocumentobase
    ADD CONSTRAINT tbdocumentobase_tbdivisao_id_fkey FOREIGN KEY (tbdivisao_id) REFERENCES tbdivisao(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2306 (class 2606 OID 5868315)
-- Dependencies: 185 2277 223 2351
-- Name: tbdocumentobase_tbtipodocumento_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbdocumentobase
    ADD CONSTRAINT tbdocumentobase_tbtipodocumento_id_fkey FOREIGN KEY (tbtipodocumento_id) REFERENCES tbtipodocumento(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2307 (class 2606 OID 5868320)
-- Dependencies: 187 2198 185 2351
-- Name: tbdocumentomemorando_tbdocumentobase_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbdocumentomemorando
    ADD CONSTRAINT tbdocumentomemorando_tbdocumentobase_id_fkey FOREIGN KEY (tbdocumentobase_id) REFERENCES tbdocumentobase(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2309 (class 2606 OID 5868325)
-- Dependencies: 2160 167 191 2351
-- Name: tbmovimentacao_auth_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbmovimentacao
    ADD CONSTRAINT tbmovimentacao_auth_user_id_fkey FOREIGN KEY (auth_user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2310 (class 2606 OID 5868330)
-- Dependencies: 177 2185 191 2351
-- Name: tbmovimentacao_tbcaixa_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbmovimentacao
    ADD CONSTRAINT tbmovimentacao_tbcaixa_id_fkey FOREIGN KEY (tbcaixa_id) REFERENCES tbcaixa(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2311 (class 2606 OID 5868335)
-- Dependencies: 177 2185 191 2351
-- Name: tbmovimentacao_tbcaixa_id_origem_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbmovimentacao
    ADD CONSTRAINT tbmovimentacao_tbcaixa_id_origem_fkey FOREIGN KEY (tbcaixa_id_origem) REFERENCES tbcaixa(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2314 (class 2606 OID 5868340)
-- Dependencies: 177 2185 195 2351
-- Name: tbpecastecnicas_tbcaixa_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbpecastecnicas
    ADD CONSTRAINT tbpecastecnicas_tbcaixa_id_fkey FOREIGN KEY (tbcaixa_id) REFERENCES tbcaixa(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2315 (class 2606 OID 5868345)
-- Dependencies: 2191 181 195 2351
-- Name: tbpecastecnicas_tbcontrato_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbpecastecnicas
    ADD CONSTRAINT tbpecastecnicas_tbcontrato_id_fkey FOREIGN KEY (tbcontrato_id) REFERENCES tbcontrato(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2316 (class 2606 OID 5868350)
-- Dependencies: 183 195 2194 2351
-- Name: tbpecastecnicas_tbdivisao_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbpecastecnicas
    ADD CONSTRAINT tbpecastecnicas_tbdivisao_id_fkey FOREIGN KEY (tbdivisao_id) REFERENCES tbdivisao(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2317 (class 2606 OID 5868355)
-- Dependencies: 189 195 2205 2351
-- Name: tbpecastecnicas_tbgleba_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbpecastecnicas
    ADD CONSTRAINT tbpecastecnicas_tbgleba_id_fkey FOREIGN KEY (tbgleba_id) REFERENCES tbgleba(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2318 (class 2606 OID 5868360)
-- Dependencies: 167 197 2160 2351
-- Name: tbpendencia_auth_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbpendencia
    ADD CONSTRAINT tbpendencia_auth_user_id_fkey FOREIGN KEY (auth_user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2336 (class 2606 OID 5868365)
-- Dependencies: 199 2229 209 2351
-- Name: tbpregao_id_refs_id_f323926f; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbprocessourbano
    ADD CONSTRAINT tbpregao_id_refs_id_f323926f FOREIGN KEY (tbpregao_id) REFERENCES tbpregao(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2322 (class 2606 OID 5868370)
-- Dependencies: 183 199 2194 2351
-- Name: tbpregao_tbdivisao_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbpregao
    ADD CONSTRAINT tbpregao_tbdivisao_id_fkey FOREIGN KEY (tbdivisao_id) REFERENCES tbdivisao(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2323 (class 2606 OID 5868375)
-- Dependencies: 201 2160 167 2351
-- Name: tbprocessobase_auth_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbprocessobase
    ADD CONSTRAINT tbprocessobase_auth_user_id_fkey FOREIGN KEY (auth_user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2312 (class 2606 OID 5868380)
-- Dependencies: 2233 201 191 2351
-- Name: tbprocessobase_id_refs_id_5aebc46a; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbmovimentacao
    ADD CONSTRAINT tbprocessobase_id_refs_id_5aebc46a FOREIGN KEY (tbprocessobase_id) REFERENCES tbprocessobase(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2319 (class 2606 OID 5868385)
-- Dependencies: 197 2233 201 2351
-- Name: tbprocessobase_id_refs_id_86d3804c; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbpendencia
    ADD CONSTRAINT tbprocessobase_id_refs_id_86d3804c FOREIGN KEY (tbprocessobase_id) REFERENCES tbprocessobase(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2324 (class 2606 OID 5868390)
-- Dependencies: 177 2185 201 2351
-- Name: tbprocessobase_tbcaixa_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbprocessobase
    ADD CONSTRAINT tbprocessobase_tbcaixa_id_fkey FOREIGN KEY (tbcaixa_id) REFERENCES tbcaixa(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2325 (class 2606 OID 5868395)
-- Dependencies: 201 179 2188 2351
-- Name: tbprocessobase_tbclassificacaoprocesso_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbprocessobase
    ADD CONSTRAINT tbprocessobase_tbclassificacaoprocesso_id_fkey FOREIGN KEY (tbclassificacaoprocesso_id) REFERENCES tbclassificacaoprocesso(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2326 (class 2606 OID 5868400)
-- Dependencies: 2194 201 183 2351
-- Name: tbprocessobase_tbdivisao_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbprocessobase
    ADD CONSTRAINT tbprocessobase_tbdivisao_id_fkey FOREIGN KEY (tbdivisao_id) REFERENCES tbdivisao(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2327 (class 2606 OID 5868405)
-- Dependencies: 189 2205 201 2351
-- Name: tbprocessobase_tbgleba_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbprocessobase
    ADD CONSTRAINT tbprocessobase_tbgleba_id_fkey FOREIGN KEY (tbgleba_id) REFERENCES tbgleba(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2328 (class 2606 OID 5868410)
-- Dependencies: 201 193 2215 2351
-- Name: tbprocessobase_tbmunicipio_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbprocessobase
    ADD CONSTRAINT tbprocessobase_tbmunicipio_id_fkey FOREIGN KEY (tbmunicipio_id) REFERENCES tbmunicipio(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2331 (class 2606 OID 5868415)
-- Dependencies: 203 201 2233 2351
-- Name: tbprocessoclausula_tbprocessobase_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbprocessoclausula
    ADD CONSTRAINT tbprocessoclausula_tbprocessobase_id_fkey FOREIGN KEY (tbprocessobase_id) REFERENCES tbprocessobase(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2332 (class 2606 OID 5868420)
-- Dependencies: 201 2233 205 2351
-- Name: tbprocessorural_tbprocessobase_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbprocessorural
    ADD CONSTRAINT tbprocessorural_tbprocessobase_id_fkey FOREIGN KEY (tbprocessobase_id) REFERENCES tbprocessobase(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2333 (class 2606 OID 5868425)
-- Dependencies: 2160 207 167 2351
-- Name: tbprocessosanexos_auth_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbprocessosanexos
    ADD CONSTRAINT tbprocessosanexos_auth_user_id_fkey FOREIGN KEY (auth_user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2334 (class 2606 OID 5868430)
-- Dependencies: 2233 201 207 2351
-- Name: tbprocessosanexos_tbprocessobase_id_anexo_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbprocessosanexos
    ADD CONSTRAINT tbprocessosanexos_tbprocessobase_id_anexo_fkey FOREIGN KEY (tbprocessobase_id_anexo) REFERENCES tbprocessobase(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2335 (class 2606 OID 5868435)
-- Dependencies: 207 201 2233 2351
-- Name: tbprocessosanexos_tbprocessobase_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbprocessosanexos
    ADD CONSTRAINT tbprocessosanexos_tbprocessobase_id_fkey FOREIGN KEY (tbprocessobase_id) REFERENCES tbprocessobase(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2337 (class 2606 OID 5868440)
-- Dependencies: 209 2191 181 2351
-- Name: tbprocessourbano_tbcontrato_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbprocessourbano
    ADD CONSTRAINT tbprocessourbano_tbcontrato_id_fkey FOREIGN KEY (tbcontrato_id) REFERENCES tbcontrato(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2338 (class 2606 OID 5868445)
-- Dependencies: 201 2233 209 2351
-- Name: tbprocessourbano_tbprocessobase_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbprocessourbano
    ADD CONSTRAINT tbprocessourbano_tbprocessobase_id_fkey FOREIGN KEY (tbprocessobase_id) REFERENCES tbprocessobase(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2340 (class 2606 OID 5868450)
-- Dependencies: 183 2194 211 2351
-- Name: tbservidor_tbdivisao_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbservidor
    ADD CONSTRAINT tbservidor_tbdivisao_id_fkey FOREIGN KEY (tbdivisao_id) REFERENCES tbdivisao(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2339 (class 2606 OID 5868455)
-- Dependencies: 209 2262 213 2351
-- Name: tbsituacaogeo_id_refs_id_f9087efb; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbprocessourbano
    ADD CONSTRAINT tbsituacaogeo_id_refs_id_f9087efb FOREIGN KEY (tbsituacaogeo_id) REFERENCES tbsituacaogeo(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2341 (class 2606 OID 5868460)
-- Dependencies: 2194 183 213 2351
-- Name: tbsituacaogeo_tbdivisao_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbsituacaogeo
    ADD CONSTRAINT tbsituacaogeo_tbdivisao_id_fkey FOREIGN KEY (tbdivisao_id) REFERENCES tbdivisao(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2329 (class 2606 OID 5868465)
-- Dependencies: 201 2265 215 2351
-- Name: tbsituacaoprocesso_id_refs_id_bfef2fda; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbprocessobase
    ADD CONSTRAINT tbsituacaoprocesso_id_refs_id_bfef2fda FOREIGN KEY (tbsituacaoprocesso_id) REFERENCES tbsituacaoprocesso(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2342 (class 2606 OID 5868470)
-- Dependencies: 215 2194 183 2351
-- Name: tbsituacaoprocesso_tbdivisao_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbsituacaoprocesso
    ADD CONSTRAINT tbsituacaoprocesso_tbdivisao_id_fkey FOREIGN KEY (tbdivisao_id) REFERENCES tbdivisao(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2320 (class 2606 OID 5868475)
-- Dependencies: 197 217 2268 2351
-- Name: tbstatuspendencia_id_refs_id_615418ce; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbpendencia
    ADD CONSTRAINT tbstatuspendencia_id_refs_id_615418ce FOREIGN KEY (tbstatuspendencia_id) REFERENCES tbstatuspendencia(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2343 (class 2606 OID 5868480)
-- Dependencies: 183 2194 217 2351
-- Name: tbstatuspendencia_tbdivisao_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbstatuspendencia
    ADD CONSTRAINT tbstatuspendencia_tbdivisao_id_fkey FOREIGN KEY (tbdivisao_id) REFERENCES tbdivisao(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2308 (class 2606 OID 5868485)
-- Dependencies: 2271 219 189 2351
-- Name: tbsubarea_id_refs_id_c3c14a3b; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbgleba
    ADD CONSTRAINT tbsubarea_id_refs_id_c3c14a3b FOREIGN KEY (tbsubarea_id) REFERENCES tbsubarea(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2344 (class 2606 OID 5868490)
-- Dependencies: 183 2194 219 2351
-- Name: tbsubarea_tbdivisao_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbsubarea
    ADD CONSTRAINT tbsubarea_tbdivisao_id_fkey FOREIGN KEY (tbdivisao_id) REFERENCES tbdivisao(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2300 (class 2606 OID 5868495)
-- Dependencies: 2274 177 221 2351
-- Name: tbtipocaixa_id_refs_id_1f3d944c; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbcaixa
    ADD CONSTRAINT tbtipocaixa_id_refs_id_1f3d944c FOREIGN KEY (tbtipocaixa_id) REFERENCES tbtipocaixa(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2345 (class 2606 OID 5868500)
-- Dependencies: 221 2194 183 2351
-- Name: tbtipocaixa_tbdivisao_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbtipocaixa
    ADD CONSTRAINT tbtipocaixa_tbdivisao_id_fkey FOREIGN KEY (tbdivisao_id) REFERENCES tbdivisao(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2346 (class 2606 OID 5868505)
-- Dependencies: 183 223 2194 2351
-- Name: tbtipodocumento_tbdivisao_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbtipodocumento
    ADD CONSTRAINT tbtipodocumento_tbdivisao_id_fkey FOREIGN KEY (tbdivisao_id) REFERENCES tbdivisao(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2321 (class 2606 OID 5868510)
-- Dependencies: 197 2280 225 2351
-- Name: tbtipopendencia_id_refs_id_4f9053c1; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbpendencia
    ADD CONSTRAINT tbtipopendencia_id_refs_id_4f9053c1 FOREIGN KEY (tbtipopendencia_id) REFERENCES tbtipopendencia(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2347 (class 2606 OID 5868515)
-- Dependencies: 183 2194 225 2351
-- Name: tbtipopendencia_tbdivisao_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbtipopendencia
    ADD CONSTRAINT tbtipopendencia_tbdivisao_id_fkey FOREIGN KEY (tbdivisao_id) REFERENCES tbdivisao(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2348 (class 2606 OID 5868520)
-- Dependencies: 2284 225 227 2351
-- Name: tbtipoprocesso_id_refs_id_14dae0cf; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbtipopendencia
    ADD CONSTRAINT tbtipoprocesso_id_refs_id_14dae0cf FOREIGN KEY (tbtipoprocesso_id) REFERENCES tbtipoprocesso(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2330 (class 2606 OID 5868525)
-- Dependencies: 2284 227 201 2351
-- Name: tbtipoprocesso_id_refs_id_64d671a3; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbprocessobase
    ADD CONSTRAINT tbtipoprocesso_id_refs_id_64d671a3 FOREIGN KEY (tbtipoprocesso_id) REFERENCES tbtipoprocesso(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2349 (class 2606 OID 5868530)
-- Dependencies: 2194 227 183 2351
-- Name: tbtipoprocesso_tbdivisao_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbtipoprocesso
    ADD CONSTRAINT tbtipoprocesso_tbdivisao_id_fkey FOREIGN KEY (tbdivisao_id) REFERENCES tbdivisao(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2303 (class 2606 OID 5868535)
-- Dependencies: 183 229 2287 2351
-- Name: tbuf_id_refs_id_c8d633fb; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbdivisao
    ADD CONSTRAINT tbuf_id_refs_id_c8d633fb FOREIGN KEY (tbuf_id) REFERENCES tbuf(id) DEFERRABLE INITIALLY DEFERRED;

ALTER TABLE ONLY tbgleba
    ADD CONSTRAINT tbuf_id_tbgleba FOREIGN KEY (tbuf_id) REFERENCES tbuf(id) DEFERRABLE INITIALLY DEFERRED;

--
-- TOC entry 2356 (class 0 OID 0)
-- Dependencies: 6
-- Name: public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM postgres;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO PUBLIC;


-- Completed on 2014-01-14 23:22:20 BRT

--
-- PostgreSQL database dump complete
--

