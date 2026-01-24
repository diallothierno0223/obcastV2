from django.shortcuts import render, HttpResponse, get_object_or_404
from django.http import JsonResponse
from .models import Podcast

from django.db.models import F, Q, FloatField, ExpressionWrapper, Count, Avg, Min, Max, Sum
from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models.functions import ExtractYear, NullIf
from .models import Podcast, Genre, Producteur, Plateforme, Rubrique, MotCle, Createur #  Collection,

import csv
from datetime import datetime

# Create your views here.


def home(request): 
    return render(request, "main/accueil.html")

def methodologie(request): 
    return render(request, "main/methodologie.html")

def publication_event(request): 
    return render(request, "main/publication.html")

def contact(request): 
    if request.method == "POST":
        # Traitez les données du formulaire ici (par exemple, en les enregistrant dans la base de données ou en envoyant un e-mail)
        # name = request.POST.get("name")
        # email = request.POST.get("email")
        # message = request.POST.get("message")
        # Vous pouvez ajouter votre logique de traitement ici

        return HttpResponse("Merci pour votre message ! Nous vous contacterons bientôt.")
    return render(request, "main/contact.html")


def telechargement(request):
    # this function merge all table in database and return a csv file of result for download
    # Query all podcasts with optimized select_related and prefetch_related
    if request.method == "POST":
        # Use iterator() to avoid loading all data into memory at once
        podcasts = Podcast.objects.select_related("producteur").prefetch_related(
            "motcle",
            "genre",
            "createur"
        ).all().iterator(chunk_size=100)

        # Create CSV response
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="podcasts_export_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv"'

        # Create CSV writer
        writer = csv.writer(response, delimiter=';')
        
        # Write header row
        header = [
            'ID', 'Nom du Podcast', 'Date Premier Episode', 'Date Dernière Episode',
            'Périodicité', 'Durée Moyenne (min)', 'Nb Episodes Collectés 1', 'Nb Episodes Collectés 2',
            'Mots-clés', 'Producteur', 'Type Producteur', 'Status Producteur',
            'Genres', 'Créateurs', 'Genre Créateurs',
            'Téléchargements France', 'Téléchargements Monde', 'Durée d\'activité (jours)'
        ]
        writer.writerow(header)

        # Write data rows
        for p in podcasts:
            prod_nom = p.producteur.nom if p.producteur else "N/A"
            prod_type = p.producteur.type_producteur if p.producteur else "N/A"
            prod_status = p.producteur.status_producteur if p.producteur else "N/A"

            row = [
                p.id,
                p.nom,
                p.date_premier_episode if p.date_premier_episode else "",
                p.date_derniere_episode if p.date_derniere_episode else "",
                p.periodicite if p.periodicite else "",
                p.duree_moyenne if p.duree_moyenne else "",
                p.nb_episode_collecte_1 if p.nb_episode_collecte_1 else "",
                p.nb_episode_collecte_2 if p.nb_episode_collecte_2 else "",
                " | ".join([m.label for m in p.motcle.all()]),
                prod_nom,
                prod_type,
                prod_status,
                " | ".join([m.label for m in p.genre.all()]),
                " | ".join([f"{m.nom.capitalize()}" for m in p.createur.all()]),
                " | ".join([m.genre for m in p.createur.all()]),
                p.nb_telechargement_france if hasattr(p, 'nb_telechargement_france') and p.nb_telechargement_france else "",
                p.nb_telechargement_monde if hasattr(p, 'nb_telechargement_monde') and p.nb_telechargement_monde else "",
                p.datediff if hasattr(p, 'datediff') and p.datediff else ""
            ]
            writer.writerow(row)

        return response
    return render(request, "main/telechargement.html")

