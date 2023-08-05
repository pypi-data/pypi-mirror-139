import argparse


def getFunction():
    parser = argparse.ArgumentParser()
    parser.add_argument('name', type=str)
    parser.add_argument('age', type=str)
    args = parser.parse_args()
    print("My name is "+args.name+" and i'am " + args.age + " years old")