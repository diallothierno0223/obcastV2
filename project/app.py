import streamlit as st

st.set_page_config(
    page_title="OBCAST – Moteur de recherche",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Charger Bootstrap CSS et JS
st.markdown("""
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet">
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js"></script>
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
""", unsafe_allow_html=True)


# CSS personnalisé
st.markdown("""
<style>
    /* Masquer le header par défaut de Streamlit */
    header[data-testid="stHeader"] {
        display: none;
    }
    
    .stApp {
        margin-top: 0;
    }
    
    /* Styles personnalisés */
    .custom-header {
        background: white;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        top: 0;
        z-index: 1000;
    }
    
    .header-top {
        padding: 20px 0;
    }
    
    .logo-container {
        display: flex;
        align-items: center;
        gap: 15px;
    }
    
    .logo-img {
        height: 60px;
        width: auto;
    }
    
    .social-icons {
        display: flex;
        gap: 15px;
        align-items: center;
    }
    
    .social-icons a {
        color: #333;
        font-size: 20px;
        transition: color 0.2s;
    }
    
    .social-icons a:hover {
        color: #0d6efd;
    }
    
    .navbar {
        padding: 0;
        background: white;
        border-top: 1px solid #e9ecef;
    }
    
    .navbar-nav {
        width: 100%;
        justify-content: center;
    }
    
    .navbar-nav .nav-link {
        color: #333;
        font-weight: 500;
        padding: 1rem 1.5rem;
        transition: all 0.2s;
    }
    
    .navbar-nav .nav-link:hover {
        color: #0d6efd;
    }
    
    .navbar-nav .nav-link.active {
        color: #0d6efd;
        border-bottom: 2px solid #0d6efd;
    }
    
    .hero-section {
        background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
        padding: 80px 0;
        text-align: center;
    }
    
    .hero-title {
        font-size: 2.5rem;
        font-weight: 700;
        color: #212529;
        margin-bottom: 30px;
        line-height: 1.3;
    }
    
    .hero-text {
        font-size: 1.1rem;
        color: #495057;
        /*max-width: 800px;*/
        margin: 0 auto 40px;
        line-height: 1.8;
    }
    
    .btn-primary {
        background: #0d6efd;
        border: none;
        padding: 12px 30px;
        font-size: 1rem;
        font-weight: 500;
        border-radius: 6px;
        transition: all 0.2s;
    }
    
    .btn-primary:hover {
        background: #0b5ed7;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(13, 110, 253, 0.3);
    }
    
    .btn-secondary {
        background: white;
        color: #0d6efd;
        border: 2px solid #0d6efd;
        padding: 12px 30px;
        font-size: 1rem;
        font-weight: 500;
        border-radius: 6px;
        transition: all 0.2s;
    }
    
    .btn-secondary:hover {
        background: #0d6efd;
        color: white;
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(13, 110, 253, 0.3);
    }
    
    @media (max-width: 991px) {
        .hero-title {
            font-size: 2rem;
        }
        
        .social-icons {
            margin-top: 15px;
        }
    }
    
    @media (max-width: 768px) {
        .hero-title {
            font-size: 1.75rem;
        }
        
        .hero-section {
            padding: 60px 20px;
        }
    }
</style>
""", unsafe_allow_html=True)

# Header avec Bootstrap
st.markdown("""
<header class="custom-header">
    <!-- Section supérieure avec logo et réseaux sociaux -->
    <div class="header-top">
        <div class="container">
            <div class="row align-items-center">
                <div class="col-lg-6 col-md-6 col-12">
                    <div class="logo-container">
                        <img src="https://carism.assas-universite.fr/sites/default/files/2025-09/logo_carism.svg" 
                                alt="CARISM Logo" 
                                class="logo-img ">
                    </div>
                </div>
                <div class="col-lg-6 col-md-6 col-12">
                    <div class="social-icons justify-content-md-end justify-content-center">
                        <a href="#" title="Facebook"><i class="fab fa-facebook-f"></i></a>
                        <a href="#" title="LinkedIn"><i class="fab fa-linkedin-in"></i></a>
                        <a href="#" title="Twitter"><svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-twitter-x" viewBox="0 0 16 16">
                            <path d="M12.6.75h2.454l-5.36 6.142L16 15.25h-4.937l-3.867-5.07-4.425 5.07H.316l5.733-6.57L0 .75h5.063l3.495 4.633L12.601.75Zm-.86 13.028h1.36L4.323 2.145H2.865z"/>
                        </svg></a>
                    </div>
                </div>
            </div>
        </div>
    </div>
</header>

<!-- Section Hero -->
<section class="hero-section">
    <div class="container">
        <h1 class="hero-title">
            Explorer et analyser les podcasts avec<br>
            le Carism – Université Sorbonne Panthéon
        </h1>
        <p class="hero-text">
            Ce site vitrine met à disposition le travail de recherche mené au sein du 
            Carism (Université Sorbonne Panthéon) autour des podcasts.<br>
            Vous y trouverez une base de données qualitative recensant et décrivant de 
            nombreux podcasts, des analyses interactives permettant d'en saisir les 
            grandes tendances, ainsi que la possibilité de télécharger les données pour 
            vos propres recherches.
        </p>
        <div class="d-flex gap-3 justify-content-center flex-wrap">
            <button class="btn btn-primary">Explorer les podcasts</button>
            <button class="btn btn-secondary">Télécharger les données</button>
        </div>
    </div>
</section>
""", unsafe_allow_html=True)

# Contenu additionnel de votre application
st.markdown("<br><br>", unsafe_allow_html=True)

# Sections additionnelles
col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="card h-100 border-0 shadow-sm">
        <div class="card-body text-center p-4">
            <i class="fas fa-podcast fa-3x text-primary mb-3"></i>
            <h5 class="card-title">Base de données</h5>
            <p class="card-text">Accédez à notre collection complète de podcasts analysés et documentés</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="card h-100 border-0 shadow-sm">
        <div class="card-body text-center p-4">
            <i class="fas fa-chart-line fa-3x text-primary mb-3"></i>
            <h5 class="card-title">Analyses interactives</h5>
            <p class="card-text">Explorez les tendances et insights grâce à nos outils d'analyse</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="card h-100 border-0 shadow-sm">
        <div class="card-body text-center p-4">
            <i class="fas fa-download fa-3x text-primary mb-3"></i>
            <h5 class="card-title">Téléchargement</h5>
            <p class="card-text">Téléchargez les données pour vos propres recherches académiques</p>
        </div>
    </div>
    """, unsafe_allow_html=True)