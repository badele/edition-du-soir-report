# Edition-du-soir-report
<!-- ALL-CONTRIBUTORS-BADGE:START - Do not remove or modify this section -->
[![All Contributors](https://img.shields.io/badge/all_contributors-10-orange.svg?style=flat-square)](#contributors-)
<!-- ALL-CONTRIBUTORS-BADGE:END -->

L'Édition du Soir est un sous-projet de l'initiative #DataAgainstCovid19
Pendant plus d'un mois, nous avons recueilli quotidiennement, dans des articles courts postés sur les réseaux sociaux:

- Le nombre de retours à domicile
- Le nombre de cas confirmés
- Le nombre de cas total en EHPAD
- Le nombre de cas confirmés en EHPAD
- Le nombre d'hospitalisations
- Le nombre de personnes en réanimation
- Le nombre de décès à l’hôpital
- Le nombre de décès en EHPAD ou EMS
- Le commentaire d'un expert du slack DataAgainstCovid19

Aujourd'hui, cette collection offre une vision synthétique des événements, dans un ordre chronologique, avec des éléments de contexte. Elle nous parait de nature à interesser le grand public ainsi que certains chercheurs. Dans cette optique, **Edition-du-soir-report** met en forme ces informations afin de favoriser leur consultation.

Concrètement, la présentation prend la forme d'un slideshow revealjs, exportable au format pdf et postscript, [hébergé sur github](https://guillaumefe.github.io/edition-du-soir-report).

## Génération du rapport quotidien

```
# A executer qu'une fois(la premiere fois)
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

```
source .venv/bin/activate

# Get last datas
#rm -rf /tmp/opencovid19
#git clone git@github.com:opencovid19-fr/data.git /tmp/opencovid19

# Convert datas
source .venv/bin/activate
python convert_to_csv.py -p /tmp/opencovid19/ministere-sante > index.html
```


## Contributors ✨

Thanks goes to these wonderful people ([emoji key](https://allcontributors.org/docs/en/emoji-key)):
<!-- ALL-CONTRIBUTORS-LIST:START - Do not remove or modify this section -->
<!-- prettier-ignore-start -->
<!-- markdownlint-disable -->
<table>
  <tr>
    <td align="center"><a href="https://github.com/mtaieb"><img src="https://avatars2.githubusercontent.com/u/3834341?v=4" width="100px;" alt=""/><br /><sub><b>mtaieb</b></sub></a><br /><a href="#data-mtaieb" title="Data">🔣</a> <a href="#ideas-mtaieb" title="Ideas, Planning, & Feedback">🤔</a> <a href="#eventOrganizing-mtaieb" title="Event Organizing">📋</a> <a href="#projectManagement-mtaieb" title="Project Management">📆</a> <a href="https://github.com/guillaumefe/edition-du-soir-report/pulls?q=is%3Apr+reviewed-by%3Amtaieb" title="Reviewed Pull Requests">👀</a></td>
    <td align="center"><a href="https://sandrineh.github.io/"><img src="https://avatars0.githubusercontent.com/u/15267900?v=4" width="100px;" alt=""/><br /><sub><b>Sandrine</b></sub></a><br /><a href="#eventOrganizing-sandrineh" title="Event Organizing">📋</a> <a href="#projectManagement-sandrineh" title="Project Management">📆</a> <a href="#content-sandrineh" title="Content">🖋</a> <a href="https://github.com/guillaumefe/edition-du-soir-report/pulls?q=is%3Apr+reviewed-by%3Asandrineh" title="Reviewed Pull Requests">👀</a></td>
    <td align="center"><a href="https://github.com/abdoulsn"><img src="https://avatars2.githubusercontent.com/u/33933023?v=4" width="100px;" alt=""/><br /><sub><b>Abdoulaye</b></sub></a><br /><a href="#content-abdoulsn" title="Content">🖋</a> <a href="#tool-abdoulsn" title="Tools">🔧</a> <a href="https://github.com/guillaumefe/edition-du-soir-report/commits?author=abdoulsn" title="Tests">⚠️</a> <a href="#eventOrganizing-abdoulsn" title="Event Organizing">📋</a> <a href="https://github.com/guillaumefe/edition-du-soir-report/pulls?q=is%3Apr+reviewed-by%3Aabdoulsn" title="Reviewed Pull Requests">👀</a></td>
    <td align="center"><a href="https://melissasalucci.myportfolio.com"><img src="https://avatars3.githubusercontent.com/u/60431041?v=4" width="100px;" alt=""/><br /><sub><b>melissa-salucci</b></sub></a><br /><a href="#projectManagement-melissa-salucci" title="Project Management">📆</a> <a href="#ideas-melissa-salucci" title="Ideas, Planning, & Feedback">🤔</a> <a href="https://github.com/guillaumefe/edition-du-soir-report/pulls?q=is%3Apr+reviewed-by%3Amelissa-salucci" title="Reviewed Pull Requests">👀</a></td>
    <td align="center"><a href="https://github.com/Mouvoh"><img src="https://avatars3.githubusercontent.com/u/62729599?v=4" width="100px;" alt=""/><br /><sub><b>mouvoh</b></sub></a><br /><a href="https://github.com/guillaumefe/edition-du-soir-report/commits?author=Mouvoh" title="Tests">⚠️</a> <a href="#content-Mouvoh" title="Content">🖋</a></td>
    <td align="center"><a href="https://github.com/Dowser101"><img src="https://avatars0.githubusercontent.com/u/62883351?v=4" width="100px;" alt=""/><br /><sub><b>Dowser101</b></sub></a><br /><a href="#data-Dowser101" title="Data">🔣</a> <a href="https://github.com/guillaumefe/edition-du-soir-report/pulls?q=is%3Apr+reviewed-by%3ADowser101" title="Reviewed Pull Requests">👀</a> <a href="#content-Dowser101" title="Content">🖋</a></td>
    <td align="center"><a href="https://github.com/elenablum26"><img src="https://avatars1.githubusercontent.com/u/65129550?v=4" width="100px;" alt=""/><br /><sub><b>elenablum26</b></sub></a><br /><a href="#eventOrganizing-elenablum26" title="Event Organizing">📋</a> <a href="#projectManagement-elenablum26" title="Project Management">📆</a> <a href="https://github.com/guillaumefe/edition-du-soir-report/pulls?q=is%3Apr+reviewed-by%3Aelenablum26" title="Reviewed Pull Requests">👀</a></td>
  </tr>
  <tr>
    <td align="center"><a href="http://bruno.adele.im"><img src="https://avatars0.githubusercontent.com/u/2806307?v=4" width="100px;" alt=""/><br /><sub><b>Bruno Adele</b></sub></a><br /><a href="#content-badele" title="Content">🖋</a> <a href="#ideas-badele" title="Ideas, Planning, & Feedback">🤔</a> <a href="https://github.com/guillaumefe/edition-du-soir-report/commits?author=badele" title="Code">💻</a></td>
    <td align="center"><a href="https://www.facebook.com/guillaume.ferron"><img src="https://avatars1.githubusercontent.com/u/12534077?v=4" width="100px;" alt=""/><br /><sub><b>Guillaume Fe</b></sub></a><br /><a href="#eventOrganizing-guillaumefe" title="Event Organizing">📋</a> <a href="#projectManagement-guillaumefe" title="Project Management">📆</a> <a href="#tool-guillaumefe" title="Tools">🔧</a> <a href="#ideas-guillaumefe" title="Ideas, Planning, & Feedback">🤔</a> <a href="https://github.com/guillaumefe/edition-du-soir-report/pulls?q=is%3Apr+reviewed-by%3Aguillaumefe" title="Reviewed Pull Requests">👀</a></td>
    <td align="center"><a href="https://github.com/jdesboeufs"><img src="https://avatars2.githubusercontent.com/u/1231232?v=4" width="100px;" alt=""/><br /><sub><b>Jérôme Desboeufs</b></sub></a><br /><a href="#data-jdesboeufs" title="Data">🔣</a></td>
  </tr>
</table>

<!-- markdownlint-enable -->
<!-- prettier-ignore-end -->
<!-- ALL-CONTRIBUTORS-LIST:END -->

This project follows the [all-contributors](https://github.com/all-contributors/all-contributors) specification. Contributions of any kind welcome!
