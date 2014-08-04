--
-- PostgreSQL database dump
--

-- Dumped from database version 9.2.4
-- Dumped by pg_dump version 9.2.4
-- Started on 2014-03-25 12:32:35

SET statement_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

--
-- TOC entry 7 (class 2615 OID 102640)
-- Name: documentos; Type: SCHEMA; Schema: -; Owner: admin
--

CREATE SCHEMA documentos;


ALTER SCHEMA documentos OWNER TO admin;

--
-- TOC entry 263 (class 3079 OID 11727)
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- TOC entry 2514 (class 0 OID 0)
-- Dependencies: 263
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = documentos, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- TOC entry 254 (class 1259 OID 102712)
-- Name: tbbmp; Type: TABLE; Schema: documentos; Owner: admin; Tablespace: 
--

CREATE TABLE tbbmp (
    id integer NOT NULL,
    tbdocumentobase_id integer,
    coddestino character varying(20),
    localdestino character varying(120),
    transferencias character varying(80),
    baixas character varying(80),
    alteracoes character varying(80),
    observacao text,
    dtrecebimento date
);


ALTER TABLE documentos.tbbmp OWNER TO admin;

--
-- TOC entry 253 (class 1259 OID 102710)
-- Name: tbbmp_id_seq; Type: SEQUENCE; Schema: documentos; Owner: admin
--

CREATE SEQUENCE tbbmp_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE documentos.tbbmp_id_seq OWNER TO admin;

--
-- TOC entry 2515 (class 0 OID 0)
-- Dependencies: 253
-- Name: tbbmp_id_seq; Type: SEQUENCE OWNED BY; Schema: documentos; Owner: admin
--

ALTER SEQUENCE tbbmp_id_seq OWNED BY tbbmp.id;


--
-- TOC entry 258 (class 1259 OID 102746)
-- Name: tbbmp_patrimonio; Type: TABLE; Schema: documentos; Owner: admin; Tablespace: 
--

CREATE TABLE tbbmp_patrimonio (
    id integer NOT NULL,
    tbbmp_id integer
);


ALTER TABLE documentos.tbbmp_patrimonio OWNER TO admin;

--
-- TOC entry 257 (class 1259 OID 102744)
-- Name: tbbmp_patrimonio_id_seq; Type: SEQUENCE; Schema: documentos; Owner: admin
--

CREATE SEQUENCE tbbmp_patrimonio_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE documentos.tbbmp_patrimonio_id_seq OWNER TO admin;

--
-- TOC entry 2516 (class 0 OID 0)
-- Dependencies: 257
-- Name: tbbmp_patrimonio_id_seq; Type: SEQUENCE OWNED BY; Schema: documentos; Owner: admin
--

ALTER SEQUENCE tbbmp_patrimonio_id_seq OWNED BY tbbmp_patrimonio.id;


--
-- TOC entry 256 (class 1259 OID 102725)
-- Name: tbdiaria; Type: TABLE; Schema: documentos; Owner: admin; Tablespace: 
--

CREATE TABLE tbdiaria (
    id integer NOT NULL,
    tbdocumentobase_id integer
);


ALTER TABLE documentos.tbdiaria OWNER TO admin;

--
-- TOC entry 255 (class 1259 OID 102723)
-- Name: tbdiaria_id_seq; Type: SEQUENCE; Schema: documentos; Owner: admin
--

CREATE SEQUENCE tbdiaria_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE documentos.tbdiaria_id_seq OWNER TO admin;

--
-- TOC entry 2517 (class 0 OID 0)
-- Dependencies: 255
-- Name: tbdiaria_id_seq; Type: SEQUENCE OWNED BY; Schema: documentos; Owner: admin
--

ALTER SEQUENCE tbdiaria_id_seq OWNED BY tbdiaria.id;


--
-- TOC entry 246 (class 1259 OID 102643)
-- Name: tbmemorando; Type: TABLE; Schema: documentos; Owner: admin; Tablespace: 
--

CREATE TABLE tbmemorando (
    tbdocumentobase_id integer NOT NULL,
    nmassunto character varying(100) NOT NULL,
    nmlocal character varying(100) NOT NULL,
    nmremetente character varying(100) NOT NULL,
    nmdestinatario character varying(100) NOT NULL,
    nmmensagem text NOT NULL,
    id integer NOT NULL,
    nrsisdoc character varying(20),
    nrsufixosisdoc character varying(20),
    blcircular boolean
);


ALTER TABLE documentos.tbmemorando OWNER TO admin;

--
-- TOC entry 245 (class 1259 OID 102641)
-- Name: tbmemorando_id_seq; Type: SEQUENCE; Schema: documentos; Owner: admin
--

CREATE SEQUENCE tbmemorando_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE documentos.tbmemorando_id_seq OWNER TO admin;

--
-- TOC entry 2518 (class 0 OID 0)
-- Dependencies: 245
-- Name: tbmemorando_id_seq; Type: SEQUENCE OWNED BY; Schema: documentos; Owner: admin
--

ALTER SEQUENCE tbmemorando_id_seq OWNED BY tbmemorando.id;


--
-- TOC entry 262 (class 1259 OID 102824)
-- Name: tboficio; Type: TABLE; Schema: documentos; Owner: admin; Tablespace: 
--

CREATE TABLE tboficio (
    tbdocumentobase_id integer NOT NULL,
    nrsisdoc character varying(20),
    nrsufixosisdoc character varying(20),
    nmtratamento character varying(80) NOT NULL,
    nmdestinatario character varying(100) NOT NULL,
    nmcargo character varying(80) NOT NULL,
    nmempresa character varying(80) NOT NULL,
    nmendereco text NOT NULL,
    nrcep character varying(10) NOT NULL,
    nmcidade character varying(100) NOT NULL,
    nrtelefone character varying(20) NOT NULL,
    nmemail text NOT NULL,
    nmassunto character varying(100) NOT NULL,
    nmmensagem text NOT NULL,
    blcircular boolean,
    id integer NOT NULL,
    nmlocal character varying(100)
);


ALTER TABLE documentos.tboficio OWNER TO admin;

--
-- TOC entry 261 (class 1259 OID 102822)
-- Name: tboficio_id_seq; Type: SEQUENCE; Schema: documentos; Owner: admin
--

CREATE SEQUENCE tboficio_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE documentos.tboficio_id_seq OWNER TO admin;

--
-- TOC entry 2519 (class 0 OID 0)
-- Dependencies: 261
-- Name: tboficio_id_seq; Type: SEQUENCE OWNED BY; Schema: documentos; Owner: admin
--

ALTER SEQUENCE tboficio_id_seq OWNED BY tboficio.id;


--
-- TOC entry 248 (class 1259 OID 102673)
-- Name: tbrme; Type: TABLE; Schema: documentos; Owner: admin; Tablespace: 
--

CREATE TABLE tbrme (
    id integer NOT NULL,
    tbdocumentobase_id integer,
    dtperiodo date,
    nrordem integer,
    solicitante character varying(120)
);


ALTER TABLE documentos.tbrme OWNER TO admin;

--
-- TOC entry 247 (class 1259 OID 102671)
-- Name: tbrme_id_seq; Type: SEQUENCE; Schema: documentos; Owner: admin
--

CREATE SEQUENCE tbrme_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE documentos.tbrme_id_seq OWNER TO admin;

--
-- TOC entry 2520 (class 0 OID 0)
-- Dependencies: 247
-- Name: tbrme_id_seq; Type: SEQUENCE OWNED BY; Schema: documentos; Owner: admin
--

ALTER SEQUENCE tbrme_id_seq OWNED BY tbrme.id;


--
-- TOC entry 260 (class 1259 OID 102759)
-- Name: tbrme_material; Type: TABLE; Schema: documentos; Owner: admin; Tablespace: 
--

CREATE TABLE tbrme_material (
    id integer NOT NULL,
    tbrme_id integer
);


ALTER TABLE documentos.tbrme_material OWNER TO admin;

--
-- TOC entry 259 (class 1259 OID 102757)
-- Name: tbrme_material_id_seq; Type: SEQUENCE; Schema: documentos; Owner: admin
--

CREATE SEQUENCE tbrme_material_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE documentos.tbrme_material_id_seq OWNER TO admin;

--
-- TOC entry 2521 (class 0 OID 0)
-- Dependencies: 259
-- Name: tbrme_material_id_seq; Type: SEQUENCE OWNED BY; Schema: documentos; Owner: admin
--

ALTER SEQUENCE tbrme_material_id_seq OWNED BY tbrme_material.id;


--
-- TOC entry 252 (class 1259 OID 102699)
-- Name: tbrv; Type: TABLE; Schema: documentos; Owner: admin; Tablespace: 
--

CREATE TABLE tbrv (
    id integer NOT NULL,
    tbdocumentobase_id integer,
    dtinicioservicos timestamp without time zone,
    objetivo text,
    destino character varying(120),
    tempodias integer,
    motorista character varying(120),
    usuarios text,
    localviatura character varying(80),
    dtsolicitante date,
    dtautorizado date,
    veiculo character varying(80),
    placa character varying(20)
);


ALTER TABLE documentos.tbrv OWNER TO admin;

--
-- TOC entry 251 (class 1259 OID 102697)
-- Name: tbrv_id_seq; Type: SEQUENCE; Schema: documentos; Owner: admin
--

CREATE SEQUENCE tbrv_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE documentos.tbrv_id_seq OWNER TO admin;

--
-- TOC entry 2522 (class 0 OID 0)
-- Dependencies: 251
-- Name: tbrv_id_seq; Type: SEQUENCE OWNED BY; Schema: documentos; Owner: admin
--

ALTER SEQUENCE tbrv_id_seq OWNED BY tbrv.id;


--
-- TOC entry 250 (class 1259 OID 102686)
-- Name: tbtru; Type: TABLE; Schema: documentos; Owner: admin; Tablespace: 
--

CREATE TABLE tbtru (
    id integer NOT NULL,
    tbdocumentobase_id integer,
    nmlocalidade character varying(80),
    nome character varying(80),
    nrsiape character varying(20),
    nrcpf character varying(11),
    endereco text,
    justificativa text,
    dtiniciocedencia date,
    dtfimcedencia date,
    declaracao text
);


ALTER TABLE documentos.tbtru OWNER TO admin;

--
-- TOC entry 249 (class 1259 OID 102684)
-- Name: tbtru_id_seq; Type: SEQUENCE; Schema: documentos; Owner: admin
--

CREATE SEQUENCE tbtru_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE documentos.tbtru_id_seq OWNER TO admin;

--
-- TOC entry 2523 (class 0 OID 0)
-- Dependencies: 249
-- Name: tbtru_id_seq; Type: SEQUENCE OWNED BY; Schema: documentos; Owner: admin
--

ALTER SEQUENCE tbtru_id_seq OWNED BY tbtru.id;


SET search_path = public, pg_catalog;

--
-- TOC entry 169 (class 1259 OID 101407)
-- Name: auth_group; Type: TABLE; Schema: public; Owner: admin; Tablespace: 
--

CREATE TABLE auth_group (
    id integer NOT NULL,
    name character varying(80) NOT NULL,
    tbdivisao_id integer NOT NULL
);


ALTER TABLE public.auth_group OWNER TO admin;

--
-- TOC entry 170 (class 1259 OID 101410)
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
-- TOC entry 2524 (class 0 OID 0)
-- Dependencies: 170
-- Name: auth_group_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE auth_group_id_seq OWNED BY auth_group.id;


--
-- TOC entry 171 (class 1259 OID 101412)
-- Name: auth_group_permissions; Type: TABLE; Schema: public; Owner: admin; Tablespace: 
--

