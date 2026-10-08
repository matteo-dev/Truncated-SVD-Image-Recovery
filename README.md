# Truncated SVD Image Recovery 

🇫🇷 [Version française](#francais) | 🇬🇧 [English version](#english) 

---

## <a name="francais"></a> 🇫🇷 Français

### Présentation
Ce dépôt contient une implémentation en Python d'une méthode itérative de restauration d'image basée sur la **Décomposition en Valeurs Singulières (SVD) tronquée**. Inspiré de l'article *"Truncated singular value decomposition in ripped photo recovery"* (Kong Hoong Lem, 2021), cet algorithme permet de réparer mathématiquement des photos endommagées, rayées ou pliées. 

Initialement développé dans le cadre d'un module d'analyse numérique, le projet intègre désormais une application web interactive **Streamlit** pour tester l'algorithme en direct, illustrant l'application concrète de concepts d'algèbre linéaire.

### Fonctionnalités
* **Application Web Interactive** : Un dashboard Streamlit complet permettant d'ajuster les hyperparamètres ($k$, $\epsilon$, itérations) et de visualiser la restauration en temps réel.
* **Support Noir & Blanc et Couleur** : Restaure les images monocanal et multicanaux (traitement indépendant canal par canal pour le RGB).
* **Approximation Itérative** : Utilise des approximations SVD de rang réduit pour estimer et combler les pixels manquants dans les zones détériorées.

### Installation et Déploiement
1. Clonez ce dépôt.
2. Installez les dépendances requises : `pip install -r requirements.txt`
3. Lancez le dashboard en local : `streamlit run dashboard.py`

### Technologies
* Python
* Streamlit (Interface Web)
* NumPy (Opérations matricielles & SVD)
* Pillow (Manipulation d'images)

---

## <a name="english"></a> 🇬🇧 English

### Overview
This repository contains a Python implementation of an iterative image restoration method based on **Truncated Singular Value Decomposition (SVD)**. Inspired by the paper *"Truncated singular value decomposition in ripped photo recovery"* (Kong Hoong Lem, 2021), this algorithm mathematically repairs damaged, scratched, or folded photographs.

Initially developed as part of a numerical analysis course, the project now features an interactive **Streamlit** web application to test the algorithm live, bridging the gap between theoretical linear algebra and practical implementation.

### Features
* **Interactive Web App**: A complete Streamlit dashboard to tweak hyperparameters ($k$, $\epsilon$, iterations) and visualize the restoration in real-time.
* **Grayscale & RGB Support**: Restores single-channel (black & white) and multi-channel (color) images.
* **Iterative Approximation**: Uses reduced-rank SVD approximations to estimate and fill missing pixels in damaged areas.

### Installation and Deployment
1. Clone this repository.
2. Install the required dependencies: `pip install -r requirements.txt`
3. Run the dashboard locally: `streamlit run dashboard.py`

### Technologies
* Python
* Streamlit (Web Interface)
* NumPy (Matrix operations & SVD)
* Pillow (Image manipulation)
