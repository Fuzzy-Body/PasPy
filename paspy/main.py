TOKEN_TYPES = INT, ADD, MINU, MUL, DIV, EOF = ('INT', 'ADD', 'MINU', 'MUL', 'DIV', 'EOF')


class Token(object):

    def __init__(self, type_, token):
        self.type_ = type_
        self.token = token


class Interpreter(object):

    def __init__(self, text):
        self.text = text
        self.pos = 0
        self.current_text = self.text[self.pos]
        self.current_token = self.get_next_token()

    def error(self):
        raise Exception("Syntax Error")

    def roll_next(self):
        self.pos += 1
        if self.pos > len(self.text) - 1:
            self.current_text = None
        else:
            self.current_text = self.text[self.pos]

    def skip_whitespaces(self):
        while self.current_text is not None and self.current_text.isspace():
            self.roll_next()

    def get_next_token(self):
        while self.current_text is not None: 
            value = self.current_text
            if value.isspace():
                self.skip_whitespaces()
                continue

            if value.isdigit():
                return Token(INT, self.integer())

            if value == '+':
                self.roll_next()
                return Token(ADD, value)
            if value == '-':
                self.roll_next()
                return Token(MINU, value)
            if value == '*':
                self.roll_next()
                return Token(MUL, value)
            if value == '/':
                self.roll_next()
                return Token(DIV, value)

            return self.error()

        return Token(EOF, None)

    def eat(self, type_):
        if self.current_token.type_ == type_:
            self.current_token = self.get_next_token()
        else:
            return self.error()

    def integer(self):
        result = '0'
        while self.current_text is not None and self.current_text.isdigit():
            result += self.current_text
            self.roll_next()
        return int(result)

    def factor(self):
        token = self.current_token
        self.eat(INT)
        return token.token

    def term(self):
        result = self.factor()
        while self.current_token.type_ in (MUL, DIV):
            token = self.current_token
            if token.type_ == MUL:
                self.eat(MUL)
                result = result * self.factor()
            elif token.type_ == DIV:
                self.eat(DIV)
                result = result / self.factor()
        return result

    def expr(self):
        result = self.term()
        while self.current_token.type_ in (ADD, MINU):
            token = self.current_token
            if token.type_ == ADD:
                self.eat(ADD)
                result = result + self.factor()
            elif token.type_ == MINU:
                self.eat(MINU)
                result = result - self.factor()
        return result


def main():
    text = raw_input() 
    print(Interpreter(text).expr())


if __name__ == "__main__":
    main()
