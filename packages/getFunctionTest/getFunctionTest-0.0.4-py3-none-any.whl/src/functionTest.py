import argparse

parser = argparse.ArgumentParser()
parser.add_argument('name', type=str)
parser.add_argument('age', type=str)
args = parser.parse_args()


def getFunction(name, age):
    text = "My name is "+name+" and i'am " + age + " years old"
    return text


if __name__ == '__main__':
    print(getFunction(args.name, args.age))