def podcast(request):
    from django.core.paginator import Paginator
    
    print("start reading")
    podcasts_qs = Podcast.objects.select_related("producteur").prefetch_related(
        "motcle",
        "genre",
        "createur"
    ).all()

    # Setup pagination - 20 items per page
    paginator = Paginator(podcasts_qs, 20)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    data = []

    for p in page_obj:
        # On gère le cas où producteur est None (si défini en SET_NULL dans les models)
        prod_nom = p.producteur.nom if p.producteur else "N/A"
        prod_type = p.producteur.type_producteur if p.producteur else "N/A"
        prod_status = p.producteur.status_producteur if p.producteur else "N/A"

        data.append({
            "id": p.id,
            "nom": p.nom,
            "date_premier_episode": p.date_premier_episode,
            "date_derniere_episode": p.date_derniere_episode,
            "periodicite": p.periodicite,
            "duree_moyenne": p.duree_moyenne,
            "nb_episode_collecte_1": p.nb_episode_collecte_1,
            "nb_episode_collecte_2": p.nb_episode_collecte_2,
            "mot_cle": [m.label for m in p.motcle.all()],
            "nom_producteur": prod_nom, 
            "type_producteur": prod_type,
            "status_producteur": prod_status,
            "genre_podcast": [m.label for m in p.genre.all()],
            "createur": [f"{m.nom.capitalize()}" for m in p.createur.all()],
            "genre_createur": [m.genre for m in p.createur.all()]
        })

    print(f"Data prepared for {len(data)} podcasts on page {page_number}")
    r = list(range(50))
    
    return render(request, "main/podcast.html", context={
        "podcasts": data,
        "page_obj": page_obj,
        "paginator": paginator,
        "total_count": paginator.count,
        "r": r
    })



def podcast_detail(request, podcast_id):
    podcast = Podcast.objects.select_related('producteur').prefetch_related(
        'motcle', 'rubrique', 'recompense', 'genre', 'plateforme', 'createur', 'etiquette'
    ).get(id=podcast_id)

    return render(request, "main/podcast_detail.html", {"podcast": podcast})




