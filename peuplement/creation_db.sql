-- =====================================================
-- 1. Création de la base de données
-- path : \i E:/thierno/TRAVAIL/PROJET_PERSO/OBCAST/peuplement/creation_db.sql

-- =====================================================
-- CREATE DATABASE obcast_project;

-- Se connecter à la base
-- \c obcast_project;

-- =====================================================
-- 2. Suppression et recréation du schéma public
-- =====================================================
DROP SCHEMA public CASCADE;
CREATE SCHEMA public;
-- SET search_path TO public;
-- C:/User/SG54800/Documents/peuplement/creation_db.sql

-- =====================================================
-- 3. Création des tables
-- =====================================================


CREATE TABLE main_motcle (
    id SERIAL PRIMARY KEY,
    label VARCHAR(100) NOT NULL
);


CREATE TABLE main_rubrique (
    id SERIAL PRIMARY KEY,
    label VARCHAR(100) NOT NULL
);


CREATE TABLE main_recompense (
    id SERIAL PRIMARY KEY,
    label VARCHAR(100) NOT NULL
);


CREATE TABLE main_genre (
    id SERIAL PRIMARY KEY,
    label VARCHAR(100) NOT NULL
);



CREATE TABLE main_plateforme (
    id SERIAL PRIMARY KEY,
    label VARCHAR(100) NOT NULL
);

CREATE TABLE main_etiquette (
    id SERIAL PRIMARY KEY,
    label VARCHAR(50) NOT NULL,
    type_etiquette VARCHAR(100) DEFAULT 'N/A'
);


CREATE TABLE main_createur (
    id SERIAL PRIMARY KEY,
    nom TEXT DEFAULT 'N/A',
    genre VARCHAR(100) DEFAULT 'N/A',
    categorie_createur TEXT DEFAULT 'N/A',
    origin TEXT
);


CREATE TABLE main_producteur (
    id SERIAL PRIMARY KEY,
    nom VARCHAR(100) DEFAULT 'N/A',
    status_producteur VARCHAR(100) DEFAULT 'N/A',
    type_producteur VARCHAR(100) DEFAULT 'N/A',
    model_eco VARCHAR(100) DEFAULT 'N/A',
    natif_enrichi VARCHAR(100) DEFAULT 'N/A'
);





CREATE TABLE main_podcast (
    id SERIAL PRIMARY KEY,

    nom TEXT DEFAULT 'N/A',
    collection TEXT DEFAULT 'N/A',
    resume_officiel TEXT DEFAULT 'N/A',
    nom_host TEXT DEFAULT 'N/A',
    date_premier_episode DATE,
    date_derniere_episode DATE,
    datediff INTEGER DEFAULT 0,
    periodicite TEXT DEFAULT 'N/A',
    interrompu_moment_1_collection TEXT DEFAULT 'N/A',
    interrompu_moment_2_collection TEXT DEFAULT 'N/A',
    nb_episode_collecte_1 INTEGER DEFAULT 0,
    nb_episode_collecte_2 INTEGER DEFAULT 0,
    nb_episode_collecte_1_media INTEGER DEFAULT 0,
    nb_episode_collecte_2_media INTEGER DEFAULT 0,
    duree_moyenne FLOAT DEFAULT 0,
    duree_variable TEXT DEFAULT 'N/A',

    audience_site_nb_ecoute INTEGER DEFAULT 0, 
    audience_apple_classement INTEGER DEFAULT 0,
    audience_apple_note FLOAT DEFAULT 0,
    audience_castbox_abonnement INTEGER DEFAULT 0,
    audience_castbox_nb_ecoute INTEGER DEFAULT 0,
    audience_podcastaddict_abonnement INTEGER DEFAULT 0,
    audience_youtube_nb_vue INTEGER DEFAULT 0,
    audience_soundcloud_nb_ecoute INTEGER DEFAULT 0,
    nb_telechargement_france INTEGER DEFAULT 0,
    nb_telechargement_monde INTEGER DEFAULT 0,

    date_collecte_1 DATE,
    date_collecte_2 DATE,

    producteur_id INTEGER REFERENCES main_producteur(id) ON DELETE SET NULL
);

-- =====================================================
-- Tables d’association (ManyToMany)
-- =====================================================

CREATE TABLE main_podcast_motcle (
    podcast_id INTEGER REFERENCES main_podcast(id) ON DELETE CASCADE,
    motcle_id INTEGER REFERENCES main_motcle(id) ON DELETE CASCADE,
    PRIMARY KEY (podcast_id, motcle_id)
);

CREATE TABLE main_podcast_rubrique (
    podcast_id INTEGER REFERENCES main_podcast(id) ON DELETE CASCADE,
    rubrique_id INTEGER REFERENCES main_rubrique(id) ON DELETE CASCADE,
    PRIMARY KEY (podcast_id, rubrique_id)
);

CREATE TABLE main_podcast_recompense (
    podcast_id INTEGER REFERENCES main_podcast(id) ON DELETE CASCADE,
    recompense_id INTEGER REFERENCES main_recompense(id) ON DELETE CASCADE,
    PRIMARY KEY (podcast_id, recompense_id)
);

CREATE TABLE main_podcast_genre (
    podcast_id INTEGER REFERENCES main_podcast(id) ON DELETE CASCADE,
    genre_id INTEGER REFERENCES main_genre(id) ON DELETE CASCADE,
    PRIMARY KEY (podcast_id, genre_id)
);


CREATE TABLE main_podcast_etiquette (
    podcast_id INTEGER REFERENCES main_podcast(id) ON DELETE CASCADE,
    etiquette_id INTEGER REFERENCES main_etiquette(id) ON DELETE CASCADE,
    PRIMARY KEY (podcast_id, etiquette_id)
);


CREATE TABLE main_podcast_createur (
    podcast_id INTEGER REFERENCES main_podcast(id) ON DELETE CASCADE,
    createur_id INTEGER REFERENCES main_createur(id) ON DELETE CASCADE,
    PRIMARY KEY (podcast_id, createur_id)
);



CREATE TABLE main_podcast_plateforme (
    podcast_id INTEGER REFERENCES main_podcast(id) ON DELETE CASCADE,
    plateforme_id INTEGER REFERENCES main_plateforme(id) ON DELETE CASCADE,
    etat VARCHAR(50),
    PRIMARY KEY (podcast_id, plateforme_id)
);
-- =====================================================
-- Fin du script
-- =====================================================