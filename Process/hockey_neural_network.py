### Hockey_Neural_Network.py
### Neural Network for Predictin Hockey

### TRAINING
### 1) Lines for every game 
	### Make a .csv with gameid, player, player, player, etc.

### 2) Stats for each player in that game


### 3) Result of the game
import pandas as pd
import tensorflow as tf
#import tensorflow.keras.Sequential
#import sklearn.model_selection.train_test_split
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split

def main():
	training_epochs=1000 # Number of iterations for training
	n_neurons_in_h1=8 # Number of hidden neurons
	learning_rate= 0.01 # Number between 0-1

	print('Opening Dataframe')
	df=pd.read_csv('~/Desktop/NHL_predictor_results.csv')

#	print(df)
	df=clean_df(df) ### Gets rid of irrelevant data in the df and determines whether home or away team won
	print(list(df))
	print(df)

### For Hidden Layer
	print("Beginning Calculations")


	X = df.iloc[:, 2:10]
	print(X)
	y = df.iloc[:, 12]
	print(y)

# Create training and test data
	# train_size determines what prportian will be for training
	X_train, X_test, y_train, y_test = train_test_split(X, y, train_size=0.75)


	clf = MLPClassifier(solver='lbfgs', alpha=1e-5, hidden_layer_sizes=(8,),
		random_state=1, activation='logistic') # hidden_layer_sizes (neurons_per_hidden_layer, #of_hidden_layers)
	clf.fit(X_train,y_train)

	total_number_correct=0
	print(type(X_test))
	print(type(y_test))

	print(clf.score(X_test,y_test))

#	predicted_answers=clf.predict(X_test)
#	for index in range(len(y_test)):
#		expected_answer=predicted_answers[index]
#		correct_answer=y_test.iloc[index]
#
#	
#		if expected_answer==correct_answer:
#			total_number_correct += 1
#			print('correct: ' + str(expected_answer) +',' + str(correct_answer))
#		else:
#			print('wrong:' + str(expected_answer) +',' + str(correct_answer))

#	print(str(total_number_correct) + '/' + str(len(X_test)))



#	print(clf.predict([[2.099,1.79,2.385,2.55,3.123,2.223,2.88,3.536]]))
#	print(clf.predict([[2.379,1.879,2.127,2.321,2.991,1.851, 2.584,3.048]]))
#	print(clf.predict([[1.821,2.164,2.311,1.824,2.453,2.908,2.892,2.696]]))
#	print([coef.shape for coef in clf.coefs_])






def clean_df(df):
	print('Cleaning Dataframe')
	df.drop('Result.1',axis=1, inplace=True)
	df=df.loc[:, ~df.columns.str.contains('^Unnamed')]
	df=df.loc[:, ~df.columns.str.contains('^Predict')]
	df=df.loc[:, ~df.columns.str.contains('^Difference')]
	df.dropna(subset=['Result'], inplace=True)
#	df.dropna(axis=0, how='all', inplace=True) #drops all empty rows
#	df.dropna(axis=1, how='all', inplace=True) #drops all empty columns
	df.drop('Game',axis=1, inplace=True)
	df.drop('Date',axis=1, inplace=True)
	df.drop('Sports Interaction Bets',axis=1, inplace=True)
#	df.drop('Result.1',axis=1, inplace=True)
	df.drop('Day Profit',axis=1, inplace=True)
	df.drop('MoneyPuck Odds',axis=1, inplace=True)
	df['H_team_5on5_xGF'].dropna(axis=0, inplace=True)
	print(df['Result'])
	df['winner']=df['Result'].apply(lambda x: str(x).split(' ')[-1])
	df['home_team_win']=(df['Home']==df['winner'])
	df.home_team_win=df.home_team_win.astype(int)
	print(df.iloc[12])
	return df

main()