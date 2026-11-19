# ShuttleXpress → ETC Eos (Chataigne)

🇬🇧 [English version](README.en.md)

Projet [Chataigne](https://github.com/benkuper/Chataigne) prêt à l'emploi pour piloter **ETC Eos / ETCnomad** avec un **Contour ShuttleXpress**, via la passerelle [ShuttleXpressOSC](https://github.com/100ders/shuttleXpress-OSC). Sans script : tout est dans les States de Chataigne.

```
ShuttleXpress ──USB──▶ ShuttleOSC ──OSC :9000──▶ Chataigne ──OSC :8000──▶ Eos
                                                    ▲                       │
                                                    └──── OSC :9000 ────────┘ (optionnel)
```

## Fonctions
| Contrôle | Action |
|---|---|
| Bouton 1 | Mode **Intensité** (page d'encodeurs Eos : Intensity) |
| Bouton 2 | Mode **Pan** (page Focus) |
| Bouton 3 | **Home** sur la sélection (`/eos/at/home`) |
| Bouton 4 | Mode **Tilt** (page Focus) |
| Bouton 5 | Mode **Zoom** (page Form) |
| Jog (molette) | Réglage pas à pas du paramètre du mode actif |
| Bague (à ressort) | Mouvement continu du paramètre actif ; s'arrête au relâchement |

Un seul mode est actif à la fois (Pan au démarrage). Chaque changement de mode coupe d'abord tout mouvement de bague en cours et bascule la page d'encodeurs d'Eos pour indiquer le paramètre piloté.

## Prérequis
- [Chataigne](https://github.com/benkuper/Chataigne) **1.9.24** (testé avec cette version) : [page de téléchargement](https://benjamin.kuperberg.fr/chataigne/).
- ETC Eos / ETCnomad (testé avec ETCnomad sous Windows, mode Offline).
- La passerelle **ShuttleOSC** lancée, envoyant vers le port **9000**.

## Paramétrage d'Eos
Voir aussi le [paramétrage OSC d'Eos](../docs/eos-osc-setup.md), avec la vérification dans `Tab 99`.

Dans Eos : **Setup › Réglages Système › Show Control › OSC**

| Réglage | Valeur | Rôle |
|---|---|---|
| OSC RX | **Activé** | Eos reçoit les commandes de Chataigne |
| OSC UDP RX Port | **8000** | Port de réception d'Eos |
| OSC TX | Activé *(optionnel)* | Retour d'information vers Chataigne |
| OSC UDP TX IP Address | `127.0.0.1` *(si Chataigne est sur le même ordinateur, sinon son IP)* | Destination du retour |
| OSC UDP TX Port | **9000** | Port d'écoute de Chataigne |

Notes :
- Ce projet fonctionne **sans** OSC TX. Le TX est nécessaire seulement pour les commandes `/eos/active/wheel/…` et pour afficher des informations d'Eos dans Chataigne.
- Sous Windows, autoriser Chataigne (et Eos) dans le pare-feu au premier lancement.
- **Diagnostic** : `Tab 99` dans Eos affiche les messages OSC reçus (`RECV`) et envoyés (`SEND`).
- Les commandes s'appliquent aux **canaux sélectionnés** : sélectionner un projecteur avant d'utiliser le Shuttle.

## Paramétrage de Chataigne
1. Ouvrir `Shuttle-EOS.noisette`.
2. Module **OSC** :
   - *Input* : port local **9000** ;
   - *Output* : hôte `127.0.0.1` (ou l'IP de l'ordinateur Eos), port **8000**.
3. Lancer ShuttleOSC, sélectionner un projecteur dans Eos, tourner le jog.

## Personnalisation
| Pour… | Modifier |
|---|---|
| Changer la vitesse du jog | L'argument des Actions `JOG +` / `JOG -` de chaque State (2 / -2 par défaut) |
| Changer la vitesse de la bague | Le filtre **Remap** du Mapping `BAGUE …` (sortie -3…3 ; -1…1 pour l'intensité) |
| Piloter un autre paramètre | L'adresse `/eos/wheel/coarse/<paramètre>` et `/eos/switch/<paramètre>` dans un State JOG |
| Réglage plus fin | Remplacer `coarse` par `fine` et augmenter l'argument (un cran *fine* est très petit) |
| Réaffecter un bouton | La condition `/shuttle/button/<n>` de l'Action dans le State **BOUTONS** |

## Dépannage
| Symptôme | Piste |
|---|---|
| Rien ne bouge | ShuttleOSC lancé ? Module OSC sur le port 9000 ? Projecteur sélectionné ? OSC RX activé ? |
| Messages reçus dans `Tab 99` mais pas de mouvement | Un cran *fine* est presque invisible : utiliser *coarse* ou un argument plus grand |
| `invalid active parameter` dans `Tab 99` | Concerne `/eos/active/wheel/…` : activer **OSC TX** dans Eos et resélectionner le projecteur |
| La page d'encodeurs ne change pas | Vérifier dans `Tab 99` la réception de `/eos/key/encoder_category_…` |
| Le paramètre continue de bouger | Remettre la bague au centre ; en secours, envoyer `/eos/reset` |

## Limites connues
- **Home** ramène tous les paramètres sélectionnés à leur position par défaut, pas seulement pan/tilt.
- Le mode **Intensité** (`/eos/wheel/level`, `/eos/switch/level`) est le moins testé.

---

📜 GPL v3 · Projet indépendant, non affilié à Contour Design, ETC ni Chataigne.
