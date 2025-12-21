from django.db import models

# Create your models here.


class MotCle(models.Model): 
    label = models.CharField(max_length=100)

    def __str__(self):
        return self.label


class Producteur(models.Model): 
    nom = models.CharField(max_length=100, default="N/A")
    model_eco = models.CharField(max_length=100, default="N/A")
    natif_enrichi = models.CharField(max_length=100, default="N/A")
    nb_episode_collecte_1 = models.SmallIntegerField(default=0)
    nb_episode_collecte_2 = models.SmallIntegerField(default=0)
    status_producteur = models.CharField(max_length=100, default="N/A")
    type_producteur = models.CharField(max_length=100, default="N/A")


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
    


class Createur(models.Model): 
    nom = models.CharField(max_length=100, default="N/A")
    prenom = models.CharField(max_length=100, default="N/A")
    mail = models.CharField(max_length=100, default="N/A")
    genre = models.CharField(max_length=100, default="N/A")
    is_host = models.CharField(max_length=100, default="N/A")
    categoeir_createur = models.CharField(max_length=100, default="N/A")


    
class Etiquette(models.Model): 
    label = models.CharField(max_length=50)
    type_etiquette = models.CharField(max_length=100, default="N/A")

    def __str__(self):
        return self.label
    

    
class Collection(models.Model): 
    label = models.CharField(max_length=50)

    def __str__(self):
        return self.label
    


class Podcast(models.Model):
    nom = models.CharField(max_length=100, default="N/A")
    date_premier_episode = models.DateField()
    date_derniere_episode = models.DateField()
    datediff = models.SmallIntegerField(default=0)
    periodicite = models.CharField(default="N/A", max_length=100)
    interrompu_moment_1_collection = models.CharField(max_length=100, default="N/A")
    interrompu_moment_2_collection = models.CharField(max_length=100, default="N/A")
    nb_episode_collecte_1 = models.SmallIntegerField(default=0)
    nb_episode_collecte_2 = models.SmallIntegerField(default=0)
    duree_moyenne = models.SmallIntegerField(default=0)
    duree_variable = models.CharField(default="N/A", max_length=100)
    date_collecte_1 = models.DateField()
    date_collecte_2 = models.DateField()
    nb_telechargement_france = models.IntegerField(default=0)
    nb_telechargement_monde = models.IntegerField(default=0)

    motcle = models.ManyToManyField(MotCle, related_name="podcast", blank=True)
    producteur = models.ForeignKey(Producteur, on_delete=models.CASCADE, related_name="podcasts", blank=True)
    rubrique = models.ManyToManyField(Rubrique, related_name="podcast", blank=True)
    recompense = models.ManyToManyField(Recompense, related_name="podcast", blank=True)
    genre = models.ManyToManyField(Genre, related_name="podcast", blank=True)
    plateforme = models.ManyToManyField(Plateforme, related_name="podcast", blank=True)
    createur = models.ManyToManyField(Createur, related_name="podcast", blank=True)
    etiquette = models.ManyToManyField(Etiquette, related_name="podcast", blank=True)
    collection = models.ManyToManyField(Collection, related_name="podcast", blank=True)

