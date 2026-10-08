import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from copy import deepcopy

# Chargement des images
img_nb = mpimg.imread(r"H:\Documents\ING3_S2\Analyse Numérique\AnaNumProjet\cheval-abime2-nb.png")
mask = mpimg.imread(r"H:\Documents\ING3_S2\Analyse Numérique\AnaNumProjet\cheval-abime2-mask.png")

# Normaliser les données (dans [0,1] si ce n'est pas déjà fait)
if img_nb.max() > 1:
    img_nb = img_nb / 255.0
if mask.max() > 1:
    mask = mask / 255.0

# S'assurer que le masque est binaire
mask = (mask > 0.5).astype(float)

# Création d'une copie de l'image d'origine
img_restored = deepcopy(img_nb)

# Paramètres
k = 50  # Nombre de valeurs singulières conservées
epsilon = 1e-4  # Tolérance pour la convergence
max_iter = 100  # Nombre max d'itérations

# Fonction de SVD tronquée
def svd_tronquee(A, k):
    U, S, Vt = np.linalg.svd(A, full_matrices=False)
    S[k:] = 0  # On tronque à k valeurs
    return U @ np.diag(S) @ Vt

# Itérations
for i in range(max_iter):
    Ak = svd_tronquee(img_restored, k)
    new_img = img_nb * (1 - mask) + Ak * mask  # On remplace uniquement dans la zone masquée
    diff = np.linalg.norm(img_restored - new_img, ord='fro')
    img_restored = new_img
    if diff < epsilon:
        break


#  Norme de Frobenius sur les zones masquées uniquement
diff_masque = mask * (img_restored - img_nb)
norme_frobenius_locale = np.linalg.norm(diff_masque, ord='fro')
print(f"Norme de Frobenius (zone masquee uniquement) : {norme_frobenius_locale:.6f}")


# Affichage des résultats
fig, axs = plt.subplots(1, 2, figsize=(12, 6))
axs[0].imshow(img_nb, cmap='gray')
axs[0].set_title("Image abimee")
axs[0].axis('off')
axs[1].imshow(img_restored, cmap='gray')
axs[1].set_title("Image restauree (NB)")
axs[1].axis('off')
plt.tight_layout()
plt.show()

# Sauvegarde de l’image restaurée NB
plt.imsave("image_restauree_nb.png", img_restored, cmap='gray')
print("Image NB restauree enregistree sous : image_restauree_nb.png")