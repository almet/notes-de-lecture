# Notes de lecture

Un petit outil pour avoir une meilleure organisation de mes notes de lecture.
A partir d'un ensemble de fichiers au format ``.yaml``, créé un petit site web statique.

Les notes sont disponibles à l'adresse [https://lectures.notmyidea.org](https://lectures.notmyidea.org)

Voici comment l'installer :

    git clone https://github.com/almet/notes-de-lecture.git
    cd notes-de-lecture/readingnotes
    pip3 install -e .

Puis, simplement :

    readingnotes notes output && python3 http.server --directory output
