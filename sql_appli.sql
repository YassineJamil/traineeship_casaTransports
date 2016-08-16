-- SDC script complet de creation de table et de son remplissage, ne pas oublier de bien mentionner la date

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
FROM 'C:/Program Files/PostgreSQL/9.5/CSV/SDC/SDC_0115_clean.csv'
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

CREATE TABLE avril_2016
(
  jourvalidation date,
  tranchehoraire integer,
  libellearret character(20),
  nb1eremontees integer,
  directiontrajet character(6)
);

COPY avril_2016
FROM 'C:/Program Files/PostgreSQL/9.5/CSV/SDD/SDD_0416_clean.csv'
WITH DELIMITER ',';