# Lightning Fast Topsis Score Generator ⚡
### By Vyom Chopra
&nbsp;
##### "Topsis-Vyom-101917060":
###### A package that comes real handy when calculating topsis score. It's one stop destination for all Topsis related work.  
&nbsp;
*"Using this topsis package, calculating topsis score is nothing more than a child's play."*

The function 'build_topsis()' in this package, will return the final dataset with topsis score and corresponding rank column.
This function takes three arguments:
	
* **data**: the original dataset upon which you want to calculate topsis score,
* **weights**: a list that contains the pre-determined weights for all the numeric columns (int/float),
* **impacts**: a list that contains the pre-determined impacts for all the numeric columns ('+'/'-')  
 
To add such an amazing capability to your python workspace, simply type in the following command in the command prompt.

```sh
pip install Topsis-Vyom-101917060
```  
This will install the topsis package in your workspace.

##### The build_topsis() have inbuilt functionality:
* to detect numeric columns and automatically calculate topsis score only off them.
* to check contents of both weights and impacts list for any discrepancy.
* to handle any exception raised.

Now, when you write your python code, simply add this amazing functionality into your code with just a tad bit of new line of code
```sh
import Topsis_Vyom_101917060
```
## Sample Code
Let's see a sample case:
Given below is a dataset of which, we need to find the topsis score and hence, corresponding rank.

|Fund Name|P1  |P2  |P3 |P4  |P5   |
|---------|----|----|---|----|-----|
|M1       |0.93|0.86|4.1|46.1|13   |
|M2       |0.67|0.45|6.1|44  |12.81|
|M3       |0.72|0.52|3.8|32.7|9.44 |
|M4       |0.73|0.53|4.1|45  |12.59|
|M5       |0.71|0.5 |3.4|55.5|15.03|
|M6       |0.74|0.55|7  |63.3|17.9 |
|M7       |0.95|0.9 |5.1|41.8|12.19|
|M8       |0.63|0.4 |7  |63.5|17.88|

```sh
weights = [1,1,1,1,1]
impacts = ['+','-','+','-','+']
``` 

In the code editor:
```sh
import pandas as pd
import Topsis_Vyom_101917060

data = pd.read_csv(input_data_path)
dataset = build_topsis(data,,weights,impacts)
print(dataset)
```  

Hence, we get the final Output as:
|Fund Name|P1  |P2  |P3 |P4  |P5   |Topsis Score|Rank|
|---------|----|----|---|----|-----|------------|----|
|M1       |0.93|0.86|4.1|46.1|13   |0.368067725 |8   |
|M2       |0.67|0.45|6.1|44  |12.81|0.629815594 |1   |
|M3       |0.72|0.52|3.8|32.7|9.44 |0.488377092 |5   |
|M4       |0.73|0.53|4.1|45  |12.59|0.489923292 |4   |
|M5       |0.71|0.5 |3.4|55.5|15.03|0.461216998 |6   |
|M6       |0.74|0.55|7  |63.3|17.9 |0.603048108 |3   |
|M7       |0.95|0.9 |5.1|41.8|12.19|0.416449713 |7   |
|M8       |0.63|0.4 |7  |63.5|17.88|0.621465197 |2   |

**Isn't it amazing!!**
## License

MIT