__docformat__ = 'restructuredtext en'

# -----------------------------------------------------------------------------
#  _                            _
# (_)_ __ ___  _ __   ___  _ __| |_ ___
# | | '_ ` _ \| '_ \ / _ \| '__| __/ __|
# | | | | | | | |_) | (_) | |  | |_\__ \
# |_|_| |_| |_| .__/ \___/|_|   \__|___/
#             |_|
# -----------------------------------------------------------------------------
#
import pyparsing as pp
import jc2cli.tools.loggerator as loggerator


# -----------------------------------------------------------------------------
#
#   ___ ___  _ __  ___| |_ __ _ _ __ | |_ ___
#  / __/ _ \| '_ \/ __| __/ _` | '_ \| __/ __|
# | (_| (_) | | | \__ \ || (_| | | | | |_\__ \
#  \___\___/|_| |_|___/\__\__,_|_| |_|\__|___/
#
# -----------------------------------------------------------------------------
#
MODULE = 'PARSER.parser'
logger = loggerator.getLoggerator(MODULE)


# -----------------------------------------------------------------------------
#            _                     _   _
#  ___ _   _| |__  _ __ ___  _   _| |_(_)_ __   ___  ___
# / __| | | | '_ \| '__/ _ \| | | | __| | '_ \ / _ \/ __|
# \__ \ |_| | |_) | | | (_) | |_| | |_| | | | |  __/\__ \
# |___/\__,_|_.__/|_|  \___/ \__,_|\__|_|_| |_|\___||___/
#
# -----------------------------------------------------------------------------
#
def _map_parent_type_to_op(parent_type):
    """Provide the operation type to use given the parent type for the rule.

    Rule for free-form parameters set the type to '3', parent has a rule
    type '@'.

    Rule for required parameters set the type to '1'.

    Args:
        parent_type (str) : Character with the parent type rule.

    Returns:
        str : Character with the operation type to be used.
    """
    if not parent_type:
        return '1'
    elif parent_type == '@':
        return '3'
    elif parent_type in '?+*!':
        return '4'
    else:
        return '1'


def process_tokens(tokens, withend=True, parent_type=None):
    """Function that process given tokens.

    Rule types are:

        - '1' : Required parameter. Default value should be always None.

        - '2' : Constant parameter. It can be required or optional. From '<x>'
          syntax.

        - '3' : Free-for parameter from '@' syntax. Required.

        - '?' : zero or one parameters. Always optional.

        - '*' : zero or more parameters. Always optional.

        - '+' : one or more parameters. Always optional.

        - '!' : one optional parameter. Required.

    Args:
        tokens (list): list of tokens to parse.
        withend (boolean): True if last rule has to be added at the end,
        False else.

    Returns:
        list: list of dictionaries with all rules.
    """
    rules, counter = [], 0
    for tok in tokens:
        toktype = type(tok)
        op = _map_parent_type_to_op(parent_type)
        if tok == '|':
            counter = 0
            continue
        elif toktype == str:
            # rule for constant parameters set the type to '2'
            if tok.startswith('<') and tok.endswith('>'):
                rules.append({'counter': counter, 'type': '2', 'args': tok[1:-1]})
            else:
                rules.append({'counter': counter, 'type': op, 'args': tok})
        elif toktype == list and len(tok) == 1:
            rules.append({'counter': counter, 'type': op, 'args': tok[0]})
        elif toktype in [pp.ParseResults, list]:
            tok = tok.asList()[0] if toktype == pp.ParseResults else tok
            op = tok[-1]
            if type(op) == str and op in '?+*!@':
                tok.pop()
            else:
                op = '1'
            rules.append({'counter': counter, 'type': op, 'args': process_tokens(tok, False, op)})
        else:
            logger.error('Invalid Syntax', out=True)
        counter += 1
    if withend:
        rules.append({'counter': counter, 'type': '0', 'args': None})
    return rules


def _process_syntax(tokens):
    """Function that process a syntas for the given tokens.

    Args:
        tokens (list): list of tokens to parse.

    Returns:
        tuple: pair with the commadn and a list of dictionaries with all rules.
    """
    command = tokens[0]
    rules = process_tokens(tokens[1:])
    return command, rules


