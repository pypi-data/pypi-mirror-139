#!/usr/bin/env python
# coding: utf-8

# In[523]:
def toopsis():
    import sys
    if(len(sys.argv) != 5):
        print("Please Enter correct number of parameters !!")
        sys.exit();
    if ".csv" not in sys.argv[1]:
        print("Kindly spcify correct file format to read dataset (.csv)!!")
        sys.exit();
    if ".csv" not in sys.argv[-1]:
        print("Kindly spcify correct file format to save (.csv)!!")
        sys.exit();

    impacts = [sys.argv[-2][0],sys.argv[-2][2],sys.argv[-2][4],sys.argv[-2][6],sys.argv[-2][8]]
    weights = [int(sys.argv[-3][0]),int(sys.argv[-3][2]),int(sys.argv[-3][4]),int(sys.argv[-3][6]),int(sys.argv[-3][8]) ]
    for i in range(0,5):
        if ( (impacts[i] != "+") and (impacts[i] != '-') ):
            print("Impacts must be either +ve or -ve")
            sys.exit()
            
    import pandas as pd
    import numpy as np

    #sys.argv[1] = "101903321-data.csv"
    reading = pd.read_csv(sys.argv[1])
    # print(reading)
    df = reading.iloc[: , 1:6]
    # df


    # In[525]:


    normalised_vector_P1 = np.sqrt( np.sum(df.iloc[:,0:1] * df.iloc[:,0:1]) )
    normalised_vector_P2 = np.sqrt( np.sum(df.iloc[:,1:2] * df.iloc[:,1:2]) )
    normalised_vector_P3 = np.sqrt( np.sum(df.iloc[:,2:3] * df.iloc[:,2:3]) )
    normalised_vector_P4 = np.sqrt( np.sum(df.iloc[:,3:4] * df.iloc[:,3:4]) )
    normalised_vector_P5 = np.sqrt( np.sum(df.iloc[:,4:5] * df.iloc[:,4:5]) )

    # print( normalised_vector_P1 )
    # print( normalised_vector_P2 )
    # print( normalised_vector_P3 )
    # print( normalised_vector_P4 )
    # print( normalised_vector_P5 )

    # df.iloc[:,0:1] * df.iloc[:,0:1]


    # In[526]:

    normalised_df_P1 = df.iloc[:,0:1].div(normalised_vector_P1)
    normalised_df_P2 = df.iloc[:,1:2].div(normalised_vector_P2)
    normalised_df_P3 = df.iloc[:,2:3].div(normalised_vector_P3)
    normalised_df_P4 = df.iloc[:,3:4].div(normalised_vector_P4)
    normalised_df_P5 = df.iloc[:,4:5].div(normalised_vector_P5)

    normalised_df = pd.concat([normalised_df_P1, normalised_df_P2, normalised_df_P3, normalised_df_P4, normalised_df_P5], axis=1)
    # normalised_df


    # In[527]:


    normalised_df["P1"] = weights[0] * normalised_df["P1"]
    normalised_df["P2"] = weights[1] * normalised_df["P2"]
    normalised_df["P3"] = weights[2] * normalised_df["P3"]
    normalised_df["P4"] = weights[3] * normalised_df["P4"]
    normalised_df["P5"] = weights[4] * normalised_df["P5"]


    # In[528]:


    # normalised_df


    # In[529]:


    max_value_P1 = normalised_df["P1"].max()
    max_value_P2 = normalised_df["P2"].max()
    max_value_P3 = normalised_df["P3"].max()
    max_value_P4 = normalised_df["P4"].max()
    max_value_P5 = normalised_df["P5"].max()
    max_value_Ps = [max_value_P1, max_value_P2, max_value_P3, max_value_P4, max_value_P5]
    #############
    min_value_P1 = normalised_df["P1"].min()
    min_value_P2 = normalised_df["P2"].min()
    min_value_P3 = normalised_df["P3"].min()
    min_value_P4 = normalised_df["P4"].min()
    min_value_P5 = normalised_df["P5"].min()
    min_value_Ps = [min_value_P1, min_value_P2, min_value_P3, min_value_P4, min_value_P5]

    # print( max_value_Ps )
    # print( min_value_Ps )


    # In[530]:


    # Finding Ideal Best and Ideal Worst
    Ideal_best  = list(range(5))
    Ideal_worst = list(range(5))

    for i in range(0,5):
        if impacts[i] == "+":
            Ideal_best[i]  = max_value_Ps[i]
            Ideal_worst[i] = min_value_Ps[i]
        elif impacts[i] == "-":
            Ideal_best[i]  = min_value_Ps[i]
            Ideal_worst[i] = max_value_Ps[i] 
            
    # print(Ideal_best)
    # print(Ideal_worst)


    # In[531]:


    #Appending a row of Ideal best and ideal worst
    normalised_df.loc[len(normalised_df)] = Ideal_best
    normalised_df.loc[len(normalised_df)] = Ideal_worst

    # display(normalised_df)


    # In[532]:


    splus_0 = np.sqrt(np.sum(pow(normalised_df.loc[0]-normalised_df.loc[8],2)))
    splus_1 = np.sqrt(np.sum(pow(normalised_df.loc[1]-normalised_df.loc[8],2)))
    splus_2 = np.sqrt(np.sum(pow(normalised_df.loc[2]-normalised_df.loc[8],2)))
    splus_3 = np.sqrt(np.sum(pow(normalised_df.loc[3]-normalised_df.loc[8],2)))
    splus_4 = np.sqrt(np.sum(pow(normalised_df.loc[4]-normalised_df.loc[8],2)))
    splus_5 = np.sqrt(np.sum(pow(normalised_df.loc[5]-normalised_df.loc[8],2)))
    splus_6 = np.sqrt(np.sum(pow(normalised_df.loc[6]-normalised_df.loc[8],2)))
    splus_7 = np.sqrt(np.sum(pow(normalised_df.loc[7]-normalised_df.loc[8],2)))
    S_plus = [splus_0, splus_1, splus_2, splus_3, splus_4, splus_5, splus_6, splus_7, 'Nan', 'Nan']

    sminus_0 = np.sqrt(np.sum(pow(normalised_df.loc[0]-normalised_df.loc[9],2)))
    sminus_1 = np.sqrt(np.sum(pow(normalised_df.loc[1]-normalised_df.loc[9],2)))
    sminus_2 = np.sqrt(np.sum(pow(normalised_df.loc[2]-normalised_df.loc[9],2)))
    sminus_3 = np.sqrt(np.sum(pow(normalised_df.loc[3]-normalised_df.loc[9],2)))
    sminus_4 = np.sqrt(np.sum(pow(normalised_df.loc[4]-normalised_df.loc[9],2)))
    sminus_5 = np.sqrt(np.sum(pow(normalised_df.loc[5]-normalised_df.loc[9],2)))
    sminus_6 = np.sqrt(np.sum(pow(normalised_df.loc[6]-normalised_df.loc[9],2)))
    sminus_7 = np.sqrt(np.sum(pow(normalised_df.loc[7]-normalised_df.loc[9],2)))
    S_minus = [sminus_0, sminus_1, sminus_2, sminus_3, sminus_4, sminus_5, sminus_6, sminus_7, 'Nan', 'Nan']

    normalised_df['S_plus'] = S_plus
    normalised_df['S_minus'] = S_minus

    # normalised_df


    # In[533]:


    normalised_df['S_plus + S_minus'] = normalised_df['S_plus'] + normalised_df['S_minus']


    # In[534]:


    # normalised_df


    # In[535]:


    x = normalised_df.iloc[0:8,0:8]
    # x

    x['Topsis Score(Pt)'] = x['S_minus'] / x['S_plus + S_minus']
    # x


    # In[536]:


    def calculate_rank(vector):
      a={}
      rank=8
      for num in sorted(vector):
        if num not in a:
          a[num]=rank
          rank=rank-1
      return[a[i] for i in vector]

    Rank = calculate_rank(x['Topsis Score(Pt)'])        
    x['Rank'] = Rank
    # x


    # In[537]:


    TOPSIS = pd.concat([reading, x['Topsis Score(Pt)'], x['Rank']], axis=1)
    print(TOPSIS)
    # sys.argv[-1]='101903321-result.csv'
    TOPSIS.to_csv(sys.argv[-1], index=False)

        
