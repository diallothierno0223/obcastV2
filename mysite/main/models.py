from django.db import models

class MotCle(models.Model): 
    label = models.CharField(max_length=100)

    def __str__(self):
        return self.label

class Rubrique(models.Model): 
    label = models.CharField(max_length=100)

    def __str__(self):
        return self.label

class Recompense(models.Model): 
    label = models.CharField(max_length=100)

    def __str__(self):
        return self.label

class Genre(models.Model): 
    label = models.CharField(max_length=100)

    def __str__(self):
        return self.label

class Plateforme(models.Model): 
    label = models.CharField(max_length=100)

    def __str__(self):
        return self.label

class Etiquette(models.Model): 
    label = models.CharField(max_length=50)
    type_etiquette = models.CharField(max_length=100, default="N/A")

    def __str__(self):
        return self.label

class Createur(models.Model): 
    nom = models.TextField(default="N/A")
    genre = models.CharField(max_length=100, default="N/A")
    categorie_createur = models.TextField(default="N/A")
    origin = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.nom

class Producteur(models.Model): 
    nom = models.CharField(max_length=100, default="N/A")
    status_producteur = models.CharField(max_length=100, default="N/A")
    type_producteur = models.CharField(max_length=100, default="N/A")
    model_eco = models.CharField(max_length=100, default="N/A")
    natif_enrichi = models.CharField(max_length=100, default="N/A")

    def __str__(self):
        return self.nom

class Podcast(models.Model):
    nom = models.TextField(default="N/A")
    collection = models.TextField(default="N/A")
    resume_officiel = models.TextField(default="N/A")
    nom_host = models.TextField(default="N/A")
    
    date_premier_episode = models.DateField(null=True, blank=True)
    date_derniere_episode = models.DateField(null=True, blank=True)
    datediff = models.IntegerField(default=0)
    periodicite = models.TextField(default="N/A")
    
    interrompu_moment_1_collection = models.TextField(default="N/A")
    interrompu_moment_2_collection = models.TextField(default="N/A")
    
    nb_episode_collecte_1 = models.IntegerField(default=0)
    nb_episode_collecte_2 = models.IntegerField(default=0)
    nb_episode_collecte_1_media = models.IntegerField(default=0)
    nb_episode_collecte_2_media = models.IntegerField(default=0)
    
    duree_moyenne = models.FloatField(default=0)
    duree_variable = models.TextField(default="N/A")

    # Audience & Stats
    audience_site_nb_ecoute = models.IntegerField(default=0)
    audience_apple_classement = models.IntegerField(default=0)
    audience_apple_note = models.FloatField(default=0)
    audience_castbox_abonnement = models.IntegerField(default=0)
    audience_castbox_nb_ecoute = models.IntegerField(default=0)
    audience_podcastaddict_abonnement = models.IntegerField(default=0)
    audience_youtube_nb_vue = models.IntegerField(default=0)
    audience_soundcloud_nb_ecoute = models.IntegerField(default=0)
    nb_telechargement_france = models.IntegerField(default=0)
    nb_telechargement_monde = models.IntegerField(default=0)

    date_collecte_1 = models.DateField(null=True, blank=True)
    date_collecte_2 = models.DateField(null=True, blank=True)

    # Foreign Key
    producteur = models.ForeignKey(Producteur, on_delete=models.SET_NULL, null=True, related_name="podcasts")

    # ManyToMany
    motcle = models.ManyToManyField(MotCle, related_name="podcasts")
    rubrique = models.ManyToManyField(Rubrique, related_name="podcasts")
    recompense = models.ManyToManyField(Recompense, related_name="podcasts")
    genre = models.ManyToManyField(Genre, related_name="podcasts")
    etiquette = models.ManyToManyField(Etiquette, related_name="podcasts")
    createur = models.ManyToManyField(Createur, related_name="podcasts")
    
    # ManyToMany avec table intermédiaire pour le champ 'etat'
    plateforme = models.ManyToManyField(Plateforme, through='PodcastPlateforme', related_name="podcasts")

    def __str__(self):
        return self.nom

class PodcastPlateforme(models.Model):
    podcast = models.ForeignKey(Podcast, on_delete=models.CASCADE)
    plateforme = models.ForeignKey(Plateforme, on_delete=models.CASCADE)
    etat = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        unique_together = ('podcast', 'plateforme')
        db_table = 'main_podcast_plateforme'