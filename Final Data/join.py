import pandas as pd
import numpy as np

if __name__ == '__main__':

	df_pais = pd.read_table("tabela_pais.txt", sep='\t')
	df_team = pd.read_table("tabela_times.txt", sep='\t')
	df = pd.read_table("final_dataset.txt", sep='\t')

	#df = pd.merge(df_fifa, df_transfer, on=['Name', 'Market Value', 'Price'])
	df['Country A'] = ''
	df['Country B'] = ''
	df_pais['Id'] = list(map(lambda x: str(x), df_pais['Id']))
	for index, row in df.iterrows():

		for team in ['A', 'B']:
			country_id = df_team.loc[df_team['Team'] == row['Team ' + team]]['Id']
			#print(len(country_id))
			if len(country_id) > 0:
				country_id = list(set(country_id))[0]
				country_name = df_pais.loc[df_pais['Id'] == country_id]['Country']
				if len(country_name) > 0:	
					df.loc[index, 'Country ' + team] = country_name.values[0]
				else:
					df.loc[index, 'Country ' + team] = "Unknown"

	df.to_csv("final_version.txt", sep='\t', index=False)
