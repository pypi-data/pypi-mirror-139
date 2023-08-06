
----------------------------------------------------------------------
Hello!! I made this package in order to make the process of generating the topsis score for a dataset, a child's play. With just one function, you will have the dataset with the topsis score and rank column.

The function 'build_topsis()' will return the final dataset with topsis score and corresponding rank column.
This function takes three arguments: 
	
	data: the original dataset upon which you want to calculate topsis score,
	weights: a list that contains the pre-determined weights for all the numeric columns (int/float),
	imapcts: a list that conatins the pre-determined impacts for all the numeric columns ('+'/'-')

This function will return the original dataset passed in it but with the additional columns of Topsis Score and Rank.

Have fun.
----------------------------------------------------------------------	