from src import functionTest


def testFunc():
    text = functionTest.getFunction("regie")
    assert text == "regie"