CREATE TABLE auth_group_permissions (
    id integer NOT NULL,
    group_id integer NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE public.auth_group_permissions OWNER TO admin;

--
-- TOC entry 172 (class 1259 OID 101415)
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
-- TOC entry 2525 (class 0 OID 0)
-- Dependencies: 172
-- Name: auth_group_permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE auth_group_permissions_id_seq OWNED BY auth_group_permissions.id;


--
-- TOC entry 173 (class 1259 OID 101417)
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
-- TOC entry 174 (class 1259 OID 101420)
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
-- TOC entry 2526 (class 0 OID 0)
-- Dependencies: 174
-- Name: auth_permission_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE auth_permission_id_seq OWNED BY auth_permission.id;


--
-- TOC entry 175 (class 1259 OID 101422)
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
-- TOC entry 176 (class 1259 OID 101425)
-- Name: auth_user_groups; Type: TABLE; Schema: public; Owner: admin; Tablespace: 
--

CREATE TABLE auth_user_groups (
    id integer NOT NULL,
    user_id integer NOT NULL,
    group_id integer NOT NULL
);


ALTER TABLE public.auth_user_groups OWNER TO admin;

--
-- TOC entry 177 (class 1259 OID 101428)
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
-- TOC entry 2527 (class 0 OID 0)
-- Dependencies: 177
-- Name: auth_user_groups_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE auth_user_groups_id_seq OWNED BY auth_user_groups.id;


--
-- TOC entry 178 (class 1259 OID 101430)
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
-- TOC entry 2528 (class 0 OID 0)
-- Dependencies: 178
-- Name: auth_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE auth_user_id_seq OWNED BY auth_user.id;


--
-- TOC entry 179 (class 1259 OID 101432)
-- Name: auth_user_user_permissions; Type: TABLE; Schema: public; Owner: admin; Tablespace: 
--

CREATE TABLE auth_user_user_permissions (
    id integer NOT NULL,
    user_id integer NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE public.auth_user_user_permissions OWNER TO admin;

--
-- TOC entry 180 (class 1259 OID 101435)
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
-- TOC entry 2529 (class 0 OID 0)
-- Dependencies: 180
-- Name: auth_user_user_permissions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE auth_user_user_permissions_id_seq OWNED BY auth_user_user_permissions.id;


--
-- TOC entry 181 (class 1259 OID 101437)
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
-- TOC entry 182 (class 1259 OID 101443)
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
-- TOC entry 183 (class 1259 OID 101446)
-- Name: django_session; Type: TABLE; Schema: public; Owner: admin; Tablespace: 
--

CREATE TABLE django_session (
    session_key character varying(40) NOT NULL,
    session_data text NOT NULL,
    expire_date timestamp with time zone NOT NULL
);


ALTER TABLE public.django_session OWNER TO admin;

--
-- TOC entry 184 (class 1259 OID 101452)
-- Name: django_site; Type: TABLE; Schema: public; Owner: admin; Tablespace: 
--

CREATE TABLE django_site (
    id integer NOT NULL,
    domain character varying(100) NOT NULL,
    name character varying(50) NOT NULL
);


ALTER TABLE public.django_site OWNER TO admin;

--
-- TOC entry 185 (class 1259 OID 101455)
-- Name: tbcaixa; Type: TABLE; Schema: public; Owner: admin; Tablespace: 
--

CREATE TABLE tbcaixa (
    nmlocalarquivo character varying(80) NOT NULL,
    tbtipocaixa_id integer NOT NULL,
    id integer NOT NULL,
    tbdivisao_id integer
);


ALTER TABLE public.tbcaixa OWNER TO admin;

--
-- TOC entry 186 (class 1259 OID 101458)
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
-- TOC entry 2530 (class 0 OID 0)
-- Dependencies: 186
-- Name: tbcaixa_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE tbcaixa_id_seq OWNED BY tbcaixa.id;


--
-- TOC entry 187 (class 1259 OID 101460)
-- Name: tbclassificacaoprocesso; Type: TABLE; Schema: public; Owner: admin; Tablespace: 
--

CREATE TABLE tbclassificacaoprocesso (
    nmclassificacao character varying(80) NOT NULL,
    tbdivisao_id integer,
    id integer NOT NULL
);


ALTER TABLE public.tbclassificacaoprocesso OWNER TO admin;

--
-- TOC entry 188 (class 1259 OID 101463)
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
-- TOC entry 2531 (class 0 OID 0)
-- Dependencies: 188
-- Name: tbclassificacaoprocesso_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE tbclassificacaoprocesso_id_seq OWNED BY tbclassificacaoprocesso.id;


--
-- TOC entry 189 (class 1259 OID 101465)
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
-- TOC entry 190 (class 1259 OID 101468)
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
-- TOC entry 2532 (class 0 OID 0)
-- Dependencies: 190
-- Name: tbcontrato_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE tbcontrato_id_seq OWNED BY tbcontrato.id;


--
-- TOC entry 191 (class 1259 OID 101470)
-- Name: tbdivisao; Type: TABLE; Schema: public; Owner: admin; Tablespace: 
--

CREATE TABLE tbdivisao (
    nmdivisao character varying(80) NOT NULL,
    dsdivisao text NOT NULL,
    tbuf_id integer,
    id integer NOT NULL,
    nrclasse smallint
);


ALTER TABLE public.tbdivisao OWNER TO admin;

--
-- TOC entry 192 (class 1259 OID 101476)
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
-- TOC entry 2533 (class 0 OID 0)
-- Dependencies: 192
-- Name: tbdivisao_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE tbdivisao_id_seq OWNED BY tbdivisao.id;


--
-- TOC entry 193 (class 1259 OID 101478)
-- Name: tbdocumentobase; Type: TABLE; Schema: public; Owner: admin; Tablespace: 
--

CREATE TABLE tbdocumentobase (
    nmdocumento character varying(80) NOT NULL,
    tbtipodocumento_id integer NOT NULL,
    dtcadastrodocumento timestamp without time zone,
    auth_user_id integer NOT NULL,
    tbdivisao_id integer NOT NULL,
    id integer NOT NULL,
    dtdocumento timestamp without time zone
);


ALTER TABLE public.tbdocumentobase OWNER TO admin;

--
-- TOC entry 194 (class 1259 OID 101484)
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
-- TOC entry 2534 (class 0 OID 0)
-- Dependencies: 194
-- Name: tbdocumentobase_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE tbdocumentobase_id_seq OWNED BY tbdocumentobase.id;


--
-- TOC entry 195 (class 1259 OID 101486)
-- Name: tbdocumentomemorando; Type: TABLE; Schema: public; Owner: admin; Tablespace: 
--

CREATE TABLE tbdocumentomemorando (
    tbdocumentobase_id integer NOT NULL,
    nmassunto character varying(100) NOT NULL,
    nmlocal character varying(100) NOT NULL,
    nmremetente character varying(100) NOT NULL,
    nmdestinatario character varying(100) NOT NULL,
    nmmensagem text NOT NULL,
    id integer NOT NULL,
    nrsisdoc character varying(20),
    nrsufixosisdoc character varying(20),
    blcircular boolean
);


ALTER TABLE public.tbdocumentomemorando OWNER TO admin;

--
-- TOC entry 196 (class 1259 OID 101492)
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
-- TOC entry 2535 (class 0 OID 0)
-- Dependencies: 196
-- Name: tbdocumentomemorando_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE tbdocumentomemorando_id_seq OWNED BY tbdocumentomemorando.id;


--
-- TOC entry 197 (class 1259 OID 101494)
-- Name: tbdocumentoservidor; Type: TABLE; Schema: public; Owner: admin; Tablespace: 
--

CREATE TABLE tbdocumentoservidor (
    tbdocumentobase_id integer NOT NULL,
    tbservidor_id integer NOT NULL,
    id integer NOT NULL
);


ALTER TABLE public.tbdocumentoservidor OWNER TO admin;

--
-- TOC entry 198 (class 1259 OID 101497)
-- Name: tbdocumentoservidor_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE tbdocumentoservidor_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.tbdocumentoservidor_id_seq OWNER TO admin;

--
-- TOC entry 2536 (class 0 OID 0)
-- Dependencies: 198
-- Name: tbdocumentoservidor_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE tbdocumentoservidor_id_seq OWNED BY tbdocumentoservidor.id;


--
-- TOC entry 199 (class 1259 OID 101499)
-- Name: tbferias; Type: TABLE; Schema: public; Owner: admin; Tablespace: 
--

CREATE TABLE tbferias (
    id integer NOT NULL,
    tbservidor_id integer NOT NULL,
    "nrAno" integer NOT NULL,
    "dtInicio1" date NOT NULL,
    "nrDias1" integer NOT NULL,
    "dtInicio2" timestamp with time zone,
    "nrDias2" integer,
    "dtInicio3" date,
    "nrDias3" integer,
    "stAntecipa" boolean,
    "stDecimoTerceiro" boolean,
    "stSituacao1_id" integer,
    "stSituacao2_id" integer,
    "stSituacao3_id" integer,
    "dsObservacao" text
);


ALTER TABLE public.tbferias OWNER TO admin;

--
-- TOC entry 200 (class 1259 OID 101505)
-- Name: tbferias_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE tbferias_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.tbferias_id_seq OWNER TO admin;

--
-- TOC entry 2537 (class 0 OID 0)
-- Dependencies: 200
-- Name: tbferias_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE tbferias_id_seq OWNED BY tbferias.id;


--
-- TOC entry 201 (class 1259 OID 101507)
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
-- TOC entry 202 (class 1259 OID 101510)
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
-- TOC entry 2538 (class 0 OID 0)
-- Dependencies: 202
-- Name: tbgleba_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE tbgleba_id_seq OWNED BY tbgleba.id;


--
-- TOC entry 203 (class 1259 OID 101512)
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
-- TOC entry 204 (class 1259 OID 101515)
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
-- TOC entry 2539 (class 0 OID 0)
-- Dependencies: 204
-- Name: tbmovimentacao_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE tbmovimentacao_id_seq OWNED BY tbmovimentacao.id;


--
-- TOC entry 205 (class 1259 OID 101517)
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
-- TOC entry 206 (class 1259 OID 101520)
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
-- TOC entry 2540 (class 0 OID 0)
-- Dependencies: 206
-- Name: tbmunicipio_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE tbmunicipio_id_seq OWNED BY tbmunicipio.id;


--
-- TOC entry 207 (class 1259 OID 101522)
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
-- TOC entry 208 (class 1259 OID 101528)
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
-- TOC entry 2541 (class 0 OID 0)
-- Dependencies: 208
-- Name: tbpecastecnicas_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE tbpecastecnicas_id_seq OWNED BY tbpecastecnicas.id;


--
-- TOC entry 209 (class 1259 OID 101530)
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
-- TOC entry 210 (class 1259 OID 101536)
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
-- TOC entry 2542 (class 0 OID 0)
-- Dependencies: 210
-- Name: tbpendencia_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE tbpendencia_id_seq OWNED BY tbpendencia.id;


--
-- TOC entry 211 (class 1259 OID 101538)
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
-- TOC entry 212 (class 1259 OID 101544)
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
-- TOC entry 2543 (class 0 OID 0)
-- Dependencies: 212
-- Name: tbpregao_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE tbpregao_id_seq OWNED BY tbpregao.id;


--
-- TOC entry 213 (class 1259 OID 101546)
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
-- TOC entry 214 (class 1259 OID 101549)
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
-- TOC entry 2544 (class 0 OID 0)
-- Dependencies: 214
-- Name: tbprocessobase_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE tbprocessobase_id_seq OWNED BY tbprocessobase.id;


--
-- TOC entry 215 (class 1259 OID 101551)
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
    id integer NOT NULL,
    stcertquitacao boolean,
    stcertliberacao boolean
);


ALTER TABLE public.tbprocessoclausula OWNER TO admin;

--
-- TOC entry 216 (class 1259 OID 101557)
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
-- TOC entry 2545 (class 0 OID 0)
-- Dependencies: 216
-- Name: tbprocessoclausula_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE tbprocessoclausula_id_seq OWNED BY tbprocessoclausula.id;


--
-- TOC entry 217 (class 1259 OID 101559)
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
-- TOC entry 218 (class 1259 OID 101562)
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
-- TOC entry 2546 (class 0 OID 0)
-- Dependencies: 218
-- Name: tbprocessorural_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE tbprocessorural_id_seq OWNED BY tbprocessorural.id;


--
-- TOC entry 219 (class 1259 OID 101564)
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
-- TOC entry 220 (class 1259 OID 101567)
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
-- TOC entry 2547 (class 0 OID 0)
-- Dependencies: 220
-- Name: tbprocessosanexos_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE tbprocessosanexos_id_seq OWNED BY tbprocessosanexos.id;


--
-- TOC entry 221 (class 1259 OID 101569)
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
-- TOC entry 222 (class 1259 OID 101572)
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
-- TOC entry 2548 (class 0 OID 0)
-- Dependencies: 222
-- Name: tbprocessourbano_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE tbprocessourbano_id_seq OWNED BY tbprocessourbano.id;


--
-- TOC entry 223 (class 1259 OID 101574)
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
    id integer NOT NULL,
    nmcontrato character varying(20),
    dtnascimento date
);


