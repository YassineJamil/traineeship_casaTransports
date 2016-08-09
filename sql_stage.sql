-- creation de la base SDC
CREATE DATABASE "SDC"
  WITH ENCODING='UTF8'
       OWNER=yassine
       CONNECTION LIMIT=-1;


-- creation de table
create table test4 (
	dateValidation date,
	numProduit integer,
	libelleCourtProduitTitre char(20),
	nb1ereMontees integer,
	nbCorresp integer,
	nbValidations integer,
	directionValidation integer,
	numLieu integer,
	libelleArret char(20),
	codeEmplacement char(20),
	codeSite char(10),
	libelleLongProduitTitre char(20),
	typeSupport integer,
	libelleTypeSupport char(20)
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

--------------------------------------------------------------------

-- changement de directionvalidation ... SDC **


select * from avril_20ALTER TABLE avril_2016
ALTER COLUMN directionvalidation TYPE char(10);

UPDATE avril_2016
SET directionvalidation = 'entree'
WHERE directionvalidation = '1';

UPDATE avril_2016
SET directionvalidation = 'sortie'
WHERE directionvalidation = '2';16 where directionvalidation ='entree';

----------------------------------------------------------------------
--traitement de la somme

drop table if exists somme;
create table somme (
datevalidation date,
sommenb1eremonteesentree int,
sommenbcorrespentree int,
sommenbvalidationsentree int,
sommenb1eremonteessortie int,
sommenbcorrespsortie int,
sommenbvalidationssortie int );
insert into somme (datevalidation, sommenb1eremonteesentree, sommenbcorrespentree, sommenbvalidationsentree, sommenb1eremonteessortie, sommenbcorrespsortie, sommenbvalidationssortie )
SELECT datevalidation ,SUM(nb1eremontees) ,SUM(nbcorresp),SUM(nbvalidations)
FROM test
GROUP BY datevalidation;

---------------------------------------------------------------------------------
-- extraire le mois

select * from mai_2016 where extract(month from datevalidation) = '05';

---------------------------------------------------------------------------------
-- le traitement d'un mois

drop table if exists somme;
create table somme (
datevalidation date,
sommenb1eremonteeentree int,
sommenb1eremonteesortie int,
sommenbcorrespentree int,
sommenbcorrespsortie int,
sommenbvalidationsentree int,
sommenbvalidationssortie int );

drop table if exists sommeentree;
create table sommeentree (
datevalidation date,
sommenb1eremonteeentree int,
sommenbcorrespentree int,
sommenbvalidationsentree int);
insert into sommeentree
SELECT datevalidation ,SUM(nb1eremontees),SUM(nbcorresp),SUM(nbvalidations)
FROM mai_2016
where directionvalidation = 'entree'
GROUP BY datevalidation;

drop table if exists sommesortie;
create table sommesortie (
datevalidation date,
sommenb1eremonteesortie int,
sommenbcorrespsortie int,
sommenbvalidationssortie int);
insert into sommesortie
SELECT datevalidation ,SUM(nb1eremontees),SUM(nbcorresp),SUM(nbvalidations)
FROM mai_2016
where directionvalidation = 'sortie'
GROUP BY datevalidation;

insert into somme
SELECT sommeentree.datevalidation, sommenb1eremonteeentree,  sommenb1eremonteesortie, sommenbcorrespentree, sommenbcorrespsortie, sommenbvalidationsentree, sommenbvalidationssortie
    FROM sommeentree, sommesortie
    WHERE sommeentree.datevalidation = sommesortie.datevalidation;

-- ordonnement de somme create table sommebuffer (like somme);

insert into sommebuffer
select * from somme order by datevalidation;

delete from somme;

insert into somme
select * from sommebuffer;



-- script complet de creation de table et de son remplissage, ne pas oublier de bien mentionner la date

create table janvier_2015 (
	dateValidation date,
	numProduit integer,
	libelleCourtProduitTitre char(20),
	nb1ereMontees integer,
	nbCorresp integer,
	nbValidations integer,
	directionValidation integer,
	numLieu integer,
	libelleArret char(20),
	codeEmplacement char(20),
	codeSite char(10),
	libelleLongProduitTitre char(20),
	typeSupport integer,
	libelleTypeSupport char(20)
	);

COPY janvier_2015
FROM 'C:/Program Files/PostgreSQL/9.5/CSV/sdc_1_15.csv'
WITH DELIMITER ',';

ALTER TABLE janvier_2015
ALTER COLUMN directionvalidation TYPE char(10);

UPDATE janvier_2015
SET directionvalidation = 'entree'
WHERE directionvalidation = '1';

UPDATE janvier_2015
SET directionvalidation = 'sortie'
WHERE directionvalidation = '2';

-- SDD script complet de creation de table et de son remplissage, ne pas oublier de bien mentionner la date

CREATE TABLE public.mai_2016
(
  jourvalidation date,
  tranchehoraire integer,
  libellearret character(20),
  nb1eremontees integer
);

COPY juin_2016
FROM 'C:/Program Files/PostgreSQL/9.5/CSV/SDD/SDD_mois_0716_clean.csv'
WITH DELIMITER ',';

-- pour faire la moyenne
select sum(nb1eremontees)/30 from avril_2016;
select count(distinct jourvalidation) from mai_2016;
select sum(nb1eremontees)/(select count(distinct jourvalidation) from mai_2016) from mai_2016;
-- exemple de requete pour une station
SELECT jourvalidation, tranchehoraire, nb1eremontees FROM juillet_2016 WHERE libellearret = 'Hay Raja' AND jourvalidation = '2016-07-19' ORDER BY tranchehoraire;