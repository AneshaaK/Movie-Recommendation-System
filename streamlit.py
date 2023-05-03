import streamlit as st
import pandas as pd
import numpy as np

#from google.colab import drive
#drive.mount('/content/drive')

# File path
path = 'Data240/project/'

#input_file
n=3
movie_data = pd.read_csv('movie_titles.csv',header = None,encoding='ISO-8859-1',usecols=range(n),lineterminator='\n')
movie_data.columns = ['movie_id', 'year', 'name']
def user_input_features():
	st.title("Netflix Movie Recommendation")
	html_temp = """
	<div style="background-color:black;padding:10px">
	<h3 style="color:white;text-align:center;">Association Rules</h>
	</div>"""
	st.markdown(html_temp,unsafe_allow_html=True)
	Algorithm = st.selectbox("Algorith",["Apriori","FP_Growth","ECLAT"])
	movie_name = st.selectbox("Movie Title",movie_data['name'].unique())

	data = {'algorithm': Algorithm,
	'movie_name' : movie_name }

	return data

association_rules = pd.read_csv('ruleslift1_fp.csv',index_col=False)
input_df = user_input_features()
#print(input_df)
if st.button("submit"):
	if input_df['algorithm'] == 'FP_Growth':
		association_rules = pd.read_csv('/ruleslift1_fp.csv',index_col=False)
		df_movie = association_rules[association_rules['antecedents'].apply(lambda x: input_df['movie_name'] in x)]
		df_res = df_movie.sort_values(by=['lift'], ascending=False)
	elif input_df['algorithm'] == 'Apriori':
		association_rules = pd.read_csv('ruleslift1_ap.csv',index_col=False)
		df_movie = association_rules[association_rules['antecedents'].apply(lambda x: input_df['movie_name'] in x)]
		df_res = df_movie.sort_values(by=['lift'], ascending=False)
	else:
		association_rules = pd.read_csv('eclat_rules_005.csv',index_col=False)
		df_movie = association_rules[association_rules['antecedents'].apply(lambda x: input_df['movie_name'] in x)]
		df_res = df_movie.sort_values(by=['support'], ascending=False)

	# df_movie = association_rules[association_rules['antecedents'].apply(lambda x: input_df['movie_name'] in x)]


	# df_res = df_movie.sort_values(by=['lift'], ascending=False)
	#print(df_res.head(10))
	result = pd.DataFrame(df_movie['consequents'].unique())
	result.columns = ['Movie Recommendation']
	st.write(result.head(10))
