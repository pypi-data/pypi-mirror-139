import numpy as np
import pandas as pd
import topsispy as tp

def top_score(data,weights,criterias):
    
    df=pd.read_csv("data.csv")

    df1=df.drop(["Fund Name"],axis=1)
    d=df1.to_numpy()

    t = tp.topsis(d,weights,criterias)
    l=t[1]

    ll=pd.DataFrame(l)
    ll = ll.rename({0: 'Topsis Score'}, axis=1)  # new method

    rankk=ll.rank(ascending=False)
    rankk.rename({'Topsis Score': 'Rank'}, axis=1,inplace=True) 

    df=pd.concat([df, ll,rankk], axis=1)

    df.to_csv( "101917118-result.csv",index=False)



