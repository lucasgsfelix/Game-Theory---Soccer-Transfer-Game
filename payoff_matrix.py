"""  Measure the values of the payoff matrix for a two team transaction. """


def _evaluate_key(t, token):
    """
        Responsible to evaluate if a token is the transfers dict
        After evaluation, a model a equation is generated or the
        payoff value.
    """

    # alfa (market_value  + importancia_dinheiro_seller/buyer)
    if token not in t.keys():

        string_value = token + ' + ' + str(t['Market Value'])

    else: # them this value is not a string

        if 'Buyer' in token:
            string_value = t['Imp. Money - Buyer']
        else:
            string_value  = t['Imp. Money - Seller']

        string_value += t['Market Value']

    if 'alpha' in t.keys(): # them there is a alpha value

        if isinstance(string_value, str):

            return str(t['alpha']) + '(' + string_value + ')'

        else: # in this case is not a string value

            return round(t['alpha'] * string_value, 3)

    # when there is no alpha value

    if isinstance(string_value, str):

        return "alpha" + '(' + string_value + ')'

    else: # in this case is not a string value

        return "alpha(" + str(round(string_value, 3)) + ")"


def _evaluate_instance(measure, team, sign = '+'):
    """
        Responsible to better define if the output of the method
        will be a str or a int
    """
    if isinstance(measure, str):
        return str(team) + ' ' + sign + ' ' + measure

    return team + measure


def _evaluate_simple_key(t, verify_token, token, sign):
    """
        Evaluate and parsing of more simple cases of key tretment
    """
    if verify_token not in t.keys():
        if sign == '+':
            return str(t[token]) + ' + ' + verify_token
        else:
            return str(t[token]) + ' - ' + verify_token

    if sign == '+':
        return t[token] + t[verify_token]

    return t[token] - t[verify_token]


def transfer_sell_buy(t):
    """ 
        Given as enter the transfer info will return the payoff
        of a sell-buy transfer.
    """

    buyer = t['Imp. Player - Buyer'] - t['Market Value'] - t['Imp. Money - Buyer'] 
    seller = t['Market Value'] + t['Imp. Money - Seller'] - t['Imp. Player - Seller']

    return round(seller, 3), round(buyer, 3)


def transfer_sell_trade(t):
    """
        Given as enter the transfer info, will return the payoff
        to a sell-trade transfer.
    """
    seller = _evaluate_simple_key(t, 'Imp. Player Off. - Seller',
                                 'Imp. Player - Seller', '-')
    measure = _evaluate_key(t, 'Imp. Money - Seller')
    seller = _evaluate_instance(measure, seller, '-')

    buyer = _evaluate_simple_key(t, 'Imp. Player Off. - Buyer',
                                'Imp. Player - Seller', '-')
    measure = _evaluate_key(t, 'Imp. Money - Buyer')
    buyer = _evaluate_instance(measure, buyer, '+')

    return seller, buyer


def transfer_not_negotiate_buy(t):
    """
        Given as enter the transfer info, will return the payoff
        to a not negotiate-buy transfer.
    """
    seller = t['Imp. Player - Seller'] - t['Imp. Money - Seller'] - t['Market Value']
    buyer = t['Imp. Money - Buyer'] - t['Market Value'] - t['Imp. Player - Buyer']

    return round(seller, 3), round(buyer, 3)

def transfer_not_negotiate_trade(t):
    """
        Given as enter the transfer info, will return the payoff
        to a not negotiate-trade transfer.
    """
    return transfer_sell_trade(t)


def transfer_trade_buy(t):
    """
        Given as enter the transfer info, will return the payoff
        to a not trade-buy transfer.
    """

    seller = _evaluate_simple_key(t, 'Imp. Player Off. - Seller',
                                 'Imp. Player - Seller', '-')
    measure = _evaluate_key(t, 'Imp. Money - Seller')
    seller = _evaluate_instance(measure, seller, '-')

    buyer = t['Imp. Money - Buyer'] + t['Market Value'] - t['Imp. Player - Buyer']

    return seller, buyer


def transfer_trade_trade(t):
    """
        Given as enter the transfer info, will return the payoff
        to a trade-trade transfer.
    """

    if 'Imp. Player Off. - Seller' not in t.keys():
        seller = 'Imp. Player Off. - Seller' + ' - ' + str(t['Imp. Player - Seller'])
    else:
        seller = t['Imp. Player Off. - Seller'] - t['Imp. Player - Seller']

    measure = _evaluate_key(t, 'Imp. Money - Seller') # add the alpha part
    seller = _evaluate_instance(measure, seller, '+')

    buyer = _evaluate_simple_key(t, 'Imp. Player Off. - Buyer',
                                 'Imp. Player - Buyer', '-')
    measure = _evaluate_key(t, 'Imp. Money - Buyer') # add the alpha part
    buyer = _evaluate_instance(measure, buyer, '-')

    return seller, buyer


def mount_latex_table(transfer_matrix):

    for key in transfer_matrix.keys():
        transfer_matrix[key] = ''.join(str(transfer_matrix[key]))
        transfer_matrix[key] = transfer_matrix[key].replace("'", '')
        transfer_matrix[key] = transfer_matrix[key].replace('[', '')
        transfer_matrix[key] = transfer_matrix[key].replace(']', '')
        transfer_matrix[key] = transfer_matrix[key].replace('alpha', '\\alpha')


    table = "Sell & " + transfer_matrix['Sell-Buy'] + ' & ' + transfer_matrix['Sell-Trade'] + '\\\\ \\hline \n'
    table += "Not Negotiate & " + transfer_matrix['Not Negotiate-Buy'] + ' & ' + transfer_matrix['Not Negotiate-Trade'] + '\\\\ \\hline \n'
    table += "Trade & " + transfer_matrix['Trade-Buy'] + ' & ' + transfer_matrix['Trade-Trade'] + '\\\\ \\hline \n'

    print(table)

if __name__ == '__main__':

    transfer_info = {}

    # Player normalized Market Value
    transfer_info['Market Value'] = 0.4

    ## Importance of the Player
    transfer_info['Imp. Player - Seller'] = 1
    transfer_info['Imp. Player - Buyer'] = 0.89

    ## Importance of the Money
    transfer_info['Imp. Money - Seller'] = 1.764
    transfer_info['Imp. Money - Buyer'] = 0.735

    transfer_matrix = {}
    transfer_matrix['Sell-Buy'] = transfer_sell_buy(transfer_info)
    transfer_matrix['Sell-Trade'] = transfer_sell_trade(transfer_info)
    transfer_matrix['Not Negotiate-Buy'] = transfer_not_negotiate_buy(transfer_info)
    transfer_matrix['Not Negotiate-Trade'] = transfer_not_negotiate_trade(transfer_info)
    transfer_matrix['Trade-Buy'] = transfer_trade_buy(transfer_info)
    transfer_matrix['Trade-Trade'] = transfer_trade_trade(transfer_info)

    latex_symbol = {'alpha': '\\alpha', 'Imp. Player Off. - Seller': 'I_s^S',
                    'Imp. Player Off. - Buyer': 'I_s^B'}
    for key in transfer_matrix.keys():
        transfer_matrix[key] = list(transfer_matrix[key])

    for key in transfer_matrix.keys():
        for index, value in enumerate(transfer_matrix[key]):
            for symbol in latex_symbol.keys():
                if symbol in str(value):
                    transfer_matrix[key][index] = '$ ' + value.replace(symbol, latex_symbol[symbol]) + ' $'

    mount_latex_table(transfer_matrix)