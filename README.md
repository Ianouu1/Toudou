# Toudou

The best todo application!

```bash
$ pip install pdm       # Python Dependency Manager is recommended
$ pdm install           # install project dependencies
$ pdm run toudou        # run the cli
$ pdm run start # run the projet

Usage: toudou [OPTIONS] COMMAND [ARGS]...

Options:
    --help  Show this message and exit.

Commands:
    display
```

Course & examples : [https://kathode.neocities.org](https://kathode.neocities.org)

You can access the API after running the project by using : 
```bash
$ pdm run start
```
Then you can go to http://localhost:5000/apidoc/swagger/

However, we cannot update a task through the API because I didn't have enough time to finish.
Also, the POST method to create a task isn't working. 

I also used Hypercorn since Uvicorn wasn't working for me