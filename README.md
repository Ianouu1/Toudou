# Toudou

The best todo application!

```bash
$ pip install pdm       # Python Dependency Manager is recommended
$ pdm install           # install project dependencies
$ pdm run toudou        # run the project
$ pdm run flask --app toudou.views --debug run # run the GUI

Usage: toudou [OPTIONS] COMMAND [ARGS]...

Options:
    --help  Show this message and exit.

Commands:
    display
```

Course & examples : [https://kathode.neocities.org](https://kathode.neocities.org)


Here's some commands that I've used for development & testing purpose. (Just left them here to reuse them later if needed😀)
```bash
pdm run toudou createtask --task "Nom_de_la_tache" --description "Description_de_la_tache" --date "1212-12-12 15:15:15" --status True
```
```bash
pdm run toudou updatetask -t "Faire les courses" -d "Acheter du lait et des oufs" -da "2024-05-10 08:00:00"
```
