# Utilitaires pour le projet Coronavirus COVID-19 - France dataset

## Introduction
Ce projet contient 3 utilitaires afin de faciliter le travail de consolidation
des données France de la pandémie COVID-19 [url du
projet](https://github.com/lperez31/coronavirus-france-dataset) :

* git-fork-maintenance.sh
* patient-utils.py
* merge-files.sh

## Usage

### TL;DR
Voici le workflow lors de la mise à jour quotidienne des données :

* lancement de `git-fork-maintenance.sh`
* For each ajout de données (groupé par [region|departement|ville|status|...])
    * lancement de `patient-utils.py`
    * lancement de `merge-files.sh`

### Maintenance des forks locaux par rapport au projet Master
> git-fork-maintenance.sh

Le premier utilitaire permet de maintenir toujours à jour le projet local du
contributeur par rapport au projet master. Voici comment il s'utilise :

```bash
$ ./src/git-fork-maintenance.sh <absolute/path/to/repo>
```
**IMPORTANT** Toujours mettre à jour les branches du repo local avant de faire
de nouvelles modifications.

### Ajout de nouvelles données consolidées
> patient-utils.py

Le second utilitaire permet d'ajouter en masse de nouvelles données dans le
fichier `patient.csv`.

Par soucis de sécurité, l'utilitaire ne modifie pas le fichier source mais
génère un nouveau fichier, copie du ficher source avec l'ajout des nouvelles
données. Ce fichier se trouve ici : `./_tmp/patient-tmp.csv`.

L'utilitaire a pour arguments les différentes colonnes du fichier `patient.csv`
+ deux arguments supplémentaires :
* mode : [stats|add]
* occurrence : nombre de lignes à ajouter

Il s'utilise de la manière suivante :
```bash
$  python src/patient-utils.py --mode add --region 'Ile-de-France' --source 'CP ARS Ile-de-France' --confirmed_date 2020-03-15 --departement 'DELETE' --occurrence 1
```
Cette commande ajoute *1* ligne dont la région est *Ile-de-France*, la source *CP
ARS Ile-de-France*, pour une date de confirmation au *15 mars 2020*, pour le
département *DELETE*.

### Merge avec le fichier source
> merge-files.sh

Ce dernier utilitaire permet de merger le fichier `patient-tmp.csv` avec le
fichier master `patient.csv`.

Pour cela, il suffit de lancer la commande suivante :
```bash
$ ./src/merge-files.sh <nombre d'occurrences ajoutées>
```
Cette commande effectue les actions suivantes :
* Créé une copie de sauvegarde du fichier `patient.csv`
* Copie les lignes ajoutées depuis le fichier `patient-tmp.csv` vers le fichier `patient.csv`
* Confirme que la copie a bien eu lieu et lance un `git diff` afin de vérifier
que seules les lignes ajoutées sont considérées par git comme modification du
fichier.

**IMPORTANT** Il est indispensable d'effectuer le merge avec le fichier source à
chaque nouveau ajout de lignes.

## Limitation
Le script `patient-utils.py` ne reconnait, pour les régions, que celles ayant déjà
une personne contaminée recensée.

**Pour toute nouvelle région contaminée, il est
nécessaire de modifier le script pour y ajouter le nom de cette région dans la
liste des choix disponibles**

## Bonus
L'utilitaire `patient-utils.py` permet d'obtenir rapidement des stats sur une
région donnée. Voici comment l'utiliser :
```bash
$ python src/patient-utils.py --mode stats --region 'Bretagne'
```