ALTER TABLE public.tbservidor OWNER TO admin;

--
-- TOC entry 224 (class 1259 OID 101580)
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
-- TOC entry 2549 (class 0 OID 0)
-- Dependencies: 224
-- Name: tbservidor_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE tbservidor_id_seq OWNED BY tbservidor.id;


--
-- TOC entry 225 (class 1259 OID 101582)
-- Name: tbsituacao; Type: TABLE; Schema: public; Owner: admin; Tablespace: 
--

CREATE TABLE tbsituacao (
    id integer NOT NULL,
    "cdTabela" character varying(30) NOT NULL,
    "dsSituacao" character varying(50) NOT NULL
);


ALTER TABLE public.tbsituacao OWNER TO admin;

--
-- TOC entry 226 (class 1259 OID 101585)
-- Name: tbsituacao_id_seq; Type: SEQUENCE; Schema: public; Owner: admin
--

CREATE SEQUENCE tbsituacao_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.tbsituacao_id_seq OWNER TO admin;

--
-- TOC entry 2550 (class 0 OID 0)
-- Dependencies: 226
-- Name: tbsituacao_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE tbsituacao_id_seq OWNED BY tbsituacao.id;


--
-- TOC entry 227 (class 1259 OID 101587)
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
-- TOC entry 228 (class 1259 OID 101593)
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
-- TOC entry 2551 (class 0 OID 0)
-- Dependencies: 228
-- Name: tbsituacaogeo_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE tbsituacaogeo_id_seq OWNED BY tbsituacaogeo.id;


--
-- TOC entry 229 (class 1259 OID 101595)
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
-- TOC entry 230 (class 1259 OID 101601)
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
-- TOC entry 2552 (class 0 OID 0)
-- Dependencies: 230
-- Name: tbsituacaoprocesso_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE tbsituacaoprocesso_id_seq OWNED BY tbsituacaoprocesso.id;


--
-- TOC entry 231 (class 1259 OID 101603)
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
-- TOC entry 232 (class 1259 OID 101606)
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
-- TOC entry 2553 (class 0 OID 0)
-- Dependencies: 232
-- Name: tbstatuspendencia_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE tbstatuspendencia_id_seq OWNED BY tbstatuspendencia.id;


--
-- TOC entry 233 (class 1259 OID 101608)
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
-- TOC entry 234 (class 1259 OID 101611)
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
-- TOC entry 2554 (class 0 OID 0)
-- Dependencies: 234
-- Name: tbsubarea_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE tbsubarea_id_seq OWNED BY tbsubarea.id;


--
-- TOC entry 235 (class 1259 OID 101613)
-- Name: tbtipocaixa; Type: TABLE; Schema: public; Owner: admin; Tablespace: 
--

CREATE TABLE tbtipocaixa (
    nmtipocaixa character varying(80) NOT NULL,
    desctipocaixa text NOT NULL,
    id integer NOT NULL
);


ALTER TABLE public.tbtipocaixa OWNER TO admin;

--
-- TOC entry 236 (class 1259 OID 101619)
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
-- TOC entry 2555 (class 0 OID 0)
-- Dependencies: 236
-- Name: tbtipocaixa_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE tbtipocaixa_id_seq OWNED BY tbtipocaixa.id;


--
-- TOC entry 237 (class 1259 OID 101621)
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
-- TOC entry 238 (class 1259 OID 101627)
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
-- TOC entry 2556 (class 0 OID 0)
-- Dependencies: 238
-- Name: tbtipodocumento_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE tbtipodocumento_id_seq OWNED BY tbtipodocumento.id;


--
-- TOC entry 239 (class 1259 OID 101629)
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
-- TOC entry 240 (class 1259 OID 101632)
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
-- TOC entry 2557 (class 0 OID 0)
-- Dependencies: 240
-- Name: tbtipopendencia_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE tbtipopendencia_id_seq OWNED BY tbtipopendencia.id;


--
-- TOC entry 241 (class 1259 OID 101634)
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
-- TOC entry 242 (class 1259 OID 101637)
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
-- TOC entry 2558 (class 0 OID 0)
-- Dependencies: 242
-- Name: tbtipoprocesso_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE tbtipoprocesso_id_seq OWNED BY tbtipoprocesso.id;


--
-- TOC entry 243 (class 1259 OID 101639)
-- Name: tbuf; Type: TABLE; Schema: public; Owner: admin; Tablespace: 
--

CREATE TABLE tbuf (
    sigla character varying(2) NOT NULL,
    nmuf character varying(50) NOT NULL,
    id integer NOT NULL
);


ALTER TABLE public.tbuf OWNER TO admin;

--
-- TOC entry 244 (class 1259 OID 101642)
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
-- TOC entry 2559 (class 0 OID 0)
-- Dependencies: 244
-- Name: tbuf_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE tbuf_id_seq OWNED BY tbuf.id;


SET search_path = documentos, pg_catalog;

--
-- TOC entry 2256 (class 2604 OID 102715)
-- Name: id; Type: DEFAULT; Schema: documentos; Owner: admin
--

ALTER TABLE ONLY tbbmp ALTER COLUMN id SET DEFAULT nextval('tbbmp_id_seq'::regclass);


--
-- TOC entry 2258 (class 2604 OID 102749)
-- Name: id; Type: DEFAULT; Schema: documentos; Owner: admin
--

ALTER TABLE ONLY tbbmp_patrimonio ALTER COLUMN id SET DEFAULT nextval('tbbmp_patrimonio_id_seq'::regclass);


--
-- TOC entry 2257 (class 2604 OID 102728)
-- Name: id; Type: DEFAULT; Schema: documentos; Owner: admin
--

ALTER TABLE ONLY tbdiaria ALTER COLUMN id SET DEFAULT nextval('tbdiaria_id_seq'::regclass);


--
-- TOC entry 2252 (class 2604 OID 102646)
-- Name: id; Type: DEFAULT; Schema: documentos; Owner: admin
--

ALTER TABLE ONLY tbmemorando ALTER COLUMN id SET DEFAULT nextval('tbmemorando_id_seq'::regclass);


--
-- TOC entry 2260 (class 2604 OID 102827)
-- Name: id; Type: DEFAULT; Schema: documentos; Owner: admin
--

ALTER TABLE ONLY tboficio ALTER COLUMN id SET DEFAULT nextval('tboficio_id_seq'::regclass);


--
-- TOC entry 2253 (class 2604 OID 102676)
-- Name: id; Type: DEFAULT; Schema: documentos; Owner: admin
--

ALTER TABLE ONLY tbrme ALTER COLUMN id SET DEFAULT nextval('tbrme_id_seq'::regclass);


--
-- TOC entry 2259 (class 2604 OID 102762)
-- Name: id; Type: DEFAULT; Schema: documentos; Owner: admin
--

ALTER TABLE ONLY tbrme_material ALTER COLUMN id SET DEFAULT nextval('tbrme_material_id_seq'::regclass);


--
-- TOC entry 2255 (class 2604 OID 102702)
-- Name: id; Type: DEFAULT; Schema: documentos; Owner: admin
--

ALTER TABLE ONLY tbrv ALTER COLUMN id SET DEFAULT nextval('tbrv_id_seq'::regclass);


--
-- TOC entry 2254 (class 2604 OID 102689)
-- Name: id; Type: DEFAULT; Schema: documentos; Owner: admin
--

ALTER TABLE ONLY tbtru ALTER COLUMN id SET DEFAULT nextval('tbtru_id_seq'::regclass);


SET search_path = public, pg_catalog;

--
-- TOC entry 2216 (class 2604 OID 101644)
-- Name: id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY auth_group ALTER COLUMN id SET DEFAULT nextval('auth_group_id_seq'::regclass);


--
-- TOC entry 2217 (class 2604 OID 101645)
-- Name: id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY auth_group_permissions ALTER COLUMN id SET DEFAULT nextval('auth_group_permissions_id_seq'::regclass);


--
-- TOC entry 2218 (class 2604 OID 101646)
-- Name: id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY auth_permission ALTER COLUMN id SET DEFAULT nextval('auth_permission_id_seq'::regclass);


--
-- TOC entry 2219 (class 2604 OID 101647)
-- Name: id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY auth_user ALTER COLUMN id SET DEFAULT nextval('auth_user_id_seq'::regclass);


--
-- TOC entry 2220 (class 2604 OID 101648)
-- Name: id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY auth_user_groups ALTER COLUMN id SET DEFAULT nextval('auth_user_groups_id_seq'::regclass);


--
-- TOC entry 2221 (class 2604 OID 101649)
-- Name: id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY auth_user_user_permissions ALTER COLUMN id SET DEFAULT nextval('auth_user_user_permissions_id_seq'::regclass);


--
-- TOC entry 2222 (class 2604 OID 101650)
-- Name: id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbcaixa ALTER COLUMN id SET DEFAULT nextval('tbcaixa_id_seq'::regclass);


--
-- TOC entry 2223 (class 2604 OID 101651)
-- Name: id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbclassificacaoprocesso ALTER COLUMN id SET DEFAULT nextval('tbclassificacaoprocesso_id_seq'::regclass);


--
-- TOC entry 2224 (class 2604 OID 101652)
-- Name: id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbcontrato ALTER COLUMN id SET DEFAULT nextval('tbcontrato_id_seq'::regclass);


--
-- TOC entry 2225 (class 2604 OID 101653)
-- Name: id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbdivisao ALTER COLUMN id SET DEFAULT nextval('tbdivisao_id_seq'::regclass);


--
-- TOC entry 2226 (class 2604 OID 101654)
-- Name: id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbdocumentobase ALTER COLUMN id SET DEFAULT nextval('tbdocumentobase_id_seq'::regclass);


--
-- TOC entry 2227 (class 2604 OID 101655)
-- Name: id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbdocumentomemorando ALTER COLUMN id SET DEFAULT nextval('tbdocumentomemorando_id_seq'::regclass);


--
-- TOC entry 2228 (class 2604 OID 101656)
-- Name: id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbdocumentoservidor ALTER COLUMN id SET DEFAULT nextval('tbdocumentoservidor_id_seq'::regclass);


