def performTopsis(df,w,s):

    import numpy as np
    import pandas as pd

    with open(df, 'r') as fin:
        # df = pd.read_excel(sys.argv[1])
        if(len(df)<3):
            raise Exception("Input file must contain 3 or more columns.")

        ans = df.applymap(np.isreal).all()
        check=True
        for i in range(1,len(df.columns)):
            check = (check and ans[i])
        if(check==False):
            raise Exception("Dataframe contains non-numeric values")

        if(df.isnull().any().sum()!=0):
            raise Exception("Dataframe contains missing values")

    if(w.count(',')!=(len(df.columns)-1)-1):
        raise Exception("Commas incorrect")
    w = w.split(",")
    if((len(w)!=(len(df.columns)-1))):
        raise Exception("Weights parameters are incorrect!")
    for i in w:
        if i.isalpha():
            raise Exception("Wrong weights!")

    w = pd.to_numeric(w)

    if(s.count(',')!=(len(df.columns)-1)-1):
        raise Exception("Commas incorrect")
    s = s.split(",")
    if(len(s)!=len(df.columns)-1):
        raise Exception("Wrong impacts!")

    for i in s:
        if i not in ['+', '-']:
            raise Exception("Wrong impacts!")

    s = [1 if i=='+' else -1 for i in s]

    """Converting excel to csv file"""

    # df.to_csv('101903328-data.csv', index=False)

    """Dropping first column"""

    X = df['Fund Name']
    df.drop('Fund Name', inplace=True, axis=1)

    """input weights,impacts using command line"""

    import topsispy as tp

    a = df.values.tolist()

    t = tp.topsis(a, w, s)

    df['Topsis_Score'] = t[1]
    df['Rank'] = df['Topsis_Score'].rank(ascending=False)

    final_df = pd.DataFrame({'Fund Name':X})
    final_df = pd.concat([final_df,df],axis=1)
    # final_df.to_csv(sys.argv[4], index=False)

    return final_df

