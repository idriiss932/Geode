# Traduction FR/EN

La source du jeu (français) est `geode_src.html` ; `geode.html` en est dérivé :

    node tools/i18n/extract.js   # liste les chaînes (acorn)
    python3 tools/i18n/xform.py  # enveloppe les chaînes connues dans _T()/_tt`` et injecte le dictionnaire EN

Les traductions sont dans `en_a.py` et `en_b.py` (clé = texte français, `§` = valeur insérée, `{0}`… dans la version anglaise).
Une chaîne absente du dictionnaire reste en français.