--
-- TOC entry 2229 (class 2604 OID 101657)
-- Name: id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbferias ALTER COLUMN id SET DEFAULT nextval('tbferias_id_seq'::regclass);


--
-- TOC entry 2230 (class 2604 OID 101658)
-- Name: id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbgleba ALTER COLUMN id SET DEFAULT nextval('tbgleba_id_seq'::regclass);


--
-- TOC entry 2231 (class 2604 OID 101659)
-- Name: id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbmovimentacao ALTER COLUMN id SET DEFAULT nextval('tbmovimentacao_id_seq'::regclass);


--
-- TOC entry 2232 (class 2604 OID 101660)
-- Name: id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbmunicipio ALTER COLUMN id SET DEFAULT nextval('tbmunicipio_id_seq'::regclass);


--
-- TOC entry 2233 (class 2604 OID 101661)
-- Name: id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbpecastecnicas ALTER COLUMN id SET DEFAULT nextval('tbpecastecnicas_id_seq'::regclass);


--
-- TOC entry 2234 (class 2604 OID 101662)
-- Name: id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbpendencia ALTER COLUMN id SET DEFAULT nextval('tbpendencia_id_seq'::regclass);


--
-- TOC entry 2235 (class 2604 OID 101663)
-- Name: id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbpregao ALTER COLUMN id SET DEFAULT nextval('tbpregao_id_seq'::regclass);


--
-- TOC entry 2236 (class 2604 OID 101664)
-- Name: id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbprocessobase ALTER COLUMN id SET DEFAULT nextval('tbprocessobase_id_seq'::regclass);


--
-- TOC entry 2237 (class 2604 OID 101665)
-- Name: id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbprocessoclausula ALTER COLUMN id SET DEFAULT nextval('tbprocessoclausula_id_seq'::regclass);


--
-- TOC entry 2238 (class 2604 OID 101666)
-- Name: id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbprocessorural ALTER COLUMN id SET DEFAULT nextval('tbprocessorural_id_seq'::regclass);


--
-- TOC entry 2239 (class 2604 OID 101667)
-- Name: id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbprocessosanexos ALTER COLUMN id SET DEFAULT nextval('tbprocessosanexos_id_seq'::regclass);


--
-- TOC entry 2240 (class 2604 OID 101668)
-- Name: id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbprocessourbano ALTER COLUMN id SET DEFAULT nextval('tbprocessourbano_id_seq'::regclass);


--
-- TOC entry 2241 (class 2604 OID 101669)
-- Name: id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbservidor ALTER COLUMN id SET DEFAULT nextval('tbservidor_id_seq'::regclass);


--
-- TOC entry 2242 (class 2604 OID 101670)
-- Name: id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbsituacao ALTER COLUMN id SET DEFAULT nextval('tbsituacao_id_seq'::regclass);


--
-- TOC entry 2243 (class 2604 OID 101671)
-- Name: id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbsituacaogeo ALTER COLUMN id SET DEFAULT nextval('tbsituacaogeo_id_seq'::regclass);


--
-- TOC entry 2244 (class 2604 OID 101672)
-- Name: id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbsituacaoprocesso ALTER COLUMN id SET DEFAULT nextval('tbsituacaoprocesso_id_seq'::regclass);


--
-- TOC entry 2245 (class 2604 OID 101673)
-- Name: id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbstatuspendencia ALTER COLUMN id SET DEFAULT nextval('tbstatuspendencia_id_seq'::regclass);


--
-- TOC entry 2246 (class 2604 OID 101674)
-- Name: id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbsubarea ALTER COLUMN id SET DEFAULT nextval('tbsubarea_id_seq'::regclass);


--
-- TOC entry 2247 (class 2604 OID 101675)
-- Name: id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbtipocaixa ALTER COLUMN id SET DEFAULT nextval('tbtipocaixa_id_seq'::regclass);


--
-- TOC entry 2248 (class 2604 OID 101676)
-- Name: id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbtipodocumento ALTER COLUMN id SET DEFAULT nextval('tbtipodocumento_id_seq'::regclass);


--
-- TOC entry 2249 (class 2604 OID 101677)
-- Name: id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbtipopendencia ALTER COLUMN id SET DEFAULT nextval('tbtipopendencia_id_seq'::regclass);


--
-- TOC entry 2250 (class 2604 OID 101678)
-- Name: id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbtipoprocesso ALTER COLUMN id SET DEFAULT nextval('tbtipoprocesso_id_seq'::regclass);


--
-- TOC entry 2251 (class 2604 OID 101679)
-- Name: id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbuf ALTER COLUMN id SET DEFAULT nextval('tbuf_id_seq'::regclass);


SET search_path = documentos, pg_catalog;

--
-- TOC entry 2420 (class 2606 OID 102717)
-- Name: pk_tbbmp; Type: CONSTRAINT; Schema: documentos; Owner: admin; Tablespace: 
--

ALTER TABLE ONLY tbbmp
    ADD CONSTRAINT pk_tbbmp PRIMARY KEY (id);


--
-- TOC entry 2424 (class 2606 OID 102751)
-- Name: pk_tbbmp_patrimonio; Type: CONSTRAINT; Schema: documentos; Owner: admin; Tablespace: 
--

ALTER TABLE ONLY tbbmp_patrimonio
    ADD CONSTRAINT pk_tbbmp_patrimonio PRIMARY KEY (id);


--
-- TOC entry 2422 (class 2606 OID 102730)
-- Name: pk_tbdiaria; Type: CONSTRAINT; Schema: documentos; Owner: admin; Tablespace: 
--

ALTER TABLE ONLY tbdiaria
    ADD CONSTRAINT pk_tbdiaria PRIMARY KEY (id);


--
-- TOC entry 2414 (class 2606 OID 102678)
-- Name: pk_tbrme; Type: CONSTRAINT; Schema: documentos; Owner: admin; Tablespace: 
--

ALTER TABLE ONLY tbrme
    ADD CONSTRAINT pk_tbrme PRIMARY KEY (id);


--
-- TOC entry 2426 (class 2606 OID 102764)
-- Name: pk_tbrme_material; Type: CONSTRAINT; Schema: documentos; Owner: admin; Tablespace: 
--

ALTER TABLE ONLY tbrme_material
    ADD CONSTRAINT pk_tbrme_material PRIMARY KEY (id);


--
-- TOC entry 2418 (class 2606 OID 102704)
-- Name: pk_tbrv; Type: CONSTRAINT; Schema: documentos; Owner: admin; Tablespace: 
--

ALTER TABLE ONLY tbrv
    ADD CONSTRAINT pk_tbrv PRIMARY KEY (id);


--
-- TOC entry 2416 (class 2606 OID 102691)
-- Name: pk_tbtru; Type: CONSTRAINT; Schema: documentos; Owner: admin; Tablespace: 
--

ALTER TABLE ONLY tbtru
    ADD CONSTRAINT pk_tbtru PRIMARY KEY (id);


--
-- TOC entry 2411 (class 2606 OID 102651)
-- Name: tbmemorando_pkey; Type: CONSTRAINT; Schema: documentos; Owner: admin; Tablespace: 
--

ALTER TABLE ONLY tbmemorando
    ADD CONSTRAINT tbmemorando_pkey PRIMARY KEY (id);


--
-- TOC entry 2428 (class 2606 OID 102832)
-- Name: tboficio_pkey; Type: CONSTRAINT; Schema: documentos; Owner: admin; Tablespace: 
--

ALTER TABLE ONLY tboficio
    ADD CONSTRAINT tboficio_pkey PRIMARY KEY (id);


SET search_path = public, pg_catalog;

--
-- TOC entry 2262 (class 2606 OID 101740)
-- Name: auth_group_name_key; Type: CONSTRAINT; Schema: public; Owner: admin; Tablespace: 
--

ALTER TABLE ONLY auth_group
    ADD CONSTRAINT auth_group_name_key UNIQUE (name);


--
-- TOC entry 2270 (class 2606 OID 101742)
-- Name: auth_group_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: admin; Tablespace: 
--

ALTER TABLE ONLY auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_pkey PRIMARY KEY (id);


--
-- TOC entry 2265 (class 2606 OID 101744)
-- Name: auth_group_pkey; Type: CONSTRAINT; Schema: public; Owner: admin; Tablespace: 
--

ALTER TABLE ONLY auth_group
    ADD CONSTRAINT auth_group_pkey PRIMARY KEY (id);


--
-- TOC entry 2273 (class 2606 OID 101746)
-- Name: auth_permission_pkey; Type: CONSTRAINT; Schema: public; Owner: admin; Tablespace: 
--

ALTER TABLE ONLY auth_permission
    ADD CONSTRAINT auth_permission_pkey PRIMARY KEY (id);


--
-- TOC entry 2282 (class 2606 OID 101748)
-- Name: auth_user_groups_pkey; Type: CONSTRAINT; Schema: public; Owner: admin; Tablespace: 
--

ALTER TABLE ONLY auth_user_groups
    ADD CONSTRAINT auth_user_groups_pkey PRIMARY KEY (id);


--
-- TOC entry 2275 (class 2606 OID 101750)
-- Name: auth_user_pkey; Type: CONSTRAINT; Schema: public; Owner: admin; Tablespace: 
--

ALTER TABLE ONLY auth_user
    ADD CONSTRAINT auth_user_pkey PRIMARY KEY (id);


--
-- TOC entry 2286 (class 2606 OID 101752)
-- Name: auth_user_user_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: admin; Tablespace: 
--

ALTER TABLE ONLY auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_pkey PRIMARY KEY (id);


--
-- TOC entry 2278 (class 2606 OID 101754)
-- Name: auth_user_username_key; Type: CONSTRAINT; Schema: public; Owner: admin; Tablespace: 
--

ALTER TABLE ONLY auth_user
    ADD CONSTRAINT auth_user_username_key UNIQUE (username);


--
-- TOC entry 2290 (class 2606 OID 101756)
-- Name: django_admin_log_pkey; Type: CONSTRAINT; Schema: public; Owner: admin; Tablespace: 
--

ALTER TABLE ONLY django_admin_log
    ADD CONSTRAINT django_admin_log_pkey PRIMARY KEY (id);


--
-- TOC entry 2293 (class 2606 OID 101758)
-- Name: django_content_type_pkey; Type: CONSTRAINT; Schema: public; Owner: admin; Tablespace: 
--

ALTER TABLE ONLY django_content_type
    ADD CONSTRAINT django_content_type_pkey PRIMARY KEY (id);


--
-- TOC entry 2295 (class 2606 OID 101760)
-- Name: django_session_pkey; Type: CONSTRAINT; Schema: public; Owner: admin; Tablespace: 
--

ALTER TABLE ONLY django_session
    ADD CONSTRAINT django_session_pkey PRIMARY KEY (session_key);


--
-- TOC entry 2298 (class 2606 OID 101762)
-- Name: django_site_pkey; Type: CONSTRAINT; Schema: public; Owner: admin; Tablespace: 
--

ALTER TABLE ONLY django_site
    ADD CONSTRAINT django_site_pkey PRIMARY KEY (id);


--
-- TOC entry 2301 (class 2606 OID 101764)
-- Name: tbcaixa_pkey; Type: CONSTRAINT; Schema: public; Owner: admin; Tablespace: 
--

ALTER TABLE ONLY tbcaixa
    ADD CONSTRAINT tbcaixa_pkey PRIMARY KEY (id);


--
-- TOC entry 2304 (class 2606 OID 101766)
-- Name: tbclassificacaoprocesso_pkey; Type: CONSTRAINT; Schema: public; Owner: admin; Tablespace: 
--

