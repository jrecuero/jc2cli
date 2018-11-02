class Token:

    CR = '<<<_CR_>>>'

    @staticmethod
    def is_cr_token(token):
        return token == Token.CR
