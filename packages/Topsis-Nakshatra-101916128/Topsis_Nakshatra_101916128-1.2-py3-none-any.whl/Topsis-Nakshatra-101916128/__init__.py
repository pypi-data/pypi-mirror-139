import os
import pandas as pd
def topsis(inp,whts,impcts,res):
    if (os.path.splitext(inp))[1]!=".csv" :
      print(f"Error : Invalid file type")
      exit(1)
    elif ((os.path.splitext(res))[1])!=".csv":
        print("Error : Output file must be .csv")
        exit(1)
    elif not os.path.isfile(inp):
        print(f"Error : {inp} No such file exist")
        exit(1)

    else:
        df,normalized_df,result_df = pd.read_csv(inp), pd.read_csv(inp),pd.read_csv(inp)
        ipcol = len(df.columns.values)
        if ipcol < 3:
            print("Error : Input file must contain three or more columns.")
            exit(1)

        try:
            wts = [float(i) for i in whts.split(',')]
        except:
            print("Error : Something wrong with weights.Impacts and weights must be separated by ‘,’")
            exit(1)

        impact = impcts.split(',')
        for i in impact:
            if not (i == '-' or i == '+'):
                print("Error : Something wrong with impacts. Impacts must be either +ve or -ve.Impacts and weights must be separated by ‘,’")
                exit(1)

        if ipcol!= len(impact)+1 or ipcol != len(wts)+1 :
            print("Error : Number of weights,impacts and columns must be equal")
            exit(1)
        
        for i in range(1, ipcol):
            pd.to_numeric(df.iloc[:, i], errors='coerce')
            df.iloc[:, i].fillna((df.iloc[:, i].mean()), inplace=True)
        #Weighted Normalized Decision Matrix creation
    number_of_columns = len(df.columns.values)
    for i in range(1, number_of_columns):
        tmp = 0
        for j in range(len(df)):
            tmp = tmp + df.iloc[j, i]**2
        tmp = tmp**0.5
        for j in range(len(normalized_df)):
            normalized_df.iat[j, i] = (df.iloc[j, i] / tmp)*wts[i-1]
    # calculating ideal best and ideal worst values
    idl_best = (normalized_df.max().values)[1:]
    idl_worst = (normalized_df.min().values)[1:]
    for i in range(1, number_of_columns):
        if impact[i-1] == '-':
            idl_best[i-1], idl_worst[i-1] = idl_worst[i-1], idl_best[i-1]
        #calculate topsis score
    topsis_score = []
    for i in range(len(normalized_df)):
        pos_temp, neg_temp = 0, 0
        for j in range(1, number_of_columns):
            pos_temp = pos_temp + (idl_best [j-1] - normalized_df.iloc[i, j])**2
            neg_temp = neg_temp + (idl_worst[j-1] - normalized_df.iloc[i, j])**2
        pos_temp, neg_temp = pos_temp**0.5, neg_temp**0.5
        topsis_score.append(neg_temp/(pos_temp + neg_temp))
    result_df['Topsis Score'] = topsis_score
    #calculate rank
    result_df['Rank'] = (result_df['Topsis Score'].rank(method='max', ascending=False))
    result_df = result_df.astype({"Rank": int})
    result_df.to_csv(res, index=False)
    return result_df