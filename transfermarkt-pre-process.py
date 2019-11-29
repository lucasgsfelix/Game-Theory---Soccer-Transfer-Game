"""Responsible to pre-process Transfermarkt Dataset"""
import re


def read_file(file_name):
	"""Read and Split File"""
	with open(file_name, 'r') as file:
		data = file.read().split('\n')
	
	return list(map(lambda x: x.split('\t'), data))


def parse_money_value(value):

	if value == '-':
		return value

	values_dict = {'Mill.': '0000', 'Th.': '000'}
	value = value.replace('€', '')

	if 'Loan' in value:
		value = value.replace('Loan fee:', '')

	value = value.replace(',', '')

	#Loan fee:
	for cipher in values_dict.keys():
		if cipher in value:
			value = value.replace(cipher, '').replace(' ', '')
			return  value + values_dict[cipher]

	return '0'


def retrieve_name(transfer):

	for feature in transfer:
		if not re.match(r'[\d]+', feature):
			return feature


def retrieve_market_value(transfer):

	# then we have the market value
	values = list(filter(lambda x: '€' in x, transfer))
	if len(values) == 2:
		return values[0]
	else:
		return '-'

def retrieve_teams(transfer):

	for index, feature in enumerate(transfer):
		if feature == '-' or '€' in feature:
			return transfer[index+2], transfer[index+4]


def write_file(data, file_name='Input/saida_transfermarkt.txt'):

	with open(file_name, 'w') as file:

		header = ['Name', 'Market Value', 'Transfer Value',
				 'Team A', 'Team B', 'Transfer Type']
		file.write('\t'.join(header) + '\n')

		for transfer in data:
			transfer_aux = list(transfer.values())			
			file.write('\t'.join(transfer_aux) + '\n')


if __name__ == '__main__':


	data = read_file('Data/transfermarkt.txt')

	# Data I need to retrieve:
	# Player Name, Market Value, Transfer Value, Team A, Team B, Tranfer Type

	transfers = []
	for transfer in data:
		player_info = {}

		player_info['Name'] = retrieve_name(transfer)
		player_info['Market Value'] = retrieve_market_value(transfer)
		player_info['Market Value'] = parse_money_value(player_info['Market Value'])
		player_info['Tranfer Value'] = parse_money_value(transfer[-1])

		team_a, team_b = retrieve_teams(transfer)
		player_info['Team A'] = team_a
		player_info['Team B'] = team_b

		if 'Loan' in transfer[-1]:
			player_info['Tranfer Type'] = 'Loan'
		else:
			player_info['Tranfer Type'] = 'Sell'

		transfers.append(player_info)

	write_file(transfers)