def podcast_stats(request):
    # 1. Evolution du nombre d'épisodes dans le temps (par année)
    episodes_per_year = (
        Podcast.objects
        .annotate(year=ExtractYear('date_premier_episode'))
        .values('year')
        .annotate(
            total_episodes=Sum(F('nb_episode_collecte_1') + F('nb_episode_collecte_2'))
        )
        .order_by('year')
    )

    # 2. Répartition des podcasts par genre
    genres = Genre.objects.annotate(count=Count('podcast')).order_by('-count')

    # 3. Répartition par producteur
    producteurs = Producteur.objects.annotate(count=Count('podcasts')).order_by('-count')

    # 4. Durée moyenne des épisodes par genre
    genre_duree = (
        Genre.objects
        .annotate(avg_duree=Avg('podcast__duree_moyenne'))
        .order_by('-avg_duree')
    )

    # 5. Taux de téléchargement (France vs Monde) par podcast
    podcasts_dl = Podcast.objects.values('nom', 'nb_telechargement_france', 'nb_telechargement_monde')

    # 6. Répartition des podcasts par plateforme
    plateformes = Plateforme.objects.annotate(count=Count('podcast')).order_by('-count')

    # 7. Analyse de la durée d’activité (datediff)
    datediffs = Podcast.objects.values_list('datediff', flat=True)

    # 8. Corrélation modèle économique / succès
    model_eco_stats = (
        Producteur.objects
        .annotate(
            avg_dl=Avg('podcasts__nb_telechargement_monde')
        )
        .values('model_eco', 'avg_dl')
        .order_by('-avg_dl')
    )

    # 🧭 1A. Taux de croissance du nombre d’épisodes (NullIf pour éviter division par zéro)
    podcasts_growth = Podcast.objects.annotate(
        taux_croissance=ExpressionWrapper(
            100 * (F('nb_episode_collecte_2') - F('nb_episode_collecte_1')) /
            NullIf(F('nb_episode_collecte_1'), 0),
            output_field=FloatField()
        )
    ).values('nom', 'taux_croissance').order_by('-taux_croissance')

    # 🎧 2A. Top 10 des podcasts les plus téléchargés
    top10_dl = Podcast.objects.order_by('-nb_telechargement_monde').values('nom', 'nb_telechargement_monde')[:10]

    # 🎧 2B. Ratio Téléchargements Monde / France (NullIf pour éviter division par zéro)
    podcasts_ratio = Podcast.objects.annotate(
        ratio=ExpressionWrapper(
            F('nb_telechargement_monde') / NullIf(F('nb_telechargement_france'), 0),
            output_field=FloatField()
        )
    ).values('nom', 'nb_telechargement_france', 'nb_telechargement_monde', 'ratio')

    # 🎧 2C. Performances moyennes par genre
    genre_dl = Genre.objects.annotate(
        avg_dl=Avg('podcast__nb_telechargement_monde')
    ).values('label', 'avg_dl').order_by('-avg_dl')

    # 🧑‍💼 3A. Producteurs les plus productifs
    prod_prod = Producteur.objects.annotate(count=Count('podcasts')).values('nom', 'count').order_by('-count')

    # 🧑‍💼 3B. Corrélation modèle économique et performance
    eco_perf = Producteur.objects.annotate(
        avg_dl=Avg('podcasts__nb_telechargement_monde')
    ).values('model_eco', 'avg_dl')

    # 🧑‍💼 3C. Répartition des types de producteurs
    type_prod = Producteur.objects.values('type_producteur').annotate(count=Count('id'))

    # # 🗂️ 4A. Répartition des podcasts par rubrique
    # rubrique_counts = Rubrique.objects.annotate(count=Count('podcast')).values('label', 'count')
    # # 🗂️ 4A. Répartition des podcasts par collection
    # collection_counts = Collection.objects.annotate(count=Count('podcast')).values('label', 'count')

    # 🗂️ 4B. Analyse des mots-clés
    motcle_counts = MotCle.objects.annotate(count=Count('podcast')).order_by('-count')[:20]

    # 🗂️ 4C. Nombre moyen de genres ou étiquettes par podcast
    avg_genres = Podcast.objects.annotate(nb_genres=Count('genre')).aggregate(avg=Avg('nb_genres'))['avg']
    avg_etiquettes = Podcast.objects.annotate(nb_etiquettes=Count('etiquette')).aggregate(avg=Avg('nb_etiquettes'))['avg']

    # 🧑‍🤝‍🧑 6A. Nombre moyen de créateurs par podcast
    avg_createurs = Podcast.objects.annotate(nb_createurs=Count('createur')).aggregate(avg=Avg('nb_createurs'))['avg']

    # 🧑‍🤝‍🧑 6B. Répartition des genres parmi les créateurs
    createur_genre = Createur.objects.values('genre').annotate(count=Count('id'))

    # 🧑‍🤝‍🧑 6C. Créateurs les plus présents
    createur_top = Createur.objects.annotate(count=Count('podcast')).order_by('-count')[:10]

    context = {
        "episodes_per_year": list(episodes_per_year),
        "genres": list(genres),
        "producteurs": list(producteurs),
        "genre_duree": list(genre_duree),
        "podcasts_dl": list(podcasts_dl),
        "plateformes": list(plateformes),
        "datediffs": list(datediffs),
        "model_eco_stats": list(model_eco_stats),

        "podcasts_growth": list(podcasts_growth),
        "top10_dl": list(top10_dl),
        "podcasts_ratio": list(podcasts_ratio),
        "genre_dl": list(genre_dl),
        "prod_prod": list(prod_prod),
        "eco_perf": list(eco_perf),
        "type_prod": list(type_prod),
        # "rubrique_counts": list(rubrique_counts),
        # "collection_counts": list(collection_counts),
        "motcle_counts": list(motcle_counts),
        "avg_genres": avg_genres,
        "avg_etiquettes": avg_etiquettes,
        "avg_createurs": avg_createurs,
        "createur_genre": list(createur_genre),
        "createur_top": list(createur_top),
    }
    return render(request, "main/podcast_stats.html", context)