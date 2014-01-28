--criacao de campo em tabela de sevidores para indicar o tipo de servidor
ALTER TABLE tbservidor ADD COLUMN nmcontrato character varying(20);

--tabela para gerir todos os tipos de situacos usado pelo sistema  
 CREATE TABLE tbsituacao
(
  id serial NOT NULL,
  "cdTabela" character varying(30) NOT NULL,
  "dsSituacao" character varying(50) NOT NULL,
  CONSTRAINT tbsituacao_pkey PRIMARY KEY (id)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE tbsituacao
  OWNER TO admin;

--criacao de tabela de ferias dos servidores
CREATE TABLE tbferias
(
  id serial NOT NULL,
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
  "stSituacao_id" integer NOT NULL,
  CONSTRAINT tbferias_pkey PRIMARY KEY (id),
  CONSTRAINT "stSituacao_id_refs_id_c9e2ca6b" FOREIGN KEY ("stSituacao_id")
      REFERENCES tbsituacao (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION DEFERRABLE INITIALLY DEFERRED,
  CONSTRAINT tbferias_tbservidor_id_fkey FOREIGN KEY (tbservidor_id)
      REFERENCES tbservidor (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION DEFERRABLE INITIALLY DEFERRED
)
WITH (
  OIDS=FALSE
);
ALTER TABLE tbferias
  OWNER TO admin;

  
  
  
