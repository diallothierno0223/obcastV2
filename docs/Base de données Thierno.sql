--Tables racines
CREATE TABLE TYPE_PRODUCTEUR (
    id_type INT AUTO_INCREMENT PRIMARY KEY,
    type_ VARCHAR(255) NOT NULL
);

CREATE TABLE STATUS_PRODUCTEUR (
    id_status INT AUTO_INCREMENT PRIMARY KEY,
    status_ VARCHAR(255) NOT NULL
);

CREATE TABLE MOT_CLE (
    id_mot_cle INT AUTO_INCREMENT PRIMARY KEY,
    mot_cle VARCHAR(255) NOT NULL
);

CREATE TABLE RUBRIQUE (
    id_rubrique INT AUTO_INCREMENT PRIMARY KEY,
    rubrique VARCHAR(255) NOT NULL
);

CREATE TABLE PRIX_RECOMPENSE (
    id_prix_recompense INT AUTO_INCREMENT PRIMARY KEY,
    prix_recompense VARCHAR(255) NOT NULL
);

CREATE TABLE GENRE_FORMAT (
    id_genre_format INT AUTO_INCREMENT PRIMARY KEY,
    genre_format VARCHAR(255) NOT NULL
);

CREATE TABLE PLATEFORME (
    id_plateforme INT AUTO_INCREMENT PRIMARY KEY,
    plateforme VARCHAR(255) NOT NULL
);

CREATE TABLE CATEGORIE_CREATEUR (
    id_categorie_createur INT AUTO_INCREMENT PRIMARY KEY,
    categorie_createur VARCHAR(255) NOT NULL
);

CREATE TABLE TYPE_ETIQUETTE (
    id_type_etiquette INT AUTO_INCREMENT PRIMARY KEY,
    label VARCHAR(255) NOT NULL
);

CREATE TABLE COLLECTION (
    id_collection INT AUTO_INCREMENT PRIMARY KEY,
    label VARCHAR(255) NOT NULL
);

-- Tables dépendantes

CREATE TABLE PRODUCTEUR (
    id_producteur INT AUTO_INCREMENT PRIMARY KEY,
    nom_producteur VARCHAR(255) NOT NULL,
    model_eco VARCHAR(255),
    natif_enrichi VARCHAR(255),
    nb_episode_col_1 VARCHAR(25),
    nb_episode_col_2 VARCHAR(25),
    id_type INT NOT NULL,
    id_status INT NOT NULL,
    FOREIGN KEY (id_type) REFERENCES TYPE_PRODUCTEUR(id_type),
    FOREIGN KEY (id_status) REFERENCES STATUS_PRODUCTEUR(id_status)
);

CREATE TABLE ETIQUETTE (
    id_etiquette INT AUTO_INCREMENT PRIMARY KEY,
    etiquette VARCHAR(255) NOT NULL,
    id_type_etiquette INT NOT NULL,
    id_collection INT,
    FOREIGN KEY (id_type_etiquette) REFERENCES TYPE_ETIQUETTE(id_type_etiquette),
    FOREIGN KEY (id_collection) REFERENCES COLLECTION(id_collection)
);

CREATE TABLE CREATEUR (
    id_createur INT AUTO_INCREMENT PRIMARY KEY,
    nom_createur VARCHAR(255) NOT NULL,
    prenom_createur VARCHAR(255),
    mail VARCHAR(255),
    genre VARCHAR(255),
    is_Host VARCHAR(255),
    id_categorie_createur INT NOT NULL,
    FOREIGN KEY (id_categorie_createur) REFERENCES CATEGORIE_CREATEUR(id_categorie_createur)
);

-- Tables PODCAST

