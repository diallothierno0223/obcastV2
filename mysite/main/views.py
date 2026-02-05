from django.shortcuts import render, HttpResponse
from django.db.models import Sum, Count
from django.core.paginator import Paginator

from .models import Podcast, Genre, Producteur, Createur 

import csv
from datetime import datetime
import json






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
    
    print("start reading")
    podcasts_qs = Podcast.objects.select_related("producteur").prefetch_related(
        "motcle",
        "genre",
        "createur"
    ).all().order_by('id')

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

    print(f"Total items: {paginator.count}")
    print(f"Nombre de pages: {paginator.num_pages}")
    print(f"Page actuelle: {page_obj.number}")
    print(f"A un suivant ?: {page_obj.has_next()}")
    
    return render(request, "main/podcast.html", context={
        "podcasts": data,
        "page_obj": page_obj,
        "paginator": paginator,
        "total_count": paginator.count,
        "r": r
    })


from django.db.models import Q

def podcast_search(request):
    # 1. Récupérer tous les podcasts (avec optimisation SQL)
    query = Podcast.objects.select_related("producteur").prefetch_related(
        "motcle", "genre", "createur"
    ).all().order_by('id')

    # 2. Récupérer les paramètres du formulaire (GET)
    q_nom = request.GET.get('nom')
    q_producteur = request.GET.get('producteur')
    q_genre = request.GET.get('genre')
    q_periodicite = request.GET.get('periodicite')
    q_duree_min = request.GET.get('duree_min')

    # 3. Appliquer les filtres dynamiquement
    if q_nom:
        query = query.filter(nom__icontains=q_nom)
    
    if q_producteur:
        query = query.filter(producteur__id=q_producteur)
        
    if q_genre:
        query = query.filter(genre__id=q_genre)

    if q_periodicite:
        query = query.filter(periodicite=q_periodicite)

    if q_duree_min:
        query = query.filter(duree_moyenne__gte=q_duree_min)

    # 4. Pagination (On réutilise ta logique de 50 items)
    paginator = Paginator(query, 50)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    # 5. Préparer les données pour le Select du formulaire
    context = {
        'page_obj': page_obj,
        'podcasts': page_obj, # On boucle directement sur page_obj dans le template
        'producteurs': Producteur.objects.all().order_by('nom'),
        'genres': Genre.objects.all().order_by('label'),
        # On renvoie les valeurs saisies pour les garder dans le formulaire (recherche persistante)
        'params': request.GET 
    }
    
    return render(request, "main/podcast_search.html", context)

def podcast_detail(request, podcast_id):
    podcast = Podcast.objects.select_related('producteur').prefetch_related(
        'motcle', 'rubrique', 'recompense', 'genre', 'plateforme', 'createur', 'etiquette'
    ).get(id=podcast_id)

    return render(request, "main/podcast_detail.html", {"podcast": podcast})


def podcast_stats(request):
    context = {}

    # avant graph stat global -------------------------------------------------------------
    total_episodes = Podcast.objects.aggregate(Sum('nb_episode_collecte_1'))['nb_episode_collecte_1__sum'] or 0

    context['total_podcasts'] = Podcast.objects.count()
    context['total_producteurs'] = Producteur.objects.count()
    context['total_createurs'] = Createur.objects.count()
    context['total_episodes'] = total_episodes

    # -----------------------------------------------------------------------------------------



    # --- 1. Répartition par Modèle Économique (Pie Chart) ---
    # On agrège via le modèle Producteur
    modeles_eco = list(Producteur.objects.values('model_eco')
                       .annotate(count=Count('podcasts')) # Nombre de podcasts par modèle
                       .order_by('-count'))

    # --- 2. Top Producteurs (Histogramme Horizontal) ---
    top_producteurs = list(Producteur.objects.values('nom')
                           .annotate(total=Count('podcasts'))
                           .order_by('-total')[:10]) # Les 10 plus gros

    # --- 3. Natif vs Enrichi global ---
    stats_global = list(Podcast.objects.values('producteur__natif_enrichi').annotate(
        total=Count('id')
    ).exclude(producteur__natif_enrichi="N/A"))


    context.update({
        'modeles_eco_json': json.dumps(modeles_eco),
        'top_producteurs_json': json.dumps(top_producteurs),
        'stats_global_json': json.dumps(stats_global)
    })

# --------------------------------------------------- today
    # Dans ta vue Django
    stats_genres = list(Createur.objects.values('genre')
                        .annotate(total=Count('id'))
                        .order_by('-total'))
    context['stats_genres_json'] = json.dumps(stats_genres)


    # Le Top 10 des Genres de Podcasts (Treemap ou Bar Chart)
    stats_genres_podcast = list(Genre.objects.annotate(
        nb_podcasts=Count('podcasts')
    ).values('label', 'nb_podcasts').order_by('-nb_podcasts')[:15])
    context['genres_podcast_json'] = json.dumps(stats_genres_podcast)

    # Attention : prendre un échantillon ou limiter si trop de données (ex: Top 100)
    correlation_data = list(Podcast.objects.filter(audience_youtube_nb_vue__gt=0)
                            .values('nom', 'duree_moyenne', 'audience_youtube_nb_vue')[:200])
    context['correlation_json'] = json.dumps(correlation_data)

    # --- Graph 9. Distribution des durées par Genre ---
    # On récupère les données brutes pour que Plotly calcule les statistiques
    stats_duree_genre = list(Podcast.objects.filter(duree_moyenne__gt=0, duree_moyenne__lt=300)
                            .values('genre__label', 'duree_moyenne')
                            .exclude(genre__label__isnull=True))

    context['stats_duree_genre_json'] = json.dumps(stats_duree_genre)



    # return JsonResponse(context)
    return render(request, 'main/podcast_stats.html', context)