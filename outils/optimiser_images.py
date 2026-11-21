#!/usr/bin/env python3
"""Prépare les images du site pour le web.

Pour chaque photo images/projets/<projet>/N.jpg, crée :
  - thumbs/N.webp : vignette légère (mosaïque et galerie)
  - web/N.webp    : version d'affichage (visionneuse plein écran)
Les originaux ne sont jamais modifiés.

Génère aussi images/photos.json (liste des photos de chaque projet, avec les
dimensions des vignettes) et images/background.webp (fond de la page d'accueil).

Utilisation, depuis la racine du dépôt :
    pip install pillow
    python3 outils/optimiser_images.py

Pour ajouter des photos : déposez-les dans images/projets/<projet>/ (1.jpg, 2.jpg, ...),
relancez le script, puis publiez les nouveaux fichiers.
"""
import json
import re
import sys
from multiprocessing import Pool
from pathlib import Path

from PIL import Image, ImageOps

Image.MAX_IMAGE_PIXELS = None  # photos très haute résolution

RACINE = Path(__file__).resolve().parent.parent
IMAGES = RACINE / "images"
PROJETS = IMAGES / "projets"

THUMB_COTE_LONG, THUMB_QUALITE = 900, 72
WEB_COTE_LONG, WEB_QUALITE = 2200, 80
FOND_LARGEUR, FOND_QUALITE = 2400, 78


def a_jour(source: Path, cible: Path) -> bool:
    return cible.exists() and cible.stat().st_mtime >= source.stat().st_mtime


def redimensionner(source: Path, cible: Path, cote_long: int, qualite: int):
    """Enregistre source en WebP, côté le plus long = cote_long (sans agrandir)."""
    with Image.open(source) as im:
        icc = im.info.get("icc_profile")
        im.draft("RGB", (cote_long, cote_long))  # décodage JPEG réduit : bien plus rapide
        im = ImageOps.exif_transpose(im).convert("RGB")
        im.thumbnail((cote_long, cote_long), Image.LANCZOS)
        cible.parent.mkdir(parents=True, exist_ok=True)
        im.save(cible, "WEBP", quality=qualite, method=5, icc_profile=icc)
        return im.size


def traiter(source: Path):
    dossier = source.parent
    n = int(source.stem)
    thumb = dossier / "thumbs" / f"{n}.webp"
    web = dossier / "web" / f"{n}.webp"
    if not a_jour(source, thumb):
        redimensionner(source, thumb, THUMB_COTE_LONG, THUMB_QUALITE)
    if not a_jour(source, web):
        redimensionner(source, web, WEB_COTE_LONG, WEB_QUALITE)
    with Image.open(thumb) as t:
        w, h = t.size
    return dossier.name, n, w, h


def main():
    sources = sorted(
        (p for p in PROJETS.glob("*/*.jpg") if re.fullmatch(r"\d+", p.stem)),
        key=lambda p: (p.parent.name, int(p.stem)),
    )
    if not sources:
        sys.exit("Aucune photo trouvée dans images/projets/")

    with Pool(2) as pool:
        resultats = pool.map(traiter, sources, chunksize=2)

    photos = {}
    for projet, n, w, h in resultats:
        photos.setdefault(projet, []).append({"n": n, "w": w, "h": h})
    for liste in photos.values():
        liste.sort(key=lambda p: p["n"])
    (IMAGES / "photos.json").write_text(
        json.dumps(photos, ensure_ascii=False, indent=1) + "\n", encoding="utf-8"
    )

    fond = IMAGES / "background.jpg"
    if fond.exists():
        cible = IMAGES / "background.webp"
        if not a_jour(fond, cible):
            with Image.open(fond) as im:
                icc = im.info.get("icc_profile")
                im.draft("RGB", (FOND_LARGEUR, FOND_LARGEUR))
                im = ImageOps.exif_transpose(im).convert("RGB")
                im.thumbnail((FOND_LARGEUR, FOND_LARGEUR), Image.LANCZOS)
                im.save(cible, "WEBP", quality=FOND_QUALITE, method=5, icc_profile=icc)

    print(f"{len(sources)} photos traitées dans {len(photos)} projets.")


if __name__ == "__main__":
    main()
