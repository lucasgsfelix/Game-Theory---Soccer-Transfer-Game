"""Responsible to join two datasets"""
import pandas as pd
import numpy as np
from string_match import levenshtein_ratio_and_distance as distance


def comparsion(fifa_data, transfer_data):
	if fifa_data['Price'] == transfer_data['Price']:
		if str(fifa_data['Market Value']) == str(transfer_data['Market Value']):
			return True

def join_dataset():
	pass
if __name__ == '__main__':

	df_fifa = pd.read_table("Input/saida_fifa.txt", sep='\t')
	df_transfer = pd.read_table("Input/saida_transfermarkt.txt", sep='\t')


	df_fifa['Market Value'] = list(map(lambda x: str(x), df_fifa['Market Value']))
	# First jonning by Name, Market Value, Price
	df = pd.merge(df_fifa, df_transfer, on=['Name', 'Market Value', 'Price'])

	# Remove from the dataframes the values in the final dataframe (df)
	fifa_remove, transfer_remove = [], []
	for name, mv, p in zip(df['Name'], df['Market Value'], df['Price']):

		df_aux = df_fifa.loc[
						 	(df_fifa['Name'] == name) &
						 	(df_fifa['Market Value'] == mv) &
						 	(df_fifa['Price'] == p)
						 	]
		fifa_remove += list(df_aux.index)

		df_aux = df_transfer.loc[
							 	(df_transfer['Name'] == name) &
							 	(df_transfer['Market Value'] == mv) &
							 	(df_transfer['Price'] == p)
							 	]
		transfer_remove += list(df_aux.index)

	# removing lines there are already in the final dataset
	df_fifa.drop(fifa_remove, axis=0, inplace=True)
	df_transfer.drop(transfer_remove, axis=0, inplace=True)

	index_transfer= 0
	test_file = open("saida_teste.txt", 'w')
	for name, mv, p in zip(df_transfer['Name'], df_transfer['Market Value'], df_transfer['Price']):
		# selecting only the values with the same market value and price
		df_aux = df_fifa.loc[
						 	(df_fifa['Market Value'] == mv) &
						 	(df_fifa['Price'] == p)
						 	]

		for index, fifa_name in enumerate(df_aux['Name']):
			if distance(fifa_name, name) >= 0.9:
				no_name = df_aux.iloc[index].drop(['Name'], axis=0)
				player = pd.concat([no_name, df_transfer.iloc[index_transfer]])
				player.drop_duplicates('first', inplace=True)
				test_file.write('\t'.join(list(map(lambda x: str(x), player.tolist())))+'\n')

				#df.append(player, ignore_index=True)

		index_transfer += 1

	test_file.close()
	df.to_csv("teste.txt", sep='\t', index=False)