ALTER TABLE ONLY tbclassificacaoprocesso
    ADD CONSTRAINT tbclassificacaoprocesso_pkey PRIMARY KEY (id);


--
-- TOC entry 2307 (class 2606 OID 101768)
-- Name: tbcontrato_pkey; Type: CONSTRAINT; Schema: public; Owner: admin; Tablespace: 
--

ALTER TABLE ONLY tbcontrato
    ADD CONSTRAINT tbcontrato_pkey PRIMARY KEY (id);


--
-- TOC entry 2310 (class 2606 OID 101770)
-- Name: tbdivisao_pkey; Type: CONSTRAINT; Schema: public; Owner: admin; Tablespace: 
--

ALTER TABLE ONLY tbdivisao
    ADD CONSTRAINT tbdivisao_pkey PRIMARY KEY (id);


--
-- TOC entry 2314 (class 2606 OID 101772)
-- Name: tbdocumentobase_pkey; Type: CONSTRAINT; Schema: public; Owner: admin; Tablespace: 
--

ALTER TABLE ONLY tbdocumentobase
    ADD CONSTRAINT tbdocumentobase_pkey PRIMARY KEY (id);


--
-- TOC entry 2318 (class 2606 OID 101774)
-- Name: tbdocumentomemorando_pkey; Type: CONSTRAINT; Schema: public; Owner: admin; Tablespace: 
--

ALTER TABLE ONLY tbdocumentomemorando
    ADD CONSTRAINT tbdocumentomemorando_pkey PRIMARY KEY (id);


--
-- TOC entry 2321 (class 2606 OID 101776)
-- Name: tbdocumentoservidor_pkey; Type: CONSTRAINT; Schema: public; Owner: admin; Tablespace: 
--

ALTER TABLE ONLY tbdocumentoservidor
    ADD CONSTRAINT tbdocumentoservidor_pkey PRIMARY KEY (id);


--
-- TOC entry 2323 (class 2606 OID 101778)
-- Name: tbferias_pkey; Type: CONSTRAINT; Schema: public; Owner: admin; Tablespace: 
--

ALTER TABLE ONLY tbferias
    ADD CONSTRAINT tbferias_pkey PRIMARY KEY (id);


--
-- TOC entry 2325 (class 2606 OID 101780)
-- Name: tbgleba_pkey; Type: CONSTRAINT; Schema: public; Owner: admin; Tablespace: 
--

ALTER TABLE ONLY tbgleba
    ADD CONSTRAINT tbgleba_pkey PRIMARY KEY (id);


--
-- TOC entry 2330 (class 2606 OID 101782)
-- Name: tbmovimentacao_pkey; Type: CONSTRAINT; Schema: public; Owner: admin; Tablespace: 
--

ALTER TABLE ONLY tbmovimentacao
    ADD CONSTRAINT tbmovimentacao_pkey PRIMARY KEY (id);


--
-- TOC entry 2336 (class 2606 OID 101784)
-- Name: tbmunicipio_pkey; Type: CONSTRAINT; Schema: public; Owner: admin; Tablespace: 
--

ALTER TABLE ONLY tbmunicipio
    ADD CONSTRAINT tbmunicipio_pkey PRIMARY KEY (id);


--
-- TOC entry 2338 (class 2606 OID 101786)
-- Name: tbpecastecnicas_pkey; Type: CONSTRAINT; Schema: public; Owner: admin; Tablespace: 
--

ALTER TABLE ONLY tbpecastecnicas
    ADD CONSTRAINT tbpecastecnicas_pkey PRIMARY KEY (id);


--
-- TOC entry 2345 (class 2606 OID 101788)
-- Name: tbpendencia_pkey; Type: CONSTRAINT; Schema: public; Owner: admin; Tablespace: 
--

ALTER TABLE ONLY tbpendencia
    ADD CONSTRAINT tbpendencia_pkey PRIMARY KEY (id);


--
-- TOC entry 2350 (class 2606 OID 101790)
-- Name: tbpregao_pkey; Type: CONSTRAINT; Schema: public; Owner: admin; Tablespace: 
--

ALTER TABLE ONLY tbpregao
    ADD CONSTRAINT tbpregao_pkey PRIMARY KEY (id);


--
-- TOC entry 2354 (class 2606 OID 101792)
-- Name: tbprocessobase_pkey; Type: CONSTRAINT; Schema: public; Owner: admin; Tablespace: 
--

ALTER TABLE ONLY tbprocessobase
    ADD CONSTRAINT tbprocessobase_pkey PRIMARY KEY (id);


--
-- TOC entry 2363 (class 2606 OID 101794)
-- Name: tbprocessoclausula_pkey; Type: CONSTRAINT; Schema: public; Owner: admin; Tablespace: 
--

ALTER TABLE ONLY tbprocessoclausula
    ADD CONSTRAINT tbprocessoclausula_pkey PRIMARY KEY (id);


--
-- TOC entry 2366 (class 2606 OID 101796)
-- Name: tbprocessorural_pkey; Type: CONSTRAINT; Schema: public; Owner: admin; Tablespace: 
--

ALTER TABLE ONLY tbprocessorural
    ADD CONSTRAINT tbprocessorural_pkey PRIMARY KEY (id);


--
-- TOC entry 2370 (class 2606 OID 101798)
-- Name: tbprocessosanexos_pkey; Type: CONSTRAINT; Schema: public; Owner: admin; Tablespace: 
--

ALTER TABLE ONLY tbprocessosanexos
    ADD CONSTRAINT tbprocessosanexos_pkey PRIMARY KEY (id);


--
-- TOC entry 2374 (class 2606 OID 101800)
-- Name: tbprocessourbano_pkey; Type: CONSTRAINT; Schema: public; Owner: admin; Tablespace: 
--

ALTER TABLE ONLY tbprocessourbano
    ADD CONSTRAINT tbprocessourbano_pkey PRIMARY KEY (id);


--
-- TOC entry 2380 (class 2606 OID 101802)
-- Name: tbservidor_pkey; Type: CONSTRAINT; Schema: public; Owner: admin; Tablespace: 
--

ALTER TABLE ONLY tbservidor
    ADD CONSTRAINT tbservidor_pkey PRIMARY KEY (id);


--
-- TOC entry 2383 (class 2606 OID 101804)
-- Name: tbsituacao_pkey; Type: CONSTRAINT; Schema: public; Owner: admin; Tablespace: 
--

ALTER TABLE ONLY tbsituacao
    ADD CONSTRAINT tbsituacao_pkey PRIMARY KEY (id);


--
-- TOC entry 2385 (class 2606 OID 101806)
-- Name: tbsituacaogeo_pkey; Type: CONSTRAINT; Schema: public; Owner: admin; Tablespace: 
--

ALTER TABLE ONLY tbsituacaogeo
    ADD CONSTRAINT tbsituacaogeo_pkey PRIMARY KEY (id);


--
-- TOC entry 2388 (class 2606 OID 101808)
-- Name: tbsituacaoprocesso_pkey; Type: CONSTRAINT; Schema: public; Owner: admin; Tablespace: 
--

ALTER TABLE ONLY tbsituacaoprocesso
    ADD CONSTRAINT tbsituacaoprocesso_pkey PRIMARY KEY (id);


--
-- TOC entry 2391 (class 2606 OID 101810)
-- Name: tbstatuspendencia_pkey; Type: CONSTRAINT; Schema: public; Owner: admin; Tablespace: 
--

ALTER TABLE ONLY tbstatuspendencia
    ADD CONSTRAINT tbstatuspendencia_pkey PRIMARY KEY (id);


--
-- TOC entry 2394 (class 2606 OID 101812)
-- Name: tbsubarea_pkey; Type: CONSTRAINT; Schema: public; Owner: admin; Tablespace: 
--

ALTER TABLE ONLY tbsubarea
    ADD CONSTRAINT tbsubarea_pkey PRIMARY KEY (id);


--
-- TOC entry 2397 (class 2606 OID 101814)
-- Name: tbtipocaixa_pkey; Type: CONSTRAINT; Schema: public; Owner: admin; Tablespace: 
--

ALTER TABLE ONLY tbtipocaixa
    ADD CONSTRAINT tbtipocaixa_pkey PRIMARY KEY (id);


--
-- TOC entry 2399 (class 2606 OID 101816)
-- Name: tbtipodocumento_pkey; Type: CONSTRAINT; Schema: public; Owner: admin; Tablespace: 
--

ALTER TABLE ONLY tbtipodocumento
    ADD CONSTRAINT tbtipodocumento_pkey PRIMARY KEY (id);


--
-- TOC entry 2402 (class 2606 OID 101818)
-- Name: tbtipopendencia_pkey; Type: CONSTRAINT; Schema: public; Owner: admin; Tablespace: 
--

ALTER TABLE ONLY tbtipopendencia
    ADD CONSTRAINT tbtipopendencia_pkey PRIMARY KEY (id);


--
-- TOC entry 2406 (class 2606 OID 101820)
-- Name: tbtipoprocesso_pkey; Type: CONSTRAINT; Schema: public; Owner: admin; Tablespace: 
--

ALTER TABLE ONLY tbtipoprocesso
    ADD CONSTRAINT tbtipoprocesso_pkey PRIMARY KEY (id);


--
-- TOC entry 2409 (class 2606 OID 101822)
-- Name: tbuf_pkey; Type: CONSTRAINT; Schema: public; Owner: admin; Tablespace: 
--

ALTER TABLE ONLY tbuf
    ADD CONSTRAINT tbuf_pkey PRIMARY KEY (id);


SET search_path = documentos, pg_catalog;

--
-- TOC entry 2412 (class 1259 OID 102657)
-- Name: tbmemorando_tbdocumentobase_id; Type: INDEX; Schema: documentos; Owner: admin; Tablespace: 
--

CREATE INDEX tbmemorando_tbdocumentobase_id ON tbmemorando USING btree (tbdocumentobase_id);


--
-- TOC entry 2429 (class 1259 OID 102838)
-- Name: tboficio_tbdocumentobase_id; Type: INDEX; Schema: documentos; Owner: admin; Tablespace: 
--

CREATE INDEX tboficio_tbdocumentobase_id ON tboficio USING btree (tbdocumentobase_id);


SET search_path = public, pg_catalog;

--
-- TOC entry 2263 (class 1259 OID 101823)
-- Name: auth_group_name_like; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX auth_group_name_like ON auth_group USING btree (name varchar_pattern_ops);


--
-- TOC entry 2267 (class 1259 OID 101824)
-- Name: auth_group_permissions_group_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX auth_group_permissions_group_id ON auth_group_permissions USING btree (group_id);


--
-- TOC entry 2268 (class 1259 OID 101825)
-- Name: auth_group_permissions_permission_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX auth_group_permissions_permission_id ON auth_group_permissions USING btree (permission_id);


--
-- TOC entry 2271 (class 1259 OID 101826)
-- Name: auth_permission_content_type_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX auth_permission_content_type_id ON auth_permission USING btree (content_type_id);


--
-- TOC entry 2280 (class 1259 OID 101827)
-- Name: auth_user_groups_group_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX auth_user_groups_group_id ON auth_user_groups USING btree (group_id);


--
-- TOC entry 2283 (class 1259 OID 101828)
-- Name: auth_user_groups_user_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX auth_user_groups_user_id ON auth_user_groups USING btree (user_id);


--
-- TOC entry 2276 (class 1259 OID 101829)
-- Name: auth_user_tbdivisao_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX auth_user_tbdivisao_id ON auth_user USING btree (tbdivisao_id);