CREATE TABLE PODCAST (
    id_podcast INT AUTO_INCREMENT PRIMARY KEY,
    nom VARCHAR(255) NOT NULL,
    data_premiere_episode VARCHAR(255),
    data_derniere_episode VARCHAR(255),
    date_diff INT,
    periodicite VARCHAR(255),
    interrompu_moment_1_collection VARCHAR(255),
    interrompu_moment_2_collection VARCHAR(255),
    nb_episode_collecte_1 INT,
    nb_episode_collecte_2 INT,
    duree_moyenne INT,
    duree_variable INT,
    data_collecte_1 INT,
    data_collecte_2 INT,
    nb_telechargement_FR INT,
    nb_telechargement INT,
);

--Tables Jointure

CREATE TABLE ETIQUETTE_PODCAST (
    id_etiquette INT,
    id_podcast INT,
    PRIMARY KEY (id_etiquette, id_podcast),
    FOREIGN KEY (id_etiquette) REFERENCES ETIQUETTE(id_etiquette),
    FOREIGN KEY (id_podcast) REFERENCES PODCAST(id_podcast)
);

CREATE TABLE CREATEUR_PODCAST (
    id_createur INT,
    id_podcast INT,
    is_host BOOLEAN NOT NULL,
    PRIMARY KEY (id_createur, id_podcast),
    FOREIGN KEY (id_createur) REFERENCES CREATEUR(id_createur),
    FOREIGN KEY (id_podcast) REFERENCES PODCAST(id_podcast)
);

CREATE TABLE COLLECTION_PODCAST (
    id_collection INT,
    id_podcast INT,
    PRIMARY KEY (id_collection, id_podcast),
    FOREIGN KEY (id_collection) REFERENCES COLLECTION(id_collection),
    FOREIGN KEY (id_podcast) REFERENCES PODCAST(id_podcast)
);

CREATE TABLE COLLECTION_PODCAST (
    id_collection INT,
    id_podcast INT,
    PRIMARY KEY (id_collection, id_podcast),
    FOREIGN KEY (id_collection) REFERENCES COLLECTION(id_collection),
    FOREIGN KEY (id_podcast) REFERENCES PODCAST(id_podcast)
);

CREATE TABLE GENRE_FORMAT_PODCAST (
    id_genre_format INT,
    id_podcast INT,
    PRIMARY KEY (id_genre_format, id_podcast),
    FOREIGN KEY (id_genre_format) REFERENCES GENRE_FORMAT(id_genre_format),
    FOREIGN KEY (id_podcast) REFERENCES PODCAST(id_podcast)
);

CREATE TABLE RUBRIQUE_PODCAST (
    id_rubrique INT,
    id_podcast INT,
    PRIMARY KEY (id_rubrique, id_podcast),
    FOREIGN KEY (id_rubrique) REFERENCES RUBRIQUE(id_rubrique),
    FOREIGN KEY (id_podcast) REFERENCES PODCAST(id_podcast)
);

CREATE TABLE PRODUCTEUR_PODCAST (
    id_producteur INT,
    id_podcast INT,
    PRIMARY KEY (id_producteur, id_podcast),
    FOREIGN KEY (id_producteur) REFERENCES PRODUCTEUR(id_producteur),
    FOREIGN KEY (id_podcast) REFERENCES PODCAST(id_podcast)
);

CREATE TABLE MOT_CLE_PODCAST (
    id_mot_cle INT,
    id_podcast INT,
    PRIMARY KEY (id_mot_cle, id_podcast),
    FOREIGN KEY (id_mot_cle) REFERENCES MOT_CLE(id_mot_cle),
    FOREIGN KEY (id_podcast) REFERENCES PODCAST(id_podcast)
);

CREATE TABLE PRIX_RECOMPENSE_PODCAST (
    id_prix_recompense INT,
    id_podcast INT,
    PRIMARY KEY (id_prix_recompense, id_podcast),
    FOREIGN KEY (id_prix_recompense) REFERENCES PRIX_RECOMPENSE(id_prix_recompense),
    FOREIGN KEY (id_podcast) REFERENCES PODCAST(id_podcast)
);