-- creation de la base SDC
CREATE DATABASE "SDC"
  WITH ENCODING='UTF8'
       OWNER=yassine
       CONNECTION LIMIT=-1;


-- creation de table
create table test (
	id integer primary key,
	dateValidation timestamp without time zone,
	numProduit integer,
	lcpt char(20),
	nb1Montees integer,
	nbCorresp integer,
	nbValidations integer,
	dirValidation integer,
	numLieu integer,
	libelleArret char(20),
	codeEmplacement char(20),
	codeSite char(10),
	llpt char(20),
	typeSupport integer,
	lts char(20)
	);

-- OR

create table test4 (
	dateValidation timestamp without time zone,
	numProduit integer,
	lcpt char(20),
	nb1Montees integer,
	nbCorresp integer,
	nbValidations integer,
	dirValidation integer,
	numLieu integer,
	libelleArret char(20),
	codeEmplacement char(20),
	codeSite char(10),
	llpt char(20),
	typeSupport integer,
	lts char(20)
	);

	-- remplir la table

COPY test4
FROM 'C:\Program Files\PostgreSQL\9.5\CSV\tvj1.csv'
WITH DELIMITER ',';

-----------------------------------------------------------------------------------------
-- creation de la base SDD

CREATE DATABASE "SDD"
  WITH ENCODING='UTF8'
       OWNER=yassine
       CONNECTION LIMIT=-1;


-- creation table

create table test3 (
	dthrOperation timestamp without time zone,
	th integer,
	tqh char(6),
	jourValidation timestamp without time zone,
	moisValidation char(7),
	nb1Montees int,
	numLieu int,
	libelArret char(20)
	);

-- remplir la table

COPY test3
FROM 'C:\Program Files\PostgreSQL\9.5\CSV\sdd_6_16.csv'
WITH DELIMITER ',';

-- exemple de traitement personaliser

select numlieu from test3 order by dthroperation desc, libelarret desc;