--
-- TOC entry 2284 (class 1259 OID 101830)
-- Name: auth_user_user_permissions_permission_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX auth_user_user_permissions_permission_id ON auth_user_user_permissions USING btree (permission_id);


--
-- TOC entry 2287 (class 1259 OID 101831)
-- Name: auth_user_user_permissions_user_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX auth_user_user_permissions_user_id ON auth_user_user_permissions USING btree (user_id);


--
-- TOC entry 2279 (class 1259 OID 101832)
-- Name: auth_user_username_like; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX auth_user_username_like ON auth_user USING btree (username varchar_pattern_ops);


--
-- TOC entry 2288 (class 1259 OID 101833)
-- Name: django_admin_log_content_type_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX django_admin_log_content_type_id ON django_admin_log USING btree (content_type_id);


--
-- TOC entry 2291 (class 1259 OID 101834)
-- Name: django_admin_log_user_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX django_admin_log_user_id ON django_admin_log USING btree (user_id);


--
-- TOC entry 2296 (class 1259 OID 101835)
-- Name: django_session_session_key_like; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX django_session_session_key_like ON django_session USING btree (session_key varchar_pattern_ops);


--
-- TOC entry 2266 (class 1259 OID 101836)
-- Name: fki_tbdivisao_id_auth_group; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX fki_tbdivisao_id_auth_group ON auth_group USING btree (tbdivisao_id);


--
-- TOC entry 2299 (class 1259 OID 102249)
-- Name: fki_tbdivisao_tbcaixa; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX fki_tbdivisao_tbcaixa ON tbcaixa USING btree (tbdivisao_id);


--
-- TOC entry 2302 (class 1259 OID 101837)
-- Name: tbcaixa_tbtipocaixa_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX tbcaixa_tbtipocaixa_id ON tbcaixa USING btree (tbtipocaixa_id);


--
-- TOC entry 2305 (class 1259 OID 101838)
-- Name: tbclassificacaoprocesso_tbdivisao_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX tbclassificacaoprocesso_tbdivisao_id ON tbclassificacaoprocesso USING btree (tbdivisao_id);


--
-- TOC entry 2308 (class 1259 OID 101839)
-- Name: tbcontrato_tbdivisao_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX tbcontrato_tbdivisao_id ON tbcontrato USING btree (tbdivisao_id);


--
-- TOC entry 2311 (class 1259 OID 101840)
-- Name: tbdivisao_tbuf_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX tbdivisao_tbuf_id ON tbdivisao USING btree (tbuf_id);


--
-- TOC entry 2312 (class 1259 OID 101841)
-- Name: tbdocumentobase_auth_user_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX tbdocumentobase_auth_user_id ON tbdocumentobase USING btree (auth_user_id);


--
-- TOC entry 2315 (class 1259 OID 101842)
-- Name: tbdocumentobase_tbdivisao_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX tbdocumentobase_tbdivisao_id ON tbdocumentobase USING btree (tbdivisao_id);


--
-- TOC entry 2316 (class 1259 OID 101843)
-- Name: tbdocumentobase_tbtipodocumento_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX tbdocumentobase_tbtipodocumento_id ON tbdocumentobase USING btree (tbtipodocumento_id);


--
-- TOC entry 2319 (class 1259 OID 101844)
-- Name: tbdocumentomemorando_tbdocumentobase_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX tbdocumentomemorando_tbdocumentobase_id ON tbdocumentomemorando USING btree (tbdocumentobase_id);


--
-- TOC entry 2326 (class 1259 OID 101845)
-- Name: tbgleba_tbsubarea_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX tbgleba_tbsubarea_id ON tbgleba USING btree (tbsubarea_id);


--
-- TOC entry 2327 (class 1259 OID 101846)
-- Name: tbgleba_tbuf_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX tbgleba_tbuf_id ON tbgleba USING btree (tbuf_id);


--
-- TOC entry 2328 (class 1259 OID 101847)
-- Name: tbmovimentacao_auth_user_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX tbmovimentacao_auth_user_id ON tbmovimentacao USING btree (auth_user_id);


--
-- TOC entry 2331 (class 1259 OID 101848)
-- Name: tbmovimentacao_tbcaixa_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX tbmovimentacao_tbcaixa_id ON tbmovimentacao USING btree (tbcaixa_id);


--
-- TOC entry 2332 (class 1259 OID 101849)
-- Name: tbmovimentacao_tbcaixa_id_origem; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX tbmovimentacao_tbcaixa_id_origem ON tbmovimentacao USING btree (tbcaixa_id_origem);


--
-- TOC entry 2333 (class 1259 OID 101850)
-- Name: tbmovimentacao_tbprocessobase_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX tbmovimentacao_tbprocessobase_id ON tbmovimentacao USING btree (tbprocessobase_id);


--
-- TOC entry 2334 (class 1259 OID 101851)
-- Name: tbmunicipio_Codigo_UF; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX "tbmunicipio_Codigo_UF" ON tbmunicipio USING btree ("Codigo_UF");


--
-- TOC entry 2339 (class 1259 OID 101852)
-- Name: tbpecastecnicas_tbcaixa_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX tbpecastecnicas_tbcaixa_id ON tbpecastecnicas USING btree (tbcaixa_id);


--
-- TOC entry 2340 (class 1259 OID 101853)
-- Name: tbpecastecnicas_tbcontrato_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX tbpecastecnicas_tbcontrato_id ON tbpecastecnicas USING btree (tbcontrato_id);


--
-- TOC entry 2341 (class 1259 OID 101854)
-- Name: tbpecastecnicas_tbdivisao_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX tbpecastecnicas_tbdivisao_id ON tbpecastecnicas USING btree (tbdivisao_id);


--
-- TOC entry 2342 (class 1259 OID 101855)
-- Name: tbpecastecnicas_tbgleba_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX tbpecastecnicas_tbgleba_id ON tbpecastecnicas USING btree (tbgleba_id);


--
-- TOC entry 2343 (class 1259 OID 101856)
-- Name: tbpendencia_auth_user_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX tbpendencia_auth_user_id ON tbpendencia USING btree (auth_user_id);


--
-- TOC entry 2346 (class 1259 OID 101857)
-- Name: tbpendencia_tbprocessobase_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX tbpendencia_tbprocessobase_id ON tbpendencia USING btree (tbprocessobase_id);


--
-- TOC entry 2347 (class 1259 OID 101858)
-- Name: tbpendencia_tbstatuspendencia_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX tbpendencia_tbstatuspendencia_id ON tbpendencia USING btree (tbstatuspendencia_id);


--
-- TOC entry 2348 (class 1259 OID 101859)
-- Name: tbpendencia_tbtipopendencia_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX tbpendencia_tbtipopendencia_id ON tbpendencia USING btree (tbtipopendencia_id);


--
-- TOC entry 2351 (class 1259 OID 101860)
-- Name: tbpregao_tbdivisao_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX tbpregao_tbdivisao_id ON tbpregao USING btree (tbdivisao_id);


--
-- TOC entry 2352 (class 1259 OID 101861)
-- Name: tbprocessobase_auth_user_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX tbprocessobase_auth_user_id ON tbprocessobase USING btree (auth_user_id);


--
-- TOC entry 2355 (class 1259 OID 101862)
-- Name: tbprocessobase_tbcaixa_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX tbprocessobase_tbcaixa_id ON tbprocessobase USING btree (tbcaixa_id);


--
-- TOC entry 2356 (class 1259 OID 101863)
-- Name: tbprocessobase_tbclassificacaoprocesso_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX tbprocessobase_tbclassificacaoprocesso_id ON tbprocessobase USING btree (tbclassificacaoprocesso_id);


--
-- TOC entry 2357 (class 1259 OID 101864)
-- Name: tbprocessobase_tbdivisao_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX tbprocessobase_tbdivisao_id ON tbprocessobase USING btree (tbdivisao_id);


--
-- TOC entry 2358 (class 1259 OID 101865)
-- Name: tbprocessobase_tbgleba_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX tbprocessobase_tbgleba_id ON tbprocessobase USING btree (tbgleba_id);


--
-- TOC entry 2359 (class 1259 OID 101866)
-- Name: tbprocessobase_tbmunicipio_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX tbprocessobase_tbmunicipio_id ON tbprocessobase USING btree (tbmunicipio_id);


--
-- TOC entry 2360 (class 1259 OID 101867)
-- Name: tbprocessobase_tbsituacaoprocesso_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX tbprocessobase_tbsituacaoprocesso_id ON tbprocessobase USING btree (tbsituacaoprocesso_id);


--
-- TOC entry 2361 (class 1259 OID 101868)
-- Name: tbprocessobase_tbtipoprocesso_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX tbprocessobase_tbtipoprocesso_id ON tbprocessobase USING btree (tbtipoprocesso_id);


--
-- TOC entry 2364 (class 1259 OID 101869)
-- Name: tbprocessoclausula_tbprocessobase_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX tbprocessoclausula_tbprocessobase_id ON tbprocessoclausula USING btree (tbprocessobase_id);


--
-- TOC entry 2367 (class 1259 OID 101870)
-- Name: tbprocessorural_tbprocessobase_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX tbprocessorural_tbprocessobase_id ON tbprocessorural USING btree (tbprocessobase_id);


--
-- TOC entry 2368 (class 1259 OID 101871)
-- Name: tbprocessosanexos_auth_user_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX tbprocessosanexos_auth_user_id ON tbprocessosanexos USING btree (auth_user_id);


--
-- TOC entry 2371 (class 1259 OID 101872)
-- Name: tbprocessosanexos_tbprocessobase_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX tbprocessosanexos_tbprocessobase_id ON tbprocessosanexos USING btree (tbprocessobase_id);


--
-- TOC entry 2372 (class 1259 OID 101873)
-- Name: tbprocessosanexos_tbprocessobase_id_anexo; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX tbprocessosanexos_tbprocessobase_id_anexo ON tbprocessosanexos USING btree (tbprocessobase_id_anexo);


--
-- TOC entry 2375 (class 1259 OID 101874)
-- Name: tbprocessourbano_tbcontrato_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX tbprocessourbano_tbcontrato_id ON tbprocessourbano USING btree (tbcontrato_id);


--
-- TOC entry 2376 (class 1259 OID 101875)
-- Name: tbprocessourbano_tbpregao_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX tbprocessourbano_tbpregao_id ON tbprocessourbano USING btree (tbpregao_id);


--
-- TOC entry 2377 (class 1259 OID 101876)
-- Name: tbprocessourbano_tbprocessobase_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX tbprocessourbano_tbprocessobase_id ON tbprocessourbano USING btree (tbprocessobase_id);


--
-- TOC entry 2378 (class 1259 OID 101877)
-- Name: tbprocessourbano_tbsituacaogeo_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX tbprocessourbano_tbsituacaogeo_id ON tbprocessourbano USING btree (tbsituacaogeo_id);


--
-- TOC entry 2381 (class 1259 OID 101878)
-- Name: tbservidor_tbdivisao_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX tbservidor_tbdivisao_id ON tbservidor USING btree (tbdivisao_id);


--
-- TOC entry 2386 (class 1259 OID 101879)
-- Name: tbsituacaogeo_tbdivisao_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX tbsituacaogeo_tbdivisao_id ON tbsituacaogeo USING btree (tbdivisao_id);


--
-- TOC entry 2389 (class 1259 OID 101880)
-- Name: tbsituacaoprocesso_tbdivisao_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX tbsituacaoprocesso_tbdivisao_id ON tbsituacaoprocesso USING btree (tbdivisao_id);


--
-- TOC entry 2392 (class 1259 OID 101881)
-- Name: tbstatuspendencia_tbdivisao_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX tbstatuspendencia_tbdivisao_id ON tbstatuspendencia USING btree (tbdivisao_id);


