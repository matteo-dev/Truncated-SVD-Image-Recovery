import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from copy import deepcopy

# Chargement des images
mask = mpimg.imread(r"H:\Documents\ING3_S2\Analyse Numérique\AnaNumProjet\cheval-abime2-mask.png")
img_color = mpimg.imread(r"H:\Documents\ING3_S2\Analyse Numérique\AnaNumProjet\cheval-abime2.png")

# Normaliser les données (dans [0,1] si ce n'est pas déjà fait)
if mask.max() > 1:
    mask = mask / 255.0
if img_color.max() > 1:
    img_color = img_color / 255.0

# S'assurer que le masque est binaire
mask = (mask > 0.5).astype(float)

# Paramètres
k = 50
epsilon = 1e-4
max_iter = 100

# Fonction de SVD tronquée
def svd_tronquee(A, k):
    U, S, Vt = np.linalg.svd(A, full_matrices=False)
    S[k:] = 0
    return U @ np.diag(S) @ Vt

restored_channels = []
normes_frobenius = []

# Traitement canal par canal
for c in range(3):
    channel = img_color[:, :, c]
    restored = deepcopy(channel)

    for i in range(max_iter):
        Ak = svd_tronquee(restored, k)
        new_channel = channel * (1 - mask) + Ak * mask
        diff = np.linalg.norm(restored - new_channel, ord='fro')
        restored = new_channel
        if diff < epsilon:
            break

# Calcul de la norme de Frobenius sur la zone masquée pour ce canal
    diff_masque = mask * (restored - channel)
    norme_locale = np.linalg.norm(diff_masque, ord='fro')
    normes_frobenius.append(norme_locale)

    restored_channels.append(restored)

# Recomposition de l’image couleur restaurée
img_restored_color = np.stack(restored_channels, axis=2)

# Affichage des résultats
fig, axs = plt.subplots(1, 2, figsize=(12, 6))
axs[0].imshow(img_color)
axs[0].set_title("Image couleur abimee")
axs[0].axis('off')
axs[1].imshow(img_restored_color)
axs[1].set_title("Image couleur restauree")
axs[1].axis('off')
plt.tight_layout()
plt.show()

# Affichage des normes de Frobenius par canal
for i, val in enumerate(normes_frobenius):
    print(f"Canal {['R', 'G', 'B'][i]} – Norme de Frobenius (zone masquee) : {val:.6f}")

# Moyenne globale
moyenne = np.mean(normes_frobenius)
print(f"\n Moyenne des normes de Frobenius sur les 3 canaux : {moyenne:.6f}")

# S’assurer que les valeurs sont bien dans [0, 1]
img_restored_color = np.clip(img_restored_color, 0, 1)
# Sauvegarde de l’image restaurée en couleur 
plt.imsave("image_restauree_couleur.png", img_restored_color)
print(" Image couleur restauree enregistree sous : image_restauree_couleur.png")
