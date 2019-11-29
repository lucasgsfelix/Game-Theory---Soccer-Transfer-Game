"""Pre-Processing FIFA dataset"""

import pandas as pd
import statistics

def overall_measure(player):

	return statistics.median(player)


if __name__ == '__main__':

	df = pd.read_table("Data/transfer_fifa.txt", sep = '\t')

	# From this df I will retrieve:
	# Player Name, Overall, Birth Place, Birth Date, Market Value, Price
	overall = []
	for _, row in df.iterrows():
		row.drop(['Name', 'Birth Place', 'Birth Date',
				  'Market Value', 'Price', 'Preferred Positions',
				  'Preferred Foot', 'Game Edition',
				  'Height', 'Weight'], inplace=True)
		#print(row)
		overall.append(overall_measure(row))


	columns = ['Name', 'Birth Place', 'Birth Date',
			   'Market Value', 'Price', 'Overall', 'Preferred Positions']
	new_df = pd.DataFrame(columns=columns)

	for column in columns:
		if column == 'Overall':
			new_df['Overall'] = overall
		else:
			new_df[column] = df[column]

	new_df.to_csv("Input/saida_fifa.txt", sep='\t', index=False)
