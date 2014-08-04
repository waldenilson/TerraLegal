-- Table: tbetapaanterior

-- DROP TABLE tbetapaanterior;

CREATE TABLE tbetapaanterior
(
  id serial NOT NULL,
  tbetapa_id integer,
  tbanterior integer,
  CONSTRAINT pk_tbetapaanterior PRIMARY KEY (id ),
  CONSTRAINT fk_tbetapa FOREIGN KEY (tbetapa_id)
      REFERENCES tbetapa (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION
)
WITH (
  OIDS=FALSE
);
ALTER TABLE tbetapaanterior
  OWNER TO admin;

  
  -- Table: tbetapaposterior

-- DROP TABLE tbetapaposterior;

CREATE TABLE tbetapaposterior
(
  id serial NOT NULL,
  tbetapa_id integer,
  tbposterior integer,
  blsequencia boolean NOT NULL,
  CONSTRAINT pk_tbetapaposterior PRIMARY KEY (id ),
  CONSTRAINT fk_tbetapa FOREIGN KEY (tbetapa_id)
      REFERENCES tbetapa (id) MATCH SIMPLE
      ON UPDATE NO ACTION ON DELETE NO ACTION
)
WITH (
  OIDS=FALSE
);
ALTER TABLE tbetapaposterior
  OWNER TO admin;
