import pandas as pd
test_dict = {'id':[1,2,3,4,5,6],'name':['Alice','Bob','Cindy','Eric','Helen','Grace '],'math':[90,89,99,78,97,93],'english':[89,94,80,94,94,90]}
test_dict_df = pd.DataFrame(test_dict)
print(test_dict_df)