--
-- TOC entry 2395 (class 1259 OID 101882)
-- Name: tbsubarea_tbdivisao_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX tbsubarea_tbdivisao_id ON tbsubarea USING btree (tbdivisao_id);


--
-- TOC entry 2400 (class 1259 OID 101884)
-- Name: tbtipodocumento_tbdivisao_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX tbtipodocumento_tbdivisao_id ON tbtipodocumento USING btree (tbdivisao_id);


--
-- TOC entry 2403 (class 1259 OID 101885)
-- Name: tbtipopendencia_tbdivisao_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX tbtipopendencia_tbdivisao_id ON tbtipopendencia USING btree (tbdivisao_id);


--
-- TOC entry 2404 (class 1259 OID 101886)
-- Name: tbtipopendencia_tbtipoprocesso_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX tbtipopendencia_tbtipoprocesso_id ON tbtipopendencia USING btree (tbtipoprocesso_id);


--
-- TOC entry 2407 (class 1259 OID 101887)
-- Name: tbtipoprocesso_tbdivisao_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX tbtipoprocesso_tbdivisao_id ON tbtipoprocesso USING btree (tbdivisao_id);


SET search_path = documentos, pg_catalog;

--
-- TOC entry 2504 (class 2606 OID 102752)
-- Name: fk_tbbmp_patrimonio; Type: FK CONSTRAINT; Schema: documentos; Owner: admin
--

ALTER TABLE ONLY tbbmp_patrimonio
    ADD CONSTRAINT fk_tbbmp_patrimonio FOREIGN KEY (tbbmp_id) REFERENCES tbbmp(id);


--
-- TOC entry 2502 (class 2606 OID 102718)
-- Name: fk_tbdocumentobase_tbbmp; Type: FK CONSTRAINT; Schema: documentos; Owner: admin
--

ALTER TABLE ONLY tbbmp
    ADD CONSTRAINT fk_tbdocumentobase_tbbmp FOREIGN KEY (tbdocumentobase_id) REFERENCES public.tbdocumentobase(id);


--
-- TOC entry 2503 (class 2606 OID 102731)
-- Name: fk_tbdocumentobase_tbdiaria; Type: FK CONSTRAINT; Schema: documentos; Owner: admin
--

ALTER TABLE ONLY tbdiaria
    ADD CONSTRAINT fk_tbdocumentobase_tbdiaria FOREIGN KEY (tbdocumentobase_id) REFERENCES public.tbdocumentobase(id);


--
-- TOC entry 2499 (class 2606 OID 102679)
-- Name: fk_tbdocumentobase_tbrme; Type: FK CONSTRAINT; Schema: documentos; Owner: admin
--

ALTER TABLE ONLY tbrme
    ADD CONSTRAINT fk_tbdocumentobase_tbrme FOREIGN KEY (tbdocumentobase_id) REFERENCES public.tbdocumentobase(id);


--
-- TOC entry 2501 (class 2606 OID 102705)
-- Name: fk_tbdocumentobase_tbrv; Type: FK CONSTRAINT; Schema: documentos; Owner: admin
--

ALTER TABLE ONLY tbrv
    ADD CONSTRAINT fk_tbdocumentobase_tbrv FOREIGN KEY (tbdocumentobase_id) REFERENCES public.tbdocumentobase(id);


--
-- TOC entry 2500 (class 2606 OID 102692)
-- Name: fk_tbdocumentobase_tbtru; Type: FK CONSTRAINT; Schema: documentos; Owner: admin
--

ALTER TABLE ONLY tbtru
    ADD CONSTRAINT fk_tbdocumentobase_tbtru FOREIGN KEY (tbdocumentobase_id) REFERENCES public.tbdocumentobase(id);


--
-- TOC entry 2505 (class 2606 OID 102765)
-- Name: fk_tbrme_material; Type: FK CONSTRAINT; Schema: documentos; Owner: admin
--

ALTER TABLE ONLY tbrme_material
    ADD CONSTRAINT fk_tbrme_material FOREIGN KEY (tbrme_id) REFERENCES tbrme(id);


--
-- TOC entry 2498 (class 2606 OID 102652)
-- Name: tbmemorando_tbdocumentobase_id_fkey; Type: FK CONSTRAINT; Schema: documentos; Owner: admin
--

