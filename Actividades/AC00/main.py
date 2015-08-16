# coding=utf-8


class User:

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return 'My name is: {}'.format(self.name)


if __name__ == '__main__':
    user = User('Lorena Ipsum')
    print(user)