def get_syntax():
    """Function that return the syntax to be used for processing.

    Returns:
        object: syntax used for parsing.
    """
    command = pp.Word(pp.alphanums + "-").setName('command')
    posarg = pp.Word(pp.alphanums + "-<>").setName('pos-arg')

    lbracket = pp.Suppress("[")
    rbracket = pp.Suppress("]")
    zero_or_one_flag = "?"
    zero_or_more_flag = "*"
    one_or_more_flag = "+"
    only_1_opt_flag = "!"
    freeform_flag = "@"
    argo = pp.Word(pp.alphanums + "-").setName('argument')
    cto = pp.Word(pp.alphanums + "-<>").setName('constant')

    zero_or_one = pp.Forward()
    zero_or_one.setName('zero-or-one')
    zero_or_one_block = pp.ZeroOrMore(("|" + pp.OneOrMore(argo | zero_or_one)) | pp.OneOrMore(zero_or_one))
    zero_or_one << pp.Group(lbracket + pp.ZeroOrMore(argo) + zero_or_one_block + rbracket + zero_or_one_flag)

    zero_or_more = pp.Forward()
    zero_or_more_block = pp.ZeroOrMore(("|" + pp.OneOrMore(argo | zero_or_more)) | pp.OneOrMore(zero_or_more))
    zero_or_more << pp.Group(lbracket + pp.ZeroOrMore(argo) + zero_or_more_block + rbracket + zero_or_more_flag)
    zero_or_more.setResultsName('zero-or-more')

    one_or_more = pp.Forward()
    one_or_more_block = pp.ZeroOrMore(("|" + pp.OneOrMore(argo | one_or_more)) | pp.OneOrMore(one_or_more))
    one_or_more << pp.Group(lbracket + pp.ZeroOrMore(argo) + one_or_more_block + rbracket + one_or_more_flag)
    one_or_more.setName('one-or-more')

    only_1_opt = pp.Forward()
    only_1_opt_block = pp.ZeroOrMore(("|" + pp.OneOrMore(cto | only_1_opt)) | pp.OneOrMore(only_1_opt))
    only_1_opt << pp.Group(lbracket + pp.ZeroOrMore(cto) + only_1_opt_block + rbracket + only_1_opt_flag)
    only_1_opt.setName('one-1-option')

    freeform = pp.Forward()
    freeform_block = pp.ZeroOrMore(("|" + pp.OneOrMore(argo | freeform)) | pp.OneOrMore(freeform))
    freeform << pp.Group(lbracket + pp.ZeroOrMore(argo) + freeform_block + rbracket + freeform_flag)
    freeform.setName('free-form')

    options = pp.ZeroOrMore(posarg | pp.Group(zero_or_one | zero_or_more | one_or_more | only_1_opt | freeform))
    syntax = command + pp.ZeroOrMore(posarg) + options
    return (syntax + pp.stringEnd)


def process_syntax(syntax):
    """
    """
    toks = get_syntax().parseString(syntax)
    cmd, rules = _process_syntax(toks)
    return cmd, rules


# -----------------------------------------------------------------------------
#                  _
#  _ __ ___   __ _(_)_ __
# | '_ ` _ \ / _` | | '_ \
# | | | | | | (_| | | | | |
# |_| |_| |_|\__,_|_|_| |_|
#
# -----------------------------------------------------------------------------
#
if __name__ == '__main__':
    # toks = (syntax + pp.stringEnd).parseString("tenant tname [t1|t2]? [t3|t4]* [t10]? [t5|t6]+")
    # toks = (syntax + pp.stringEnd).parseString("tenant tpos1 [tzoo1 | tzoo2 tzoo3 [ tzoo31 ]? ]? [tzom1]* [toom1]+")
    # toks = (syntax + pp.stringEnd).parseString("tenant tpos1 [tzoo1 | tzoo2 tzoo3 [tzoo31 | tzoo32 | tzoo33]? ]? [tzom1]* [toom1]+")

    # toks = (syntax + pp.stringEnd).parseString("tenant tname [tid | tsignature]? [talias]* [tdesc | thelp]+ [tclose]?")
    # toks = (syntax + pp.stringEnd).parseString("tenant tname [tid | tdesc talias | tsignature | tuser [tuname | tuid]? ]?")
    # toks = (syntax + pp.stringEnd).parseString("tenant tname [tid | tuid [tlastname | tpassport]? ]? [thelp | tdesc]* [tsignature]+")
    # toks = get_syntax().parseString("tenant t1 [<t2> | t3]!")
    # toks = get_syntax().parseString("tenant t1 <t2>")
    # toks = get_syntax().parseString("tenant [t1 t2 t3]+")
    # toks = get_syntax().parseString("tenant t1 [t2]@")
    # toks = get_syntax().parseString("tenant t1 [t2 | t3]*")
    # toks = get_syntax().parseString("tenant t1 [t2]? [t3]?")
    # toks = get_syntax().parseString("tenant t1 <t2>")
    toks = get_syntax().parseString("tenant t1 [t2 t3]? t4 [t5 | t6]?")
    # toks = get_syntax().parseString("tenant t1 [<t2> | <t3>]! t4")

    logger.display(toks, log=False)
    cmd, rules = _process_syntax(toks)
    logger.display(cmd, log=False)
    for rule in rules:
        logger.display(rule, log=False)