ALTER TABLE ONLY tbmemorando
    ADD CONSTRAINT tbmemorando_tbdocumentobase_id_fkey FOREIGN KEY (tbdocumentobase_id) REFERENCES public.tbdocumentobase(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2506 (class 2606 OID 102833)
-- Name: tboficio_tbdocumentobase_id_fkey; Type: FK CONSTRAINT; Schema: documentos; Owner: admin
--

ALTER TABLE ONLY tboficio
    ADD CONSTRAINT tboficio_tbdocumentobase_id_fkey FOREIGN KEY (tbdocumentobase_id) REFERENCES public.tbdocumentobase(id) DEFERRABLE INITIALLY DEFERRED;


SET search_path = public, pg_catalog;

--
-- TOC entry 2462 (class 2606 OID 101888)
-- Name: Codigo_UF_refs_id_29984a75; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbmunicipio
    ADD CONSTRAINT "Codigo_UF_refs_id_29984a75" FOREIGN KEY ("Codigo_UF") REFERENCES tbuf(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2431 (class 2606 OID 101893)
-- Name: auth_group_permissions_group_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_fkey FOREIGN KEY (group_id) REFERENCES auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2435 (class 2606 OID 101898)
-- Name: auth_user_groups_group_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY auth_user_groups
    ADD CONSTRAINT auth_user_groups_group_id_fkey FOREIGN KEY (group_id) REFERENCES auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2436 (class 2606 OID 101903)
-- Name: auth_user_groups_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY auth_user_groups
    ADD CONSTRAINT auth_user_groups_user_id_fkey FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2437 (class 2606 OID 101908)
-- Name: auth_user_user_permissions_permission_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_permission_id_fkey FOREIGN KEY (permission_id) REFERENCES auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2438 (class 2606 OID 101913)
-- Name: auth_user_user_permissions_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_user_id_fkey FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2439 (class 2606 OID 101918)
-- Name: content_type_id_refs_id_93d2d1f8; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY django_admin_log
    ADD CONSTRAINT content_type_id_refs_id_93d2d1f8 FOREIGN KEY (content_type_id) REFERENCES django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2433 (class 2606 OID 101923)
-- Name: content_type_id_refs_id_d043b34a; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY auth_permission
    ADD CONSTRAINT content_type_id_refs_id_d043b34a FOREIGN KEY (content_type_id) REFERENCES django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2440 (class 2606 OID 101928)
-- Name: django_admin_log_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY django_admin_log
    ADD CONSTRAINT django_admin_log_user_id_fkey FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2442 (class 2606 OID 102244)
-- Name: fk_tbdivisao_tbcaixa; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbcaixa
    ADD CONSTRAINT fk_tbdivisao_tbcaixa FOREIGN KEY (tbdivisao_id) REFERENCES tbdivisao(id);


--
-- TOC entry 2432 (class 2606 OID 101933)
-- Name: permission_id_refs_id_6ba0f519; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY auth_group_permissions
    ADD CONSTRAINT permission_id_refs_id_6ba0f519 FOREIGN KEY (permission_id) REFERENCES auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2430 (class 2606 OID 101938)
-- Name: tbdivisao_id_auth_group; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY auth_group
    ADD CONSTRAINT tbdivisao_id_auth_group FOREIGN KEY (tbdivisao_id) REFERENCES tbdivisao(id);


--
-- TOC entry 2443 (class 2606 OID 101943)
-- Name: tbdivisao_id_refs_id_00d25a11; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbclassificacaoprocesso
    ADD CONSTRAINT tbdivisao_id_refs_id_00d25a11 FOREIGN KEY (tbdivisao_id) REFERENCES tbdivisao(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2434 (class 2606 OID 101948)
-- Name: tbdivisao_id_refs_id_209f7cf0; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY auth_user
    ADD CONSTRAINT tbdivisao_id_refs_id_209f7cf0 FOREIGN KEY (tbdivisao_id) REFERENCES tbdivisao(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2444 (class 2606 OID 101953)
-- Name: tbdivisao_id_refs_id_c808e225; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbcontrato
    ADD CONSTRAINT tbdivisao_id_refs_id_c808e225 FOREIGN KEY (tbdivisao_id) REFERENCES tbdivisao(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2446 (class 2606 OID 101958)
-- Name: tbdocumentobase_auth_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbdocumentobase
    ADD CONSTRAINT tbdocumentobase_auth_user_id_fkey FOREIGN KEY (auth_user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2447 (class 2606 OID 101963)
-- Name: tbdocumentobase_tbdivisao_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbdocumentobase
    ADD CONSTRAINT tbdocumentobase_tbdivisao_id_fkey FOREIGN KEY (tbdivisao_id) REFERENCES tbdivisao(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2448 (class 2606 OID 101968)
-- Name: tbdocumentobase_tbtipodocumento_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbdocumentobase
    ADD CONSTRAINT tbdocumentobase_tbtipodocumento_id_fkey FOREIGN KEY (tbtipodocumento_id) REFERENCES tbtipodocumento(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2449 (class 2606 OID 101973)
-- Name: tbdocumentomemorando_tbdocumentobase_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbdocumentomemorando
    ADD CONSTRAINT tbdocumentomemorando_tbdocumentobase_id_fkey FOREIGN KEY (tbdocumentobase_id) REFERENCES tbdocumentobase(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2450 (class 2606 OID 101978)
-- Name: tbdocumentoservidor_tbdocumentobase_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbdocumentoservidor
    ADD CONSTRAINT tbdocumentoservidor_tbdocumentobase_id_fkey FOREIGN KEY (tbdocumentobase_id) REFERENCES tbdocumentobase(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2451 (class 2606 OID 101983)
-- Name: tbdocumentoservidor_tbservidor_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbdocumentoservidor
    ADD CONSTRAINT tbdocumentoservidor_tbservidor_id_fkey FOREIGN KEY (tbservidor_id) REFERENCES tbservidor(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2452 (class 2606 OID 101988)
-- Name: tbferias_stSituacao1_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbferias
    ADD CONSTRAINT "tbferias_stSituacao1_id_fkey" FOREIGN KEY ("stSituacao1_id") REFERENCES tbsituacao(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2453 (class 2606 OID 101993)
-- Name: tbferias_stSituacao2_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbferias
    ADD CONSTRAINT "tbferias_stSituacao2_id_fkey" FOREIGN KEY ("stSituacao2_id") REFERENCES tbsituacao(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2454 (class 2606 OID 101998)
-- Name: tbferias_stSituacao3_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbferias
    ADD CONSTRAINT "tbferias_stSituacao3_id_fkey" FOREIGN KEY ("stSituacao3_id") REFERENCES tbsituacao(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2455 (class 2606 OID 102003)
-- Name: tbferias_tbservidor_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbferias
    ADD CONSTRAINT tbferias_tbservidor_id_fkey FOREIGN KEY (tbservidor_id) REFERENCES tbservidor(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2458 (class 2606 OID 102008)
-- Name: tbmovimentacao_auth_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbmovimentacao
    ADD CONSTRAINT tbmovimentacao_auth_user_id_fkey FOREIGN KEY (auth_user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2459 (class 2606 OID 102013)
-- Name: tbmovimentacao_tbcaixa_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbmovimentacao
    ADD CONSTRAINT tbmovimentacao_tbcaixa_id_fkey FOREIGN KEY (tbcaixa_id) REFERENCES tbcaixa(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2460 (class 2606 OID 102018)
-- Name: tbmovimentacao_tbcaixa_id_origem_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbmovimentacao
    ADD CONSTRAINT tbmovimentacao_tbcaixa_id_origem_fkey FOREIGN KEY (tbcaixa_id_origem) REFERENCES tbcaixa(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2463 (class 2606 OID 102023)
-- Name: tbpecastecnicas_tbcaixa_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbpecastecnicas
    ADD CONSTRAINT tbpecastecnicas_tbcaixa_id_fkey FOREIGN KEY (tbcaixa_id) REFERENCES tbcaixa(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2464 (class 2606 OID 102028)
-- Name: tbpecastecnicas_tbcontrato_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbpecastecnicas
    ADD CONSTRAINT tbpecastecnicas_tbcontrato_id_fkey FOREIGN KEY (tbcontrato_id) REFERENCES tbcontrato(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2465 (class 2606 OID 102033)
-- Name: tbpecastecnicas_tbdivisao_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbpecastecnicas
    ADD CONSTRAINT tbpecastecnicas_tbdivisao_id_fkey FOREIGN KEY (tbdivisao_id) REFERENCES tbdivisao(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2466 (class 2606 OID 102038)
-- Name: tbpecastecnicas_tbgleba_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbpecastecnicas
    ADD CONSTRAINT tbpecastecnicas_tbgleba_id_fkey FOREIGN KEY (tbgleba_id) REFERENCES tbgleba(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2467 (class 2606 OID 102043)
-- Name: tbpendencia_auth_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbpendencia
    ADD CONSTRAINT tbpendencia_auth_user_id_fkey FOREIGN KEY (auth_user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2485 (class 2606 OID 102048)
-- Name: tbpregao_id_refs_id_f323926f; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbprocessourbano
    ADD CONSTRAINT tbpregao_id_refs_id_f323926f FOREIGN KEY (tbpregao_id) REFERENCES tbpregao(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2471 (class 2606 OID 102053)
-- Name: tbpregao_tbdivisao_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbpregao
    ADD CONSTRAINT tbpregao_tbdivisao_id_fkey FOREIGN KEY (tbdivisao_id) REFERENCES tbdivisao(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2472 (class 2606 OID 102058)
-- Name: tbprocessobase_auth_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbprocessobase
    ADD CONSTRAINT tbprocessobase_auth_user_id_fkey FOREIGN KEY (auth_user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2461 (class 2606 OID 102063)
-- Name: tbprocessobase_id_refs_id_5aebc46a; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbmovimentacao
    ADD CONSTRAINT tbprocessobase_id_refs_id_5aebc46a FOREIGN KEY (tbprocessobase_id) REFERENCES tbprocessobase(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2468 (class 2606 OID 102068)
-- Name: tbprocessobase_id_refs_id_86d3804c; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbpendencia
    ADD CONSTRAINT tbprocessobase_id_refs_id_86d3804c FOREIGN KEY (tbprocessobase_id) REFERENCES tbprocessobase(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2473 (class 2606 OID 102073)
-- Name: tbprocessobase_tbcaixa_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbprocessobase
    ADD CONSTRAINT tbprocessobase_tbcaixa_id_fkey FOREIGN KEY (tbcaixa_id) REFERENCES tbcaixa(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2474 (class 2606 OID 102078)
-- Name: tbprocessobase_tbclassificacaoprocesso_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbprocessobase
    ADD CONSTRAINT tbprocessobase_tbclassificacaoprocesso_id_fkey FOREIGN KEY (tbclassificacaoprocesso_id) REFERENCES tbclassificacaoprocesso(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2475 (class 2606 OID 102083)
-- Name: tbprocessobase_tbdivisao_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbprocessobase
    ADD CONSTRAINT tbprocessobase_tbdivisao_id_fkey FOREIGN KEY (tbdivisao_id) REFERENCES tbdivisao(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2476 (class 2606 OID 102088)
-- Name: tbprocessobase_tbgleba_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbprocessobase
    ADD CONSTRAINT tbprocessobase_tbgleba_id_fkey FOREIGN KEY (tbgleba_id) REFERENCES tbgleba(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2477 (class 2606 OID 102093)
-- Name: tbprocessobase_tbmunicipio_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbprocessobase
    ADD CONSTRAINT tbprocessobase_tbmunicipio_id_fkey FOREIGN KEY (tbmunicipio_id) REFERENCES tbmunicipio(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2480 (class 2606 OID 102098)
-- Name: tbprocessoclausula_tbprocessobase_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbprocessoclausula
    ADD CONSTRAINT tbprocessoclausula_tbprocessobase_id_fkey FOREIGN KEY (tbprocessobase_id) REFERENCES tbprocessobase(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2481 (class 2606 OID 102103)
-- Name: tbprocessorural_tbprocessobase_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbprocessorural
    ADD CONSTRAINT tbprocessorural_tbprocessobase_id_fkey FOREIGN KEY (tbprocessobase_id) REFERENCES tbprocessobase(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2482 (class 2606 OID 102108)
-- Name: tbprocessosanexos_auth_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbprocessosanexos
    ADD CONSTRAINT tbprocessosanexos_auth_user_id_fkey FOREIGN KEY (auth_user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2483 (class 2606 OID 102113)
-- Name: tbprocessosanexos_tbprocessobase_id_anexo_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbprocessosanexos
    ADD CONSTRAINT tbprocessosanexos_tbprocessobase_id_anexo_fkey FOREIGN KEY (tbprocessobase_id_anexo) REFERENCES tbprocessobase(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2484 (class 2606 OID 102118)
-- Name: tbprocessosanexos_tbprocessobase_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbprocessosanexos
    ADD CONSTRAINT tbprocessosanexos_tbprocessobase_id_fkey FOREIGN KEY (tbprocessobase_id) REFERENCES tbprocessobase(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2486 (class 2606 OID 102123)
-- Name: tbprocessourbano_tbcontrato_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbprocessourbano
    ADD CONSTRAINT tbprocessourbano_tbcontrato_id_fkey FOREIGN KEY (tbcontrato_id) REFERENCES tbcontrato(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2487 (class 2606 OID 102128)
-- Name: tbprocessourbano_tbprocessobase_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbprocessourbano
    ADD CONSTRAINT tbprocessourbano_tbprocessobase_id_fkey FOREIGN KEY (tbprocessobase_id) REFERENCES tbprocessobase(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2489 (class 2606 OID 102133)
-- Name: tbservidor_tbdivisao_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbservidor
    ADD CONSTRAINT tbservidor_tbdivisao_id_fkey FOREIGN KEY (tbdivisao_id) REFERENCES tbdivisao(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2488 (class 2606 OID 102138)
-- Name: tbsituacaogeo_id_refs_id_f9087efb; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbprocessourbano
    ADD CONSTRAINT tbsituacaogeo_id_refs_id_f9087efb FOREIGN KEY (tbsituacaogeo_id) REFERENCES tbsituacaogeo(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2490 (class 2606 OID 102143)
-- Name: tbsituacaogeo_tbdivisao_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbsituacaogeo
    ADD CONSTRAINT tbsituacaogeo_tbdivisao_id_fkey FOREIGN KEY (tbdivisao_id) REFERENCES tbdivisao(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2478 (class 2606 OID 102148)
-- Name: tbsituacaoprocesso_id_refs_id_bfef2fda; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbprocessobase
    ADD CONSTRAINT tbsituacaoprocesso_id_refs_id_bfef2fda FOREIGN KEY (tbsituacaoprocesso_id) REFERENCES tbsituacaoprocesso(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2491 (class 2606 OID 102153)
-- Name: tbsituacaoprocesso_tbdivisao_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbsituacaoprocesso
    ADD CONSTRAINT tbsituacaoprocesso_tbdivisao_id_fkey FOREIGN KEY (tbdivisao_id) REFERENCES tbdivisao(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2469 (class 2606 OID 102158)
-- Name: tbstatuspendencia_id_refs_id_615418ce; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbpendencia
    ADD CONSTRAINT tbstatuspendencia_id_refs_id_615418ce FOREIGN KEY (tbstatuspendencia_id) REFERENCES tbstatuspendencia(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2492 (class 2606 OID 102163)
-- Name: tbstatuspendencia_tbdivisao_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbstatuspendencia
    ADD CONSTRAINT tbstatuspendencia_tbdivisao_id_fkey FOREIGN KEY (tbdivisao_id) REFERENCES tbdivisao(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2456 (class 2606 OID 102168)
-- Name: tbsubarea_id_refs_id_c3c14a3b; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbgleba
    ADD CONSTRAINT tbsubarea_id_refs_id_c3c14a3b FOREIGN KEY (tbsubarea_id) REFERENCES tbsubarea(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2493 (class 2606 OID 102173)
-- Name: tbsubarea_tbdivisao_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbsubarea
    ADD CONSTRAINT tbsubarea_tbdivisao_id_fkey FOREIGN KEY (tbdivisao_id) REFERENCES tbdivisao(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2441 (class 2606 OID 102178)
-- Name: tbtipocaixa_id_refs_id_1f3d944c; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbcaixa
    ADD CONSTRAINT tbtipocaixa_id_refs_id_1f3d944c FOREIGN KEY (tbtipocaixa_id) REFERENCES tbtipocaixa(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2494 (class 2606 OID 102188)
-- Name: tbtipodocumento_tbdivisao_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbtipodocumento
    ADD CONSTRAINT tbtipodocumento_tbdivisao_id_fkey FOREIGN KEY (tbdivisao_id) REFERENCES tbdivisao(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2470 (class 2606 OID 102193)
-- Name: tbtipopendencia_id_refs_id_4f9053c1; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbpendencia
    ADD CONSTRAINT tbtipopendencia_id_refs_id_4f9053c1 FOREIGN KEY (tbtipopendencia_id) REFERENCES tbtipopendencia(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2495 (class 2606 OID 102198)
-- Name: tbtipopendencia_tbdivisao_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbtipopendencia
    ADD CONSTRAINT tbtipopendencia_tbdivisao_id_fkey FOREIGN KEY (tbdivisao_id) REFERENCES tbdivisao(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2496 (class 2606 OID 102203)
-- Name: tbtipoprocesso_id_refs_id_14dae0cf; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbtipopendencia
    ADD CONSTRAINT tbtipoprocesso_id_refs_id_14dae0cf FOREIGN KEY (tbtipoprocesso_id) REFERENCES tbtipoprocesso(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2479 (class 2606 OID 102208)
-- Name: tbtipoprocesso_id_refs_id_64d671a3; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbprocessobase
    ADD CONSTRAINT tbtipoprocesso_id_refs_id_64d671a3 FOREIGN KEY (tbtipoprocesso_id) REFERENCES tbtipoprocesso(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2497 (class 2606 OID 102213)
-- Name: tbtipoprocesso_tbdivisao_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbtipoprocesso
    ADD CONSTRAINT tbtipoprocesso_tbdivisao_id_fkey FOREIGN KEY (tbdivisao_id) REFERENCES tbdivisao(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2445 (class 2606 OID 102218)
-- Name: tbuf_id_refs_id_c8d633fb; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbdivisao
    ADD CONSTRAINT tbuf_id_refs_id_c8d633fb FOREIGN KEY (tbuf_id) REFERENCES tbuf(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2457 (class 2606 OID 102223)
-- Name: tbuf_id_tbgleba; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbgleba
    ADD CONSTRAINT tbuf_id_tbgleba FOREIGN KEY (tbuf_id) REFERENCES tbuf(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2513 (class 0 OID 0)
-- Dependencies: 6
-- Name: public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM postgres;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO PUBLIC;


-- Completed on 2014-03-25 12:32:37

--
-- PostgreSQL database dump complete
--

