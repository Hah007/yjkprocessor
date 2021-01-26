# import pandas as pd
# import numpy as np
# import time
# import matplotlib.pyplot as plt
# df= pd.DataFrame(np.random.rand(10, 4), columns=['A','B','C','D'])
# print(df)
# print(df.dtypes)
# df.plot.line(subplots=True)
# plt.show()
# time.sleep(2)

def convert_to_float(frac_str):
    try:
        return float(frac_str)
    except ValueError:
        num, denom = frac_str.split('/')
        try:
            leading, num = num.split(' ')
            whole = float(leading)
        except ValueError:
            whole = 0
        frac = float(num) / float(denom)
        return whole - frac if whole < 0 else whole + frac

print(convert_to_float('77/44'))