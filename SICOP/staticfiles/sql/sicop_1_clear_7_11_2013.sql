--
-- PostgreSQL database dump
--

-- Dumped from database version 9.1.6
-- Dumped by pg_dump version 9.1.6
-- Started on 2013-11-07 15:52:11 BRT

SET statement_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

--
-- TOC entry 221 (class 3079 OID 11684)
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- TOC entry 2301 (class 0 OID 0)
-- Dependencies: 221
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = public, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- TOC entry 161 (class 1259 OID 5839469)
-- Dependencies: 5
-- Name: auth_group; Type: TABLE; Schema: public; Owner: admin; Tablespace: 
--

CREATE TABLE auth_group (
    id integer NOT NULL,
    name character varying(80) NOT NULL
);


ALTER TABLE public.auth_group OWNER TO admin;

--
-- TOC entry 162 (class 1259 OID 5839476)
-- Dependencies: 5
-- Name: auth_group_permissions; Type: TABLE; Schema: public; Owner: admin; Tablespace: 
--

CREATE TABLE auth_group_permissions (
    id integer NOT NULL,
    group_id integer NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE public.auth_group_permissions OWNER TO admin;

--
-- TOC entry 163 (class 1259 OID 5839486)
-- Dependencies: 5
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
-- TOC entry 165 (class 1259 OID 5839498)
-- Dependencies: 5
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
-- TOC entry 167 (class 1259 OID 5839508)
-- Dependencies: 5
-- Name: auth_user_groups; Type: TABLE; Schema: public; Owner: admin; Tablespace: 
--

CREATE TABLE auth_user_groups (
    id integer NOT NULL,
    user_id integer NOT NULL,
    group_id integer NOT NULL
);


ALTER TABLE public.auth_user_groups OWNER TO admin;

--
-- TOC entry 166 (class 1259 OID 5839506)
-- Dependencies: 5 167
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
-- TOC entry 2302 (class 0 OID 0)
-- Dependencies: 166
-- Name: auth_user_groups_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE auth_user_groups_id_seq OWNED BY auth_user_groups.id;


--
-- TOC entry 164 (class 1259 OID 5839496)
-- Dependencies: 165 5
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
-- TOC entry 2303 (class 0 OID 0)
-- Dependencies: 164
-- Name: auth_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE auth_user_id_seq OWNED BY auth_user.id;


--
-- TOC entry 168 (class 1259 OID 5839524)
-- Dependencies: 5
-- Name: auth_user_user_permissions; Type: TABLE; Schema: public; Owner: admin; Tablespace: 
--

CREATE TABLE auth_user_user_permissions (
    id integer NOT NULL,
    user_id integer NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE public.auth_user_user_permissions OWNER TO admin;

--
-- TOC entry 169 (class 1259 OID 5839539)
-- Dependencies: 5
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
-- TOC entry 170 (class 1259 OID 5839552)
-- Dependencies: 5
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
-- TOC entry 171 (class 1259 OID 5839567)
-- Dependencies: 5
-- Name: django_session; Type: TABLE; Schema: public; Owner: admin; Tablespace: 
--

CREATE TABLE django_session (
    session_key character varying(40) NOT NULL,
    session_data text NOT NULL,
    expire_date timestamp with time zone NOT NULL
);


ALTER TABLE public.django_session OWNER TO admin;

--
-- TOC entry 172 (class 1259 OID 5839575)
-- Dependencies: 5
-- Name: django_site; Type: TABLE; Schema: public; Owner: admin; Tablespace: 
--

CREATE TABLE django_site (
    id integer NOT NULL,
    domain character varying(100) NOT NULL,
    name character varying(50) NOT NULL
);


ALTER TABLE public.django_site OWNER TO admin;

--
-- TOC entry 174 (class 1259 OID 5839582)
-- Dependencies: 5
-- Name: tbcaixa; Type: TABLE; Schema: public; Owner: admin; Tablespace: 
--

CREATE TABLE tbcaixa (
    nmlocalarquivo character varying(80) NOT NULL,
    tbtipocaixa_id integer NOT NULL,
    id integer NOT NULL
);


ALTER TABLE public.tbcaixa OWNER TO admin;

--
-- TOC entry 173 (class 1259 OID 5839580)
-- Dependencies: 174 5
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
-- TOC entry 2304 (class 0 OID 0)
-- Dependencies: 173
-- Name: tbcaixa_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE tbcaixa_id_seq OWNED BY tbcaixa.id;


--
-- TOC entry 176 (class 1259 OID 5839590)
-- Dependencies: 5
-- Name: tbclassificacaoprocesso; Type: TABLE; Schema: public; Owner: admin; Tablespace: 
--

CREATE TABLE tbclassificacaoprocesso (
    nmclassificacao character varying(80) NOT NULL,
    tbdivisao_id integer,
    id integer NOT NULL
);


ALTER TABLE public.tbclassificacaoprocesso OWNER TO admin;

--
-- TOC entry 175 (class 1259 OID 5839588)
-- Dependencies: 176 5
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
-- TOC entry 2305 (class 0 OID 0)
-- Dependencies: 175
-- Name: tbclassificacaoprocesso_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE tbclassificacaoprocesso_id_seq OWNED BY tbclassificacaoprocesso.id;


--
-- TOC entry 178 (class 1259 OID 5839598)
-- Dependencies: 5
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
-- TOC entry 177 (class 1259 OID 5839596)
-- Dependencies: 5 178
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
-- TOC entry 2306 (class 0 OID 0)
-- Dependencies: 177
-- Name: tbcontrato_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE tbcontrato_id_seq OWNED BY tbcontrato.id;


--
-- TOC entry 180 (class 1259 OID 5839606)
-- Dependencies: 5
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
-- TOC entry 179 (class 1259 OID 5839604)
-- Dependencies: 180 5
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
-- TOC entry 2307 (class 0 OID 0)
-- Dependencies: 179
-- Name: tbdivisao_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE tbdivisao_id_seq OWNED BY tbdivisao.id;


--
-- TOC entry 182 (class 1259 OID 5839632)
-- Dependencies: 5
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
-- TOC entry 181 (class 1259 OID 5839630)
-- Dependencies: 182 5
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
-- TOC entry 2308 (class 0 OID 0)
-- Dependencies: 181
-- Name: tbgleba_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE tbgleba_id_seq OWNED BY tbgleba.id;


--
-- TOC entry 184 (class 1259 OID 5839640)
-- Dependencies: 5
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
-- TOC entry 183 (class 1259 OID 5839638)
-- Dependencies: 5 184
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
-- TOC entry 2309 (class 0 OID 0)
-- Dependencies: 183
-- Name: tbmovimentacao_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE tbmovimentacao_id_seq OWNED BY tbmovimentacao.id;


--
-- TOC entry 186 (class 1259 OID 5839663)
-- Dependencies: 5
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
-- TOC entry 185 (class 1259 OID 5839661)
-- Dependencies: 5 186
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
-- TOC entry 2310 (class 0 OID 0)
-- Dependencies: 185
-- Name: tbmunicipio_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE tbmunicipio_id_seq OWNED BY tbmunicipio.id;


--
-- TOC entry 188 (class 1259 OID 5839671)
-- Dependencies: 5
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
-- TOC entry 187 (class 1259 OID 5839669)
-- Dependencies: 188 5
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
-- TOC entry 2311 (class 0 OID 0)
-- Dependencies: 187
-- Name: tbpecastecnicas_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE tbpecastecnicas_id_seq OWNED BY tbpecastecnicas.id;


--
-- TOC entry 190 (class 1259 OID 5839702)
-- Dependencies: 5
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
-- TOC entry 189 (class 1259 OID 5839700)
-- Dependencies: 190 5
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
-- TOC entry 2312 (class 0 OID 0)
-- Dependencies: 189
-- Name: tbpendencia_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE tbpendencia_id_seq OWNED BY tbpendencia.id;


--
-- TOC entry 220 (class 1259 OID 5840005)
-- Dependencies: 5
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
-- TOC entry 219 (class 1259 OID 5840003)
-- Dependencies: 5 220
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
-- TOC entry 2313 (class 0 OID 0)
-- Dependencies: 219
-- Name: tbpregao_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE tbpregao_id_seq OWNED BY tbpregao.id;


--
-- TOC entry 192 (class 1259 OID 5839718)
-- Dependencies: 5
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
-- TOC entry 191 (class 1259 OID 5839716)
-- Dependencies: 192 5
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
-- TOC entry 2314 (class 0 OID 0)
-- Dependencies: 191
-- Name: tbprocessobase_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE tbprocessobase_id_seq OWNED BY tbprocessobase.id;


--
-- TOC entry 194 (class 1259 OID 5839766)
-- Dependencies: 5
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
-- TOC entry 193 (class 1259 OID 5839764)
-- Dependencies: 5 194
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
-- TOC entry 2315 (class 0 OID 0)
-- Dependencies: 193
-- Name: tbprocessoclausula_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE tbprocessoclausula_id_seq OWNED BY tbprocessoclausula.id;


--
-- TOC entry 196 (class 1259 OID 5839782)
-- Dependencies: 5
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
-- TOC entry 195 (class 1259 OID 5839780)
-- Dependencies: 196 5
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
-- TOC entry 2316 (class 0 OID 0)
-- Dependencies: 195
-- Name: tbprocessorural_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE tbprocessorural_id_seq OWNED BY tbprocessorural.id;


--
-- TOC entry 198 (class 1259 OID 5839795)
-- Dependencies: 5
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
-- TOC entry 197 (class 1259 OID 5839793)
-- Dependencies: 198 5
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
-- TOC entry 2317 (class 0 OID 0)
-- Dependencies: 197
-- Name: tbprocessosanexos_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE tbprocessosanexos_id_seq OWNED BY tbprocessosanexos.id;


--
-- TOC entry 200 (class 1259 OID 5839818)
-- Dependencies: 5
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
-- TOC entry 199 (class 1259 OID 5839816)
-- Dependencies: 5 200
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
-- TOC entry 2318 (class 0 OID 0)
-- Dependencies: 199
-- Name: tbprocessourbano_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE tbprocessourbano_id_seq OWNED BY tbprocessourbano.id;


--
-- TOC entry 202 (class 1259 OID 5839836)
-- Dependencies: 5
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
-- TOC entry 201 (class 1259 OID 5839834)
-- Dependencies: 5 202
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
-- TOC entry 2319 (class 0 OID 0)
-- Dependencies: 201
-- Name: tbservidor_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE tbservidor_id_seq OWNED BY tbservidor.id;


--
-- TOC entry 204 (class 1259 OID 5839847)
-- Dependencies: 5
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
-- TOC entry 203 (class 1259 OID 5839845)
-- Dependencies: 5 204
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
-- TOC entry 2320 (class 0 OID 0)
-- Dependencies: 203
-- Name: tbsituacaogeo_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE tbsituacaogeo_id_seq OWNED BY tbsituacaogeo.id;


--
-- TOC entry 206 (class 1259 OID 5839868)
-- Dependencies: 5
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
-- TOC entry 205 (class 1259 OID 5839866)
-- Dependencies: 206 5
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
-- TOC entry 2321 (class 0 OID 0)
-- Dependencies: 205
-- Name: tbsituacaoprocesso_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE tbsituacaoprocesso_id_seq OWNED BY tbsituacaoprocesso.id;


--
-- TOC entry 208 (class 1259 OID 5839889)
-- Dependencies: 5
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
-- TOC entry 207 (class 1259 OID 5839887)
-- Dependencies: 5 208
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
-- TOC entry 2322 (class 0 OID 0)
-- Dependencies: 207
-- Name: tbstatuspendencia_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE tbstatuspendencia_id_seq OWNED BY tbstatuspendencia.id;


--
-- TOC entry 210 (class 1259 OID 5839907)
-- Dependencies: 5
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
-- TOC entry 209 (class 1259 OID 5839905)
-- Dependencies: 210 5
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
-- TOC entry 2323 (class 0 OID 0)
-- Dependencies: 209
-- Name: tbsubarea_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE tbsubarea_id_seq OWNED BY tbsubarea.id;


--
-- TOC entry 212 (class 1259 OID 5839925)
-- Dependencies: 5
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
-- TOC entry 211 (class 1259 OID 5839923)
-- Dependencies: 5 212
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
-- TOC entry 2324 (class 0 OID 0)
-- Dependencies: 211
-- Name: tbtipocaixa_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE tbtipocaixa_id_seq OWNED BY tbtipocaixa.id;


--
-- TOC entry 214 (class 1259 OID 5839946)
-- Dependencies: 5
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
-- TOC entry 213 (class 1259 OID 5839944)
-- Dependencies: 214 5
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
-- TOC entry 2325 (class 0 OID 0)
-- Dependencies: 213
-- Name: tbtipopendencia_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE tbtipopendencia_id_seq OWNED BY tbtipopendencia.id;


--
-- TOC entry 216 (class 1259 OID 5839964)
-- Dependencies: 5
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
-- TOC entry 215 (class 1259 OID 5839962)
-- Dependencies: 216 5
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
-- TOC entry 2326 (class 0 OID 0)
-- Dependencies: 215
-- Name: tbtipoprocesso_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE tbtipoprocesso_id_seq OWNED BY tbtipoprocesso.id;


--
-- TOC entry 218 (class 1259 OID 5839987)
-- Dependencies: 5
-- Name: tbuf; Type: TABLE; Schema: public; Owner: admin; Tablespace: 
--

CREATE TABLE tbuf (
    sigla character varying(2) NOT NULL,
    nmuf character varying(50) NOT NULL,
    id integer NOT NULL
);


ALTER TABLE public.tbuf OWNER TO admin;

--
-- TOC entry 217 (class 1259 OID 5839985)
-- Dependencies: 218 5
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
-- TOC entry 2327 (class 0 OID 0)
-- Dependencies: 217
-- Name: tbuf_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: admin
--

ALTER SEQUENCE tbuf_id_seq OWNED BY tbuf.id;


--
-- TOC entry 2085 (class 2604 OID 5839501)
-- Dependencies: 164 165 165
-- Name: id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY auth_user ALTER COLUMN id SET DEFAULT nextval('auth_user_id_seq'::regclass);


--
-- TOC entry 2086 (class 2604 OID 5839511)
-- Dependencies: 167 166 167
-- Name: id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY auth_user_groups ALTER COLUMN id SET DEFAULT nextval('auth_user_groups_id_seq'::regclass);


--
-- TOC entry 2087 (class 2604 OID 5839585)
-- Dependencies: 173 174 174
-- Name: id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbcaixa ALTER COLUMN id SET DEFAULT nextval('tbcaixa_id_seq'::regclass);


--
-- TOC entry 2088 (class 2604 OID 5839593)
-- Dependencies: 176 175 176
-- Name: id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbclassificacaoprocesso ALTER COLUMN id SET DEFAULT nextval('tbclassificacaoprocesso_id_seq'::regclass);


--
-- TOC entry 2089 (class 2604 OID 5839601)
-- Dependencies: 177 178 178
-- Name: id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbcontrato ALTER COLUMN id SET DEFAULT nextval('tbcontrato_id_seq'::regclass);


--
-- TOC entry 2090 (class 2604 OID 5839609)
-- Dependencies: 180 179 180
-- Name: id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbdivisao ALTER COLUMN id SET DEFAULT nextval('tbdivisao_id_seq'::regclass);


--
-- TOC entry 2091 (class 2604 OID 5839635)
-- Dependencies: 182 181 182
-- Name: id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbgleba ALTER COLUMN id SET DEFAULT nextval('tbgleba_id_seq'::regclass);


--
-- TOC entry 2092 (class 2604 OID 5839643)
-- Dependencies: 184 183 184
-- Name: id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbmovimentacao ALTER COLUMN id SET DEFAULT nextval('tbmovimentacao_id_seq'::regclass);


--
-- TOC entry 2093 (class 2604 OID 5839666)
-- Dependencies: 186 185 186
-- Name: id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbmunicipio ALTER COLUMN id SET DEFAULT nextval('tbmunicipio_id_seq'::regclass);


--
-- TOC entry 2094 (class 2604 OID 5839674)
-- Dependencies: 187 188 188
-- Name: id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbpecastecnicas ALTER COLUMN id SET DEFAULT nextval('tbpecastecnicas_id_seq'::regclass);


--
-- TOC entry 2095 (class 2604 OID 5839705)
-- Dependencies: 189 190 190
-- Name: id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbpendencia ALTER COLUMN id SET DEFAULT nextval('tbpendencia_id_seq'::regclass);


--
-- TOC entry 2110 (class 2604 OID 5840008)
-- Dependencies: 220 219 220
-- Name: id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbpregao ALTER COLUMN id SET DEFAULT nextval('tbpregao_id_seq'::regclass);


--
-- TOC entry 2096 (class 2604 OID 5839721)
-- Dependencies: 192 191 192
-- Name: id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbprocessobase ALTER COLUMN id SET DEFAULT nextval('tbprocessobase_id_seq'::regclass);


--
-- TOC entry 2097 (class 2604 OID 5839769)
-- Dependencies: 194 193 194
-- Name: id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbprocessoclausula ALTER COLUMN id SET DEFAULT nextval('tbprocessoclausula_id_seq'::regclass);


--
-- TOC entry 2098 (class 2604 OID 5839785)
-- Dependencies: 195 196 196
-- Name: id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbprocessorural ALTER COLUMN id SET DEFAULT nextval('tbprocessorural_id_seq'::regclass);


--
-- TOC entry 2099 (class 2604 OID 5839798)
-- Dependencies: 197 198 198
-- Name: id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbprocessosanexos ALTER COLUMN id SET DEFAULT nextval('tbprocessosanexos_id_seq'::regclass);


--
-- TOC entry 2100 (class 2604 OID 5839821)
-- Dependencies: 200 199 200
-- Name: id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbprocessourbano ALTER COLUMN id SET DEFAULT nextval('tbprocessourbano_id_seq'::regclass);


--
-- TOC entry 2101 (class 2604 OID 5839839)
-- Dependencies: 201 202 202
-- Name: id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbservidor ALTER COLUMN id SET DEFAULT nextval('tbservidor_id_seq'::regclass);


--
-- TOC entry 2102 (class 2604 OID 5839850)
-- Dependencies: 204 203 204
-- Name: id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbsituacaogeo ALTER COLUMN id SET DEFAULT nextval('tbsituacaogeo_id_seq'::regclass);


--
-- TOC entry 2103 (class 2604 OID 5839871)
-- Dependencies: 205 206 206
-- Name: id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbsituacaoprocesso ALTER COLUMN id SET DEFAULT nextval('tbsituacaoprocesso_id_seq'::regclass);


--
-- TOC entry 2104 (class 2604 OID 5839892)
-- Dependencies: 208 207 208
-- Name: id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbstatuspendencia ALTER COLUMN id SET DEFAULT nextval('tbstatuspendencia_id_seq'::regclass);


--
-- TOC entry 2105 (class 2604 OID 5839910)
-- Dependencies: 209 210 210
-- Name: id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbsubarea ALTER COLUMN id SET DEFAULT nextval('tbsubarea_id_seq'::regclass);


--
-- TOC entry 2106 (class 2604 OID 5839928)
-- Dependencies: 212 211 212
-- Name: id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbtipocaixa ALTER COLUMN id SET DEFAULT nextval('tbtipocaixa_id_seq'::regclass);


--
-- TOC entry 2107 (class 2604 OID 5839949)
-- Dependencies: 213 214 214
-- Name: id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbtipopendencia ALTER COLUMN id SET DEFAULT nextval('tbtipopendencia_id_seq'::regclass);


--
-- TOC entry 2108 (class 2604 OID 5839967)
-- Dependencies: 216 215 216
-- Name: id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbtipoprocesso ALTER COLUMN id SET DEFAULT nextval('tbtipoprocesso_id_seq'::regclass);


--
-- TOC entry 2109 (class 2604 OID 5839990)
-- Dependencies: 217 218 218
-- Name: id; Type: DEFAULT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbuf ALTER COLUMN id SET DEFAULT nextval('tbuf_id_seq'::regclass);


--
-- TOC entry 2112 (class 2606 OID 5839475)
-- Dependencies: 161 161 2295
-- Name: auth_group_name_key; Type: CONSTRAINT; Schema: public; Owner: admin; Tablespace: 
--

ALTER TABLE ONLY auth_group
    ADD CONSTRAINT auth_group_name_key UNIQUE (name);


--
-- TOC entry 2119 (class 2606 OID 5839480)
-- Dependencies: 162 162 2295
-- Name: auth_group_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: admin; Tablespace: 
--

ALTER TABLE ONLY auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_pkey PRIMARY KEY (id);


--
-- TOC entry 2115 (class 2606 OID 5839473)
-- Dependencies: 161 161 2295
-- Name: auth_group_pkey; Type: CONSTRAINT; Schema: public; Owner: admin; Tablespace: 
--

ALTER TABLE ONLY auth_group
    ADD CONSTRAINT auth_group_pkey PRIMARY KEY (id);


--
-- TOC entry 2122 (class 2606 OID 5839490)
-- Dependencies: 163 163 2295
-- Name: auth_permission_pkey; Type: CONSTRAINT; Schema: public; Owner: admin; Tablespace: 
--

ALTER TABLE ONLY auth_permission
    ADD CONSTRAINT auth_permission_pkey PRIMARY KEY (id);


--
-- TOC entry 2131 (class 2606 OID 5839513)
-- Dependencies: 167 167 2295
-- Name: auth_user_groups_pkey; Type: CONSTRAINT; Schema: public; Owner: admin; Tablespace: 
--

ALTER TABLE ONLY auth_user_groups
    ADD CONSTRAINT auth_user_groups_pkey PRIMARY KEY (id);


--
-- TOC entry 2124 (class 2606 OID 5839503)
-- Dependencies: 165 165 2295
-- Name: auth_user_pkey; Type: CONSTRAINT; Schema: public; Owner: admin; Tablespace: 
--

ALTER TABLE ONLY auth_user
    ADD CONSTRAINT auth_user_pkey PRIMARY KEY (id);


--
-- TOC entry 2135 (class 2606 OID 5839528)
-- Dependencies: 168 168 2295
-- Name: auth_user_user_permissions_pkey; Type: CONSTRAINT; Schema: public; Owner: admin; Tablespace: 
--

ALTER TABLE ONLY auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_pkey PRIMARY KEY (id);


--
-- TOC entry 2127 (class 2606 OID 5839505)
-- Dependencies: 165 165 2295
-- Name: auth_user_username_key; Type: CONSTRAINT; Schema: public; Owner: admin; Tablespace: 
--

ALTER TABLE ONLY auth_user
    ADD CONSTRAINT auth_user_username_key UNIQUE (username);


--
-- TOC entry 2139 (class 2606 OID 5839546)
-- Dependencies: 169 169 2295
-- Name: django_admin_log_pkey; Type: CONSTRAINT; Schema: public; Owner: admin; Tablespace: 
--

ALTER TABLE ONLY django_admin_log
    ADD CONSTRAINT django_admin_log_pkey PRIMARY KEY (id);


--
-- TOC entry 2142 (class 2606 OID 5839556)
-- Dependencies: 170 170 2295
-- Name: django_content_type_pkey; Type: CONSTRAINT; Schema: public; Owner: admin; Tablespace: 
--

ALTER TABLE ONLY django_content_type
    ADD CONSTRAINT django_content_type_pkey PRIMARY KEY (id);


--
-- TOC entry 2144 (class 2606 OID 5839574)
-- Dependencies: 171 171 2295
-- Name: django_session_pkey; Type: CONSTRAINT; Schema: public; Owner: admin; Tablespace: 
--

ALTER TABLE ONLY django_session
    ADD CONSTRAINT django_session_pkey PRIMARY KEY (session_key);


--
-- TOC entry 2147 (class 2606 OID 5839579)
-- Dependencies: 172 172 2295
-- Name: django_site_pkey; Type: CONSTRAINT; Schema: public; Owner: admin; Tablespace: 
--

ALTER TABLE ONLY django_site
    ADD CONSTRAINT django_site_pkey PRIMARY KEY (id);


--
-- TOC entry 2149 (class 2606 OID 5839587)
-- Dependencies: 174 174 2295
-- Name: tbcaixa_pkey; Type: CONSTRAINT; Schema: public; Owner: admin; Tablespace: 
--

ALTER TABLE ONLY tbcaixa
    ADD CONSTRAINT tbcaixa_pkey PRIMARY KEY (id);


--
-- TOC entry 2152 (class 2606 OID 5839595)
-- Dependencies: 176 176 2295
-- Name: tbclassificacaoprocesso_pkey; Type: CONSTRAINT; Schema: public; Owner: admin; Tablespace: 
--

ALTER TABLE ONLY tbclassificacaoprocesso
    ADD CONSTRAINT tbclassificacaoprocesso_pkey PRIMARY KEY (id);


--
-- TOC entry 2155 (class 2606 OID 5839603)
-- Dependencies: 178 178 2295
-- Name: tbcontrato_pkey; Type: CONSTRAINT; Schema: public; Owner: admin; Tablespace: 
--

ALTER TABLE ONLY tbcontrato
    ADD CONSTRAINT tbcontrato_pkey PRIMARY KEY (id);


--
-- TOC entry 2158 (class 2606 OID 5839614)
-- Dependencies: 180 180 2295
-- Name: tbdivisao_pkey; Type: CONSTRAINT; Schema: public; Owner: admin; Tablespace: 
--

ALTER TABLE ONLY tbdivisao
    ADD CONSTRAINT tbdivisao_pkey PRIMARY KEY (id);


--
-- TOC entry 2161 (class 2606 OID 5839637)
-- Dependencies: 182 182 2295
-- Name: tbgleba_pkey; Type: CONSTRAINT; Schema: public; Owner: admin; Tablespace: 
--

ALTER TABLE ONLY tbgleba
    ADD CONSTRAINT tbgleba_pkey PRIMARY KEY (id);


--
-- TOC entry 2165 (class 2606 OID 5839645)
-- Dependencies: 184 184 2295
-- Name: tbmovimentacao_pkey; Type: CONSTRAINT; Schema: public; Owner: admin; Tablespace: 
--

ALTER TABLE ONLY tbmovimentacao
    ADD CONSTRAINT tbmovimentacao_pkey PRIMARY KEY (id);


--
-- TOC entry 2171 (class 2606 OID 5839668)
-- Dependencies: 186 186 2295
-- Name: tbmunicipio_pkey; Type: CONSTRAINT; Schema: public; Owner: admin; Tablespace: 
--

ALTER TABLE ONLY tbmunicipio
    ADD CONSTRAINT tbmunicipio_pkey PRIMARY KEY (id);


--
-- TOC entry 2173 (class 2606 OID 5839679)
-- Dependencies: 188 188 2295
-- Name: tbpecastecnicas_pkey; Type: CONSTRAINT; Schema: public; Owner: admin; Tablespace: 
--

ALTER TABLE ONLY tbpecastecnicas
    ADD CONSTRAINT tbpecastecnicas_pkey PRIMARY KEY (id);


--
-- TOC entry 2180 (class 2606 OID 5839710)
-- Dependencies: 190 190 2295
-- Name: tbpendencia_pkey; Type: CONSTRAINT; Schema: public; Owner: admin; Tablespace: 
--

ALTER TABLE ONLY tbpendencia
    ADD CONSTRAINT tbpendencia_pkey PRIMARY KEY (id);


--
-- TOC entry 2238 (class 2606 OID 5840013)
-- Dependencies: 220 220 2295
-- Name: tbpregao_pkey; Type: CONSTRAINT; Schema: public; Owner: admin; Tablespace: 
--

ALTER TABLE ONLY tbpregao
    ADD CONSTRAINT tbpregao_pkey PRIMARY KEY (id);


--
-- TOC entry 2186 (class 2606 OID 5839723)
-- Dependencies: 192 192 2295
-- Name: tbprocessobase_pkey; Type: CONSTRAINT; Schema: public; Owner: admin; Tablespace: 
--

ALTER TABLE ONLY tbprocessobase
    ADD CONSTRAINT tbprocessobase_pkey PRIMARY KEY (id);


--
-- TOC entry 2195 (class 2606 OID 5839774)
-- Dependencies: 194 194 2295
-- Name: tbprocessoclausula_pkey; Type: CONSTRAINT; Schema: public; Owner: admin; Tablespace: 
--

ALTER TABLE ONLY tbprocessoclausula
    ADD CONSTRAINT tbprocessoclausula_pkey PRIMARY KEY (id);


--
-- TOC entry 2198 (class 2606 OID 5839787)
-- Dependencies: 196 196 2295
-- Name: tbprocessorural_pkey; Type: CONSTRAINT; Schema: public; Owner: admin; Tablespace: 
--

ALTER TABLE ONLY tbprocessorural
    ADD CONSTRAINT tbprocessorural_pkey PRIMARY KEY (id);


--
-- TOC entry 2202 (class 2606 OID 5839800)
-- Dependencies: 198 198 2295
-- Name: tbprocessosanexos_pkey; Type: CONSTRAINT; Schema: public; Owner: admin; Tablespace: 
--

ALTER TABLE ONLY tbprocessosanexos
    ADD CONSTRAINT tbprocessosanexos_pkey PRIMARY KEY (id);


--
-- TOC entry 2206 (class 2606 OID 5839823)
-- Dependencies: 200 200 2295
-- Name: tbprocessourbano_pkey; Type: CONSTRAINT; Schema: public; Owner: admin; Tablespace: 
--

ALTER TABLE ONLY tbprocessourbano
    ADD CONSTRAINT tbprocessourbano_pkey PRIMARY KEY (id);


--
-- TOC entry 2212 (class 2606 OID 5839844)
-- Dependencies: 202 202 2295
-- Name: tbservidor_pkey; Type: CONSTRAINT; Schema: public; Owner: admin; Tablespace: 
--

ALTER TABLE ONLY tbservidor
    ADD CONSTRAINT tbservidor_pkey PRIMARY KEY (id);


--
-- TOC entry 2214 (class 2606 OID 5839855)
-- Dependencies: 204 204 2295
-- Name: tbsituacaogeo_pkey; Type: CONSTRAINT; Schema: public; Owner: admin; Tablespace: 
--

ALTER TABLE ONLY tbsituacaogeo
    ADD CONSTRAINT tbsituacaogeo_pkey PRIMARY KEY (id);


--
-- TOC entry 2217 (class 2606 OID 5839876)
-- Dependencies: 206 206 2295
-- Name: tbsituacaoprocesso_pkey; Type: CONSTRAINT; Schema: public; Owner: admin; Tablespace: 
--

ALTER TABLE ONLY tbsituacaoprocesso
    ADD CONSTRAINT tbsituacaoprocesso_pkey PRIMARY KEY (id);


--
-- TOC entry 2220 (class 2606 OID 5839894)
-- Dependencies: 208 208 2295
-- Name: tbstatuspendencia_pkey; Type: CONSTRAINT; Schema: public; Owner: admin; Tablespace: 
--

ALTER TABLE ONLY tbstatuspendencia
    ADD CONSTRAINT tbstatuspendencia_pkey PRIMARY KEY (id);


--
-- TOC entry 2223 (class 2606 OID 5839912)
-- Dependencies: 210 210 2295
-- Name: tbsubarea_pkey; Type: CONSTRAINT; Schema: public; Owner: admin; Tablespace: 
--

ALTER TABLE ONLY tbsubarea
    ADD CONSTRAINT tbsubarea_pkey PRIMARY KEY (id);


--
-- TOC entry 2226 (class 2606 OID 5839933)
-- Dependencies: 212 212 2295
-- Name: tbtipocaixa_pkey; Type: CONSTRAINT; Schema: public; Owner: admin; Tablespace: 
--

ALTER TABLE ONLY tbtipocaixa
    ADD CONSTRAINT tbtipocaixa_pkey PRIMARY KEY (id);


--
-- TOC entry 2229 (class 2606 OID 5839951)
-- Dependencies: 214 214 2295
-- Name: tbtipopendencia_pkey; Type: CONSTRAINT; Schema: public; Owner: admin; Tablespace: 
--

ALTER TABLE ONLY tbtipopendencia
    ADD CONSTRAINT tbtipopendencia_pkey PRIMARY KEY (id);


--
-- TOC entry 2233 (class 2606 OID 5839969)
-- Dependencies: 216 216 2295
-- Name: tbtipoprocesso_pkey; Type: CONSTRAINT; Schema: public; Owner: admin; Tablespace: 
--

ALTER TABLE ONLY tbtipoprocesso
    ADD CONSTRAINT tbtipoprocesso_pkey PRIMARY KEY (id);


--
-- TOC entry 2236 (class 2606 OID 5839992)
-- Dependencies: 218 218 2295
-- Name: tbuf_pkey; Type: CONSTRAINT; Schema: public; Owner: admin; Tablespace: 
--

ALTER TABLE ONLY tbuf
    ADD CONSTRAINT tbuf_pkey PRIMARY KEY (id);


--
-- TOC entry 2113 (class 1259 OID 5840024)
-- Dependencies: 161 2295
-- Name: auth_group_name_like; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX auth_group_name_like ON auth_group USING btree (name varchar_pattern_ops);


--
-- TOC entry 2116 (class 1259 OID 5840025)
-- Dependencies: 162 2295
-- Name: auth_group_permissions_group_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX auth_group_permissions_group_id ON auth_group_permissions USING btree (group_id);


--
-- TOC entry 2117 (class 1259 OID 5840026)
-- Dependencies: 162 2295
-- Name: auth_group_permissions_permission_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX auth_group_permissions_permission_id ON auth_group_permissions USING btree (permission_id);


--
-- TOC entry 2120 (class 1259 OID 5840027)
-- Dependencies: 163 2295
-- Name: auth_permission_content_type_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX auth_permission_content_type_id ON auth_permission USING btree (content_type_id);


--
-- TOC entry 2129 (class 1259 OID 5840031)
-- Dependencies: 167 2295
-- Name: auth_user_groups_group_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX auth_user_groups_group_id ON auth_user_groups USING btree (group_id);


--
-- TOC entry 2132 (class 1259 OID 5840030)
-- Dependencies: 167 2295
-- Name: auth_user_groups_user_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX auth_user_groups_user_id ON auth_user_groups USING btree (user_id);


--
-- TOC entry 2125 (class 1259 OID 5840029)
-- Dependencies: 165 2295
-- Name: auth_user_tbdivisao_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX auth_user_tbdivisao_id ON auth_user USING btree (tbdivisao_id);


--
-- TOC entry 2133 (class 1259 OID 5840033)
-- Dependencies: 168 2295
-- Name: auth_user_user_permissions_permission_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX auth_user_user_permissions_permission_id ON auth_user_user_permissions USING btree (permission_id);


--
-- TOC entry 2136 (class 1259 OID 5840032)
-- Dependencies: 168 2295
-- Name: auth_user_user_permissions_user_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX auth_user_user_permissions_user_id ON auth_user_user_permissions USING btree (user_id);


--
-- TOC entry 2128 (class 1259 OID 5840028)
-- Dependencies: 165 2295
-- Name: auth_user_username_like; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX auth_user_username_like ON auth_user USING btree (username varchar_pattern_ops);


--
-- TOC entry 2137 (class 1259 OID 5840035)
-- Dependencies: 169 2295
-- Name: django_admin_log_content_type_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX django_admin_log_content_type_id ON django_admin_log USING btree (content_type_id);


--
-- TOC entry 2140 (class 1259 OID 5840034)
-- Dependencies: 169 2295
-- Name: django_admin_log_user_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX django_admin_log_user_id ON django_admin_log USING btree (user_id);


--
-- TOC entry 2145 (class 1259 OID 5840036)
-- Dependencies: 171 2295
-- Name: django_session_session_key_like; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX django_session_session_key_like ON django_session USING btree (session_key varchar_pattern_ops);


--
-- TOC entry 2150 (class 1259 OID 5840037)
-- Dependencies: 174 2295
-- Name: tbcaixa_tbtipocaixa_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX tbcaixa_tbtipocaixa_id ON tbcaixa USING btree (tbtipocaixa_id);


--
-- TOC entry 2153 (class 1259 OID 5840038)
-- Dependencies: 176 2295
-- Name: tbclassificacaoprocesso_tbdivisao_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX tbclassificacaoprocesso_tbdivisao_id ON tbclassificacaoprocesso USING btree (tbdivisao_id);


--
-- TOC entry 2156 (class 1259 OID 5840039)
-- Dependencies: 178 2295
-- Name: tbcontrato_tbdivisao_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX tbcontrato_tbdivisao_id ON tbcontrato USING btree (tbdivisao_id);


--
-- TOC entry 2159 (class 1259 OID 5840040)
-- Dependencies: 180 2295
-- Name: tbdivisao_tbuf_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX tbdivisao_tbuf_id ON tbdivisao USING btree (tbuf_id);


--
-- TOC entry 2162 (class 1259 OID 5840041)
-- Dependencies: 182 2295
-- Name: tbgleba_tbsubarea_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX tbgleba_tbsubarea_id ON tbgleba USING btree (tbsubarea_id);


--
-- TOC entry 2163 (class 1259 OID 5840045)
-- Dependencies: 184 2295
-- Name: tbmovimentacao_auth_user_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX tbmovimentacao_auth_user_id ON tbmovimentacao USING btree (auth_user_id);


--
-- TOC entry 2166 (class 1259 OID 5840044)
-- Dependencies: 184 2295
-- Name: tbmovimentacao_tbcaixa_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX tbmovimentacao_tbcaixa_id ON tbmovimentacao USING btree (tbcaixa_id);


--
-- TOC entry 2167 (class 1259 OID 5840043)
-- Dependencies: 184 2295
-- Name: tbmovimentacao_tbcaixa_id_origem; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX tbmovimentacao_tbcaixa_id_origem ON tbmovimentacao USING btree (tbcaixa_id_origem);


--
-- TOC entry 2168 (class 1259 OID 5840042)
-- Dependencies: 184 2295
-- Name: tbmovimentacao_tbprocessobase_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX tbmovimentacao_tbprocessobase_id ON tbmovimentacao USING btree (tbprocessobase_id);


--
-- TOC entry 2169 (class 1259 OID 5840046)
-- Dependencies: 186 2295
-- Name: tbmunicipio_Codigo_UF; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX "tbmunicipio_Codigo_UF" ON tbmunicipio USING btree ("Codigo_UF");


--
-- TOC entry 2174 (class 1259 OID 5840048)
-- Dependencies: 188 2295
-- Name: tbpecastecnicas_tbcaixa_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX tbpecastecnicas_tbcaixa_id ON tbpecastecnicas USING btree (tbcaixa_id);


--
-- TOC entry 2175 (class 1259 OID 5840047)
-- Dependencies: 188 2295
-- Name: tbpecastecnicas_tbcontrato_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX tbpecastecnicas_tbcontrato_id ON tbpecastecnicas USING btree (tbcontrato_id);


--
-- TOC entry 2176 (class 1259 OID 5840050)
-- Dependencies: 188 2295
-- Name: tbpecastecnicas_tbdivisao_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX tbpecastecnicas_tbdivisao_id ON tbpecastecnicas USING btree (tbdivisao_id);


--
-- TOC entry 2177 (class 1259 OID 5840049)
-- Dependencies: 188 2295
-- Name: tbpecastecnicas_tbgleba_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX tbpecastecnicas_tbgleba_id ON tbpecastecnicas USING btree (tbgleba_id);


--
-- TOC entry 2178 (class 1259 OID 5840053)
-- Dependencies: 190 2295
-- Name: tbpendencia_auth_user_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX tbpendencia_auth_user_id ON tbpendencia USING btree (auth_user_id);


--
-- TOC entry 2181 (class 1259 OID 5840051)
-- Dependencies: 190 2295
-- Name: tbpendencia_tbprocessobase_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX tbpendencia_tbprocessobase_id ON tbpendencia USING btree (tbprocessobase_id);


--
-- TOC entry 2182 (class 1259 OID 5840054)
-- Dependencies: 190 2295
-- Name: tbpendencia_tbstatuspendencia_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX tbpendencia_tbstatuspendencia_id ON tbpendencia USING btree (tbstatuspendencia_id);


--
-- TOC entry 2183 (class 1259 OID 5840052)
-- Dependencies: 190 2295
-- Name: tbpendencia_tbtipopendencia_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX tbpendencia_tbtipopendencia_id ON tbpendencia USING btree (tbtipopendencia_id);


--
-- TOC entry 2239 (class 1259 OID 5840080)
-- Dependencies: 220 2295
-- Name: tbpregao_tbdivisao_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX tbpregao_tbdivisao_id ON tbpregao USING btree (tbdivisao_id);


--
-- TOC entry 2184 (class 1259 OID 5840058)
-- Dependencies: 192 2295
-- Name: tbprocessobase_auth_user_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX tbprocessobase_auth_user_id ON tbprocessobase USING btree (auth_user_id);


--
-- TOC entry 2187 (class 1259 OID 5840056)
-- Dependencies: 192 2295
-- Name: tbprocessobase_tbcaixa_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX tbprocessobase_tbcaixa_id ON tbprocessobase USING btree (tbcaixa_id);


--
-- TOC entry 2188 (class 1259 OID 5840061)
-- Dependencies: 192 2295
-- Name: tbprocessobase_tbclassificacaoprocesso_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX tbprocessobase_tbclassificacaoprocesso_id ON tbprocessobase USING btree (tbclassificacaoprocesso_id);


--
-- TOC entry 2189 (class 1259 OID 5840062)
-- Dependencies: 192 2295
-- Name: tbprocessobase_tbdivisao_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX tbprocessobase_tbdivisao_id ON tbprocessobase USING btree (tbdivisao_id);


--
-- TOC entry 2190 (class 1259 OID 5840055)
-- Dependencies: 192 2295
-- Name: tbprocessobase_tbgleba_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX tbprocessobase_tbgleba_id ON tbprocessobase USING btree (tbgleba_id);


--
-- TOC entry 2191 (class 1259 OID 5840057)
-- Dependencies: 192 2295
-- Name: tbprocessobase_tbmunicipio_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX tbprocessobase_tbmunicipio_id ON tbprocessobase USING btree (tbmunicipio_id);


--
-- TOC entry 2192 (class 1259 OID 5840060)
-- Dependencies: 192 2295
-- Name: tbprocessobase_tbsituacaoprocesso_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX tbprocessobase_tbsituacaoprocesso_id ON tbprocessobase USING btree (tbsituacaoprocesso_id);


--
-- TOC entry 2193 (class 1259 OID 5840059)
-- Dependencies: 192 2295
-- Name: tbprocessobase_tbtipoprocesso_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX tbprocessobase_tbtipoprocesso_id ON tbprocessobase USING btree (tbtipoprocesso_id);


--
-- TOC entry 2196 (class 1259 OID 5840063)
-- Dependencies: 194 2295
-- Name: tbprocessoclausula_tbprocessobase_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX tbprocessoclausula_tbprocessobase_id ON tbprocessoclausula USING btree (tbprocessobase_id);


--
-- TOC entry 2199 (class 1259 OID 5840064)
-- Dependencies: 196 2295
-- Name: tbprocessorural_tbprocessobase_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX tbprocessorural_tbprocessobase_id ON tbprocessorural USING btree (tbprocessobase_id);


--
-- TOC entry 2200 (class 1259 OID 5840067)
-- Dependencies: 198 2295
-- Name: tbprocessosanexos_auth_user_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX tbprocessosanexos_auth_user_id ON tbprocessosanexos USING btree (auth_user_id);


--
-- TOC entry 2203 (class 1259 OID 5840065)
-- Dependencies: 198 2295
-- Name: tbprocessosanexos_tbprocessobase_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX tbprocessosanexos_tbprocessobase_id ON tbprocessosanexos USING btree (tbprocessobase_id);


--
-- TOC entry 2204 (class 1259 OID 5840066)
-- Dependencies: 198 2295
-- Name: tbprocessosanexos_tbprocessobase_id_anexo; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX tbprocessosanexos_tbprocessobase_id_anexo ON tbprocessosanexos USING btree (tbprocessobase_id_anexo);


--
-- TOC entry 2207 (class 1259 OID 5840070)
-- Dependencies: 200 2295
-- Name: tbprocessourbano_tbcontrato_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX tbprocessourbano_tbcontrato_id ON tbprocessourbano USING btree (tbcontrato_id);


--
-- TOC entry 2208 (class 1259 OID 5840069)
-- Dependencies: 200 2295
-- Name: tbprocessourbano_tbpregao_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX tbprocessourbano_tbpregao_id ON tbprocessourbano USING btree (tbpregao_id);


--
-- TOC entry 2209 (class 1259 OID 5840068)
-- Dependencies: 200 2295
-- Name: tbprocessourbano_tbprocessobase_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX tbprocessourbano_tbprocessobase_id ON tbprocessourbano USING btree (tbprocessobase_id);


--
-- TOC entry 2210 (class 1259 OID 5840071)
-- Dependencies: 200 2295
-- Name: tbprocessourbano_tbsituacaogeo_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX tbprocessourbano_tbsituacaogeo_id ON tbprocessourbano USING btree (tbsituacaogeo_id);


--
-- TOC entry 2215 (class 1259 OID 5840072)
-- Dependencies: 204 2295
-- Name: tbsituacaogeo_tbdivisao_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX tbsituacaogeo_tbdivisao_id ON tbsituacaogeo USING btree (tbdivisao_id);


--
-- TOC entry 2218 (class 1259 OID 5840073)
-- Dependencies: 206 2295
-- Name: tbsituacaoprocesso_tbdivisao_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX tbsituacaoprocesso_tbdivisao_id ON tbsituacaoprocesso USING btree (tbdivisao_id);


--
-- TOC entry 2221 (class 1259 OID 5840074)
-- Dependencies: 208 2295
-- Name: tbstatuspendencia_tbdivisao_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX tbstatuspendencia_tbdivisao_id ON tbstatuspendencia USING btree (tbdivisao_id);


--
-- TOC entry 2224 (class 1259 OID 5840075)
-- Dependencies: 210 2295
-- Name: tbsubarea_tbdivisao_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX tbsubarea_tbdivisao_id ON tbsubarea USING btree (tbdivisao_id);


--
-- TOC entry 2227 (class 1259 OID 5840076)
-- Dependencies: 212 2295
-- Name: tbtipocaixa_tbdivisao_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX tbtipocaixa_tbdivisao_id ON tbtipocaixa USING btree (tbdivisao_id);


--
-- TOC entry 2230 (class 1259 OID 5840077)
-- Dependencies: 214 2295
-- Name: tbtipopendencia_tbdivisao_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX tbtipopendencia_tbdivisao_id ON tbtipopendencia USING btree (tbdivisao_id);


--
-- TOC entry 2231 (class 1259 OID 5840078)
-- Dependencies: 214 2295
-- Name: tbtipopendencia_tbtipoprocesso_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX tbtipopendencia_tbtipoprocesso_id ON tbtipopendencia USING btree (tbtipoprocesso_id);


--
-- TOC entry 2234 (class 1259 OID 5840079)
-- Dependencies: 216 2295
-- Name: tbtipoprocesso_tbdivisao_id; Type: INDEX; Schema: public; Owner: admin; Tablespace: 
--

CREATE INDEX tbtipoprocesso_tbdivisao_id ON tbtipoprocesso USING btree (tbdivisao_id);


--
-- TOC entry 2259 (class 2606 OID 5839998)
-- Dependencies: 2235 186 218 2295
-- Name: Codigo_UF_refs_id_29984a75; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbmunicipio
    ADD CONSTRAINT "Codigo_UF_refs_id_29984a75" FOREIGN KEY ("Codigo_UF") REFERENCES tbuf(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2240 (class 2606 OID 5839481)
-- Dependencies: 2114 162 161 2295
-- Name: auth_group_permissions_group_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY auth_group_permissions
    ADD CONSTRAINT auth_group_permissions_group_id_fkey FOREIGN KEY (group_id) REFERENCES auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2245 (class 2606 OID 5839519)
-- Dependencies: 167 161 2114 2295
-- Name: auth_user_groups_group_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY auth_user_groups
    ADD CONSTRAINT auth_user_groups_group_id_fkey FOREIGN KEY (group_id) REFERENCES auth_group(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2244 (class 2606 OID 5839514)
-- Dependencies: 165 167 2123 2295
-- Name: auth_user_groups_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY auth_user_groups
    ADD CONSTRAINT auth_user_groups_user_id_fkey FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2247 (class 2606 OID 5839534)
-- Dependencies: 168 163 2121 2295
-- Name: auth_user_user_permissions_permission_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_permission_id_fkey FOREIGN KEY (permission_id) REFERENCES auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2246 (class 2606 OID 5839529)
-- Dependencies: 168 2123 165 2295
-- Name: auth_user_user_permissions_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY auth_user_user_permissions
    ADD CONSTRAINT auth_user_user_permissions_user_id_fkey FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2249 (class 2606 OID 5839562)
-- Dependencies: 169 2141 170 2295
-- Name: content_type_id_refs_id_93d2d1f8; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY django_admin_log
    ADD CONSTRAINT content_type_id_refs_id_93d2d1f8 FOREIGN KEY (content_type_id) REFERENCES django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2242 (class 2606 OID 5839557)
-- Dependencies: 2141 163 170 2295
-- Name: content_type_id_refs_id_d043b34a; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY auth_permission
    ADD CONSTRAINT content_type_id_refs_id_d043b34a FOREIGN KEY (content_type_id) REFERENCES django_content_type(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2248 (class 2606 OID 5839547)
-- Dependencies: 169 2123 165 2295
-- Name: django_admin_log_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY django_admin_log
    ADD CONSTRAINT django_admin_log_user_id_fkey FOREIGN KEY (user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2241 (class 2606 OID 5839491)
-- Dependencies: 2121 162 163 2295
-- Name: permission_id_refs_id_6ba0f519; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY auth_group_permissions
    ADD CONSTRAINT permission_id_refs_id_6ba0f519 FOREIGN KEY (permission_id) REFERENCES auth_permission(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2251 (class 2606 OID 5839620)
-- Dependencies: 2157 180 176 2295
-- Name: tbdivisao_id_refs_id_00d25a11; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbclassificacaoprocesso
    ADD CONSTRAINT tbdivisao_id_refs_id_00d25a11 FOREIGN KEY (tbdivisao_id) REFERENCES tbdivisao(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2243 (class 2606 OID 5839615)
-- Dependencies: 180 165 2157 2295
-- Name: tbdivisao_id_refs_id_209f7cf0; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY auth_user
    ADD CONSTRAINT tbdivisao_id_refs_id_209f7cf0 FOREIGN KEY (tbdivisao_id) REFERENCES tbdivisao(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2252 (class 2606 OID 5839625)
-- Dependencies: 2157 180 178 2295
-- Name: tbdivisao_id_refs_id_c808e225; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbcontrato
    ADD CONSTRAINT tbdivisao_id_refs_id_c808e225 FOREIGN KEY (tbdivisao_id) REFERENCES tbdivisao(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2257 (class 2606 OID 5839656)
-- Dependencies: 165 184 2123 2295
-- Name: tbmovimentacao_auth_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbmovimentacao
    ADD CONSTRAINT tbmovimentacao_auth_user_id_fkey FOREIGN KEY (auth_user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2256 (class 2606 OID 5839651)
-- Dependencies: 174 2148 184 2295
-- Name: tbmovimentacao_tbcaixa_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbmovimentacao
    ADD CONSTRAINT tbmovimentacao_tbcaixa_id_fkey FOREIGN KEY (tbcaixa_id) REFERENCES tbcaixa(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2255 (class 2606 OID 5839646)
-- Dependencies: 184 174 2148 2295
-- Name: tbmovimentacao_tbcaixa_id_origem_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbmovimentacao
    ADD CONSTRAINT tbmovimentacao_tbcaixa_id_origem_fkey FOREIGN KEY (tbcaixa_id_origem) REFERENCES tbcaixa(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2261 (class 2606 OID 5839685)
-- Dependencies: 174 188 2148 2295
-- Name: tbpecastecnicas_tbcaixa_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbpecastecnicas
    ADD CONSTRAINT tbpecastecnicas_tbcaixa_id_fkey FOREIGN KEY (tbcaixa_id) REFERENCES tbcaixa(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2260 (class 2606 OID 5839680)
-- Dependencies: 188 2154 178 2295
-- Name: tbpecastecnicas_tbcontrato_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbpecastecnicas
    ADD CONSTRAINT tbpecastecnicas_tbcontrato_id_fkey FOREIGN KEY (tbcontrato_id) REFERENCES tbcontrato(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2263 (class 2606 OID 5839695)
-- Dependencies: 2157 180 188 2295
-- Name: tbpecastecnicas_tbdivisao_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbpecastecnicas
    ADD CONSTRAINT tbpecastecnicas_tbdivisao_id_fkey FOREIGN KEY (tbdivisao_id) REFERENCES tbdivisao(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2262 (class 2606 OID 5839690)
-- Dependencies: 182 2160 188 2295
-- Name: tbpecastecnicas_tbgleba_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbpecastecnicas
    ADD CONSTRAINT tbpecastecnicas_tbgleba_id_fkey FOREIGN KEY (tbgleba_id) REFERENCES tbgleba(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2264 (class 2606 OID 5839711)
-- Dependencies: 165 2123 190 2295
-- Name: tbpendencia_auth_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbpendencia
    ADD CONSTRAINT tbpendencia_auth_user_id_fkey FOREIGN KEY (auth_user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2284 (class 2606 OID 5840019)
-- Dependencies: 2237 220 200 2295
-- Name: tbpregao_id_refs_id_f323926f; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbprocessourbano
    ADD CONSTRAINT tbpregao_id_refs_id_f323926f FOREIGN KEY (tbpregao_id) REFERENCES tbpregao(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2293 (class 2606 OID 5840014)
-- Dependencies: 180 2157 220 2295
-- Name: tbpregao_tbdivisao_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbpregao
    ADD CONSTRAINT tbpregao_tbdivisao_id_fkey FOREIGN KEY (tbdivisao_id) REFERENCES tbdivisao(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2271 (class 2606 OID 5839739)
-- Dependencies: 192 2123 165 2295
-- Name: tbprocessobase_auth_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbprocessobase
    ADD CONSTRAINT tbprocessobase_auth_user_id_fkey FOREIGN KEY (auth_user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2258 (class 2606 OID 5839754)
-- Dependencies: 184 192 2185 2295
-- Name: tbprocessobase_id_refs_id_5aebc46a; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbmovimentacao
    ADD CONSTRAINT tbprocessobase_id_refs_id_5aebc46a FOREIGN KEY (tbprocessobase_id) REFERENCES tbprocessobase(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2265 (class 2606 OID 5839759)
-- Dependencies: 2185 192 190 2295
-- Name: tbprocessobase_id_refs_id_86d3804c; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbpendencia
    ADD CONSTRAINT tbprocessobase_id_refs_id_86d3804c FOREIGN KEY (tbprocessobase_id) REFERENCES tbprocessobase(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2269 (class 2606 OID 5839729)
-- Dependencies: 192 174 2148 2295
-- Name: tbprocessobase_tbcaixa_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbprocessobase
    ADD CONSTRAINT tbprocessobase_tbcaixa_id_fkey FOREIGN KEY (tbcaixa_id) REFERENCES tbcaixa(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2272 (class 2606 OID 5839744)
-- Dependencies: 2151 192 176 2295
-- Name: tbprocessobase_tbclassificacaoprocesso_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbprocessobase
    ADD CONSTRAINT tbprocessobase_tbclassificacaoprocesso_id_fkey FOREIGN KEY (tbclassificacaoprocesso_id) REFERENCES tbclassificacaoprocesso(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2273 (class 2606 OID 5839749)
-- Dependencies: 180 192 2157 2295
-- Name: tbprocessobase_tbdivisao_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbprocessobase
    ADD CONSTRAINT tbprocessobase_tbdivisao_id_fkey FOREIGN KEY (tbdivisao_id) REFERENCES tbdivisao(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2268 (class 2606 OID 5839724)
-- Dependencies: 2160 192 182 2295
-- Name: tbprocessobase_tbgleba_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbprocessobase
    ADD CONSTRAINT tbprocessobase_tbgleba_id_fkey FOREIGN KEY (tbgleba_id) REFERENCES tbgleba(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2270 (class 2606 OID 5839734)
-- Dependencies: 186 192 2170 2295
-- Name: tbprocessobase_tbmunicipio_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbprocessobase
    ADD CONSTRAINT tbprocessobase_tbmunicipio_id_fkey FOREIGN KEY (tbmunicipio_id) REFERENCES tbmunicipio(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2276 (class 2606 OID 5839775)
-- Dependencies: 2185 194 192 2295
-- Name: tbprocessoclausula_tbprocessobase_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbprocessoclausula
    ADD CONSTRAINT tbprocessoclausula_tbprocessobase_id_fkey FOREIGN KEY (tbprocessobase_id) REFERENCES tbprocessobase(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2277 (class 2606 OID 5839788)
-- Dependencies: 192 2185 196 2295
-- Name: tbprocessorural_tbprocessobase_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbprocessorural
    ADD CONSTRAINT tbprocessorural_tbprocessobase_id_fkey FOREIGN KEY (tbprocessobase_id) REFERENCES tbprocessobase(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2280 (class 2606 OID 5839811)
-- Dependencies: 198 165 2123 2295
-- Name: tbprocessosanexos_auth_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbprocessosanexos
    ADD CONSTRAINT tbprocessosanexos_auth_user_id_fkey FOREIGN KEY (auth_user_id) REFERENCES auth_user(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2279 (class 2606 OID 5839806)
-- Dependencies: 198 2185 192 2295
-- Name: tbprocessosanexos_tbprocessobase_id_anexo_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbprocessosanexos
    ADD CONSTRAINT tbprocessosanexos_tbprocessobase_id_anexo_fkey FOREIGN KEY (tbprocessobase_id_anexo) REFERENCES tbprocessobase(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2278 (class 2606 OID 5839801)
-- Dependencies: 198 192 2185 2295
-- Name: tbprocessosanexos_tbprocessobase_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbprocessosanexos
    ADD CONSTRAINT tbprocessosanexos_tbprocessobase_id_fkey FOREIGN KEY (tbprocessobase_id) REFERENCES tbprocessobase(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2282 (class 2606 OID 5839829)
-- Dependencies: 2154 200 178 2295
-- Name: tbprocessourbano_tbcontrato_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbprocessourbano
    ADD CONSTRAINT tbprocessourbano_tbcontrato_id_fkey FOREIGN KEY (tbcontrato_id) REFERENCES tbcontrato(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2281 (class 2606 OID 5839824)
-- Dependencies: 192 200 2185 2295
-- Name: tbprocessourbano_tbprocessobase_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbprocessourbano
    ADD CONSTRAINT tbprocessourbano_tbprocessobase_id_fkey FOREIGN KEY (tbprocessobase_id) REFERENCES tbprocessobase(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2283 (class 2606 OID 5839861)
-- Dependencies: 2213 200 204 2295
-- Name: tbsituacaogeo_id_refs_id_f9087efb; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbprocessourbano
    ADD CONSTRAINT tbsituacaogeo_id_refs_id_f9087efb FOREIGN KEY (tbsituacaogeo_id) REFERENCES tbsituacaogeo(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2285 (class 2606 OID 5839856)
-- Dependencies: 204 2157 180 2295
-- Name: tbsituacaogeo_tbdivisao_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbsituacaogeo
    ADD CONSTRAINT tbsituacaogeo_tbdivisao_id_fkey FOREIGN KEY (tbdivisao_id) REFERENCES tbdivisao(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2274 (class 2606 OID 5839882)
-- Dependencies: 192 2216 206 2295
-- Name: tbsituacaoprocesso_id_refs_id_bfef2fda; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbprocessobase
    ADD CONSTRAINT tbsituacaoprocesso_id_refs_id_bfef2fda FOREIGN KEY (tbsituacaoprocesso_id) REFERENCES tbsituacaoprocesso(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2286 (class 2606 OID 5839877)
-- Dependencies: 2157 180 206 2295
-- Name: tbsituacaoprocesso_tbdivisao_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbsituacaoprocesso
    ADD CONSTRAINT tbsituacaoprocesso_tbdivisao_id_fkey FOREIGN KEY (tbdivisao_id) REFERENCES tbdivisao(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2266 (class 2606 OID 5839900)
-- Dependencies: 208 2219 190 2295
-- Name: tbstatuspendencia_id_refs_id_615418ce; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbpendencia
    ADD CONSTRAINT tbstatuspendencia_id_refs_id_615418ce FOREIGN KEY (tbstatuspendencia_id) REFERENCES tbstatuspendencia(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2287 (class 2606 OID 5839895)
-- Dependencies: 208 180 2157 2295
-- Name: tbstatuspendencia_tbdivisao_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbstatuspendencia
    ADD CONSTRAINT tbstatuspendencia_tbdivisao_id_fkey FOREIGN KEY (tbdivisao_id) REFERENCES tbdivisao(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2254 (class 2606 OID 5839918)
-- Dependencies: 210 2222 182 2295
-- Name: tbsubarea_id_refs_id_c3c14a3b; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbgleba
    ADD CONSTRAINT tbsubarea_id_refs_id_c3c14a3b FOREIGN KEY (tbsubarea_id) REFERENCES tbsubarea(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2288 (class 2606 OID 5839913)
-- Dependencies: 210 2157 180 2295
-- Name: tbsubarea_tbdivisao_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbsubarea
    ADD CONSTRAINT tbsubarea_tbdivisao_id_fkey FOREIGN KEY (tbdivisao_id) REFERENCES tbdivisao(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2250 (class 2606 OID 5839939)
-- Dependencies: 212 2225 174 2295
-- Name: tbtipocaixa_id_refs_id_1f3d944c; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbcaixa
    ADD CONSTRAINT tbtipocaixa_id_refs_id_1f3d944c FOREIGN KEY (tbtipocaixa_id) REFERENCES tbtipocaixa(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2289 (class 2606 OID 5839934)
-- Dependencies: 212 180 2157 2295
-- Name: tbtipocaixa_tbdivisao_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbtipocaixa
    ADD CONSTRAINT tbtipocaixa_tbdivisao_id_fkey FOREIGN KEY (tbdivisao_id) REFERENCES tbdivisao(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2267 (class 2606 OID 5839957)
-- Dependencies: 214 2228 190 2295
-- Name: tbtipopendencia_id_refs_id_4f9053c1; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbpendencia
    ADD CONSTRAINT tbtipopendencia_id_refs_id_4f9053c1 FOREIGN KEY (tbtipopendencia_id) REFERENCES tbtipopendencia(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2290 (class 2606 OID 5839952)
-- Dependencies: 214 2157 180 2295
-- Name: tbtipopendencia_tbdivisao_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbtipopendencia
    ADD CONSTRAINT tbtipopendencia_tbdivisao_id_fkey FOREIGN KEY (tbdivisao_id) REFERENCES tbdivisao(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2291 (class 2606 OID 5839980)
-- Dependencies: 216 214 2232 2295
-- Name: tbtipoprocesso_id_refs_id_14dae0cf; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbtipopendencia
    ADD CONSTRAINT tbtipoprocesso_id_refs_id_14dae0cf FOREIGN KEY (tbtipoprocesso_id) REFERENCES tbtipoprocesso(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2275 (class 2606 OID 5839975)
-- Dependencies: 216 2232 192 2295
-- Name: tbtipoprocesso_id_refs_id_64d671a3; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbprocessobase
    ADD CONSTRAINT tbtipoprocesso_id_refs_id_64d671a3 FOREIGN KEY (tbtipoprocesso_id) REFERENCES tbtipoprocesso(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2292 (class 2606 OID 5839970)
-- Dependencies: 216 180 2157 2295
-- Name: tbtipoprocesso_tbdivisao_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbtipoprocesso
    ADD CONSTRAINT tbtipoprocesso_tbdivisao_id_fkey FOREIGN KEY (tbdivisao_id) REFERENCES tbdivisao(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2253 (class 2606 OID 5839993)
-- Dependencies: 2235 218 180 2295
-- Name: tbuf_id_refs_id_c8d633fb; Type: FK CONSTRAINT; Schema: public; Owner: admin
--

ALTER TABLE ONLY tbdivisao
    ADD CONSTRAINT tbuf_id_refs_id_c8d633fb FOREIGN KEY (tbuf_id) REFERENCES tbuf(id) DEFERRABLE INITIALLY DEFERRED;


--
-- TOC entry 2300 (class 0 OID 0)
-- Dependencies: 5
-- Name: public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM postgres;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO PUBLIC;


-- Completed on 2013-11-07 15:52:12 BRT

--
-- PostgreSQL database dump complete
--

