# Portfolio — Ethan_photographie

Portfolio photo : automobile, moto, événements et portraits.

**Site : https://ethan-photographie.github.io/portfolio/**

## Contenu du dépôt

- `index.html`, `projets.html`, `contact.html` : les pages du site
- `images/projets/<dossier>/` : les photos de chaque série (`1.jpg`, `2.jpg`, …), avec les versions légères dans `thumbs/` et `web/`
- `images/photos.json` : la liste des photos de chaque série (générée automatiquement)
- `outils/optimiser_images.py` : prépare les images pour le web

## Ajouter des photos

1. Déposer les JPG dans `images/projets/<dossier>/` en continuant la numérotation (`41.jpg`, `42.jpg`, …). La photo `1.jpg` sert de couverture dans la mosaïque.
2. Depuis la racine du dépôt : `pip install pillow` (une seule fois), puis `python3 outils/optimiser_images.py`.
3. Publier les nouveaux fichiers : les dossiers `thumbs/` et `web/`, et `images/photos.json`. Les JPG originaux ne sont pas utilisés par le site.

Pour un nouveau projet, il faut aussi l'ajouter dans `projets.html` (voir les commentaires en haut du script de la page).

## Droits

Toutes les photographies sont © Ethan_photographie, tous droits réservés. Voir [LICENSE](LICENSE).
