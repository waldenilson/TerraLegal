-----------------------------------------------------------------------------
--CRIACAO E ALTERACAO DE TABELAS PARA SUPORTE A LIVRO FUNDIARIO
-----------------------------------------------------------------------------
alter table tbprocessobase add column nmendereco text;
alter table tbprocessobase add column nmcontato text;

-----------------------------------------------------------------------------
--CRIACAO  DE TABELA DE TIPO DE TITULO
-----------------------------------------------------------------------------

CREATE TABLE tbtipotitulo
(
  cdtipo character varying(10) NOT NULL,
  dstipo character varying(50) NOT NULL,
  id serial NOT NULL,
  CONSTRAINT tbtipotitulo_pkey PRIMARY KEY (id)
)
WITH (
  OIDS=FALSE
);
ALTER TABLE tbtipotitulo
  OWNER TO admin;
  
INSERT INTO tbtipotitulo(cdtipo, dstipo, id)
    VALUES ('TD','Titulo definitivo',1),('CDRU','Concessao',2);

-----------------------------------------------------------------------------
--CRIACAO  DE TABELA DE STATUS DE TITULO
-----------------------------------------------------------------------------
CREATE TABLE tbstatustitulo
(
  id serial NOT NULL,
  sttitulo character varying(30) NOT NULL,
  CONSTRAINT tbstatustitulo_pkey PRIMARY KEY (id)
)
WITH (OIDS=FALSE);
ALTER TABLE tbstatustitulo OWNER TO admin;


INSERT INTO tbstatustitulo(id, sttitulo)
    VALUES (1,'ENTREGUE'),(2,'NAO ENTREGUE'),(3,'PENDENTE ASSINATURA'),(4,'PENDENCIAS');

-----------------------------------------------------------------------------
--CRIACAO DE TABELA DE TITULOS
-----------------------------------------------------------------------------
CREATE TABLE tbtitulo
(
  cdtitulo character varying(8) NOT NULL,
  tbprocessobase_id integer NOT NULL,
  tbstatustitulo_id integer NOT NULL,
  tbtipotitulo_id integer NOT NULL,
  id serial NOT NULL,
  CONSTRAINT tbtitulo_pkey PRIMARY KEY (id),
  CONSTRAINT tbtitulo_tbprocessobase_id_fkey FOREIGN KEY (tbprocessobase_id)
      REFERENCES tbprocessobase (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION DEFERRABLE INITIALLY DEFERRED,
  CONSTRAINT tbtitulo_tbstatustitulo_id_fkey FOREIGN KEY (tbstatustitulo_id)
      REFERENCES tbstatustitulo (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION DEFERRABLE INITIALLY DEFERRED,
  CONSTRAINT tbtitulo_tbtipotitulo_id_fkey FOREIGN KEY (tbtipotitulo_id)
      REFERENCES tbtipotitulo (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION DEFERRABLE INITIALLY DEFERRED
)
WITH (
  OIDS=FALSE
);
ALTER TABLE tbtitulo
  OWNER TO admin;
