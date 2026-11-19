#!/usr/bin/env python3
"""Regenere docs/index.html (configurateur) a partir de :
  - nanokontrol2/nanoKONTROL2-EOS.noisette  (modules, INITIALISATION, modeles d'Actions de boutons)
  - tools/templates.json                     (modeles de Mapping et d'Action flash, extraits de projets valides)
  - tools/configurateur.src.html             (la page)
A lancer apres toute modification d'un de ces fichiers :
    python3 tools/build-configurateur.py
"""
import copy, json, pathlib

root = pathlib.Path(__file__).resolve().parent.parent
d = json.loads((root / "nanokontrol2/nanoKONTROL2-EOS.noisette").read_text(encoding="utf-8"))
extra = json.loads((root / "tools/templates.json").read_text(encoding="utf-8"))
S = {s["niceName"]: s for s in d["states"]["items"]}

def address(a):
    """Adresse OSC de la premiere consequence d'une Action (None si ce n'est pas une Action OSC)."""
    try:
        return next(q["value"] for q in a["consequences"]["items"][0]["command"]["parameters"] if q["controlAddress"] == "/address")
    except (KeyError, IndexError, StopIteration):
        return None

# Les modeles sont reperes par leur contenu, pas par le nom du State (libre de le renommer dans Chataigne) :
#  - commande tapee = Action qui envoie a /eos/cmd ; touche = Action qui envoie une autre adresse /eos/...
actions = [(s, a) for s in d["states"]["items"] if s["niceName"] != "INITIALISATION"
           for a in s["processors"]["items"] if a.get("type") == "Action" and address(a)]
cmd_state, cmd = next((s, a) for s, a in actions if address(a) == "/eos/cmd")
key = next(a for s, a in actions if address(a) != "/eos/cmd")
key, cmd = copy.deepcopy(key), copy.deepcopy(cmd)
shell = copy.deepcopy(cmd_state)                  # State vide servant de modele
shell["processors"]["items"] = []

d["states"]["items"] = [S["INITIALISATION"]]     # le reste est genere par la page

tpl = {"project": d, "state": shell, "keyAction": key, "cmdAction": cmd,
       "flashAction": extra["flashAction"], "mapping": extra["mapping"]}
data = json.dumps(tpl, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
src = (root / "tools/configurateur.src.html").read_text(encoding="utf-8")
(root / "docs/index.html").write_text(src.replace("__TEMPLATE__", data), encoding="utf-8")
print("docs/index.html regenere")
