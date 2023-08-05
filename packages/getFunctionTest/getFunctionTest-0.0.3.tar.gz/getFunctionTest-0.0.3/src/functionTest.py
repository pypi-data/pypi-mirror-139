import typer


app = typer.Typer()


def getFunction(name: str):
    # changes
    print(name)
    return name


if __name__ == "__main__":
    typer.run(getFunction)
