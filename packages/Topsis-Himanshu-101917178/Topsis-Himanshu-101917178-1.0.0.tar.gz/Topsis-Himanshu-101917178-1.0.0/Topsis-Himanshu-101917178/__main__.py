import sys
import numpy as np
import pandas as pd
import warnings

def main(inpFile,wts,impacts):
    #if len(sys.argv) != 3:
    #raise Exception('Provide correct number of parameters')
    #sys.exit()
    #logs.error("More number of parameters are passed then expected!!!")
	#raise Exception('Provide correct number of parameters as input!!!')
    
    try:
        with open(inpFile) as f:
            print("File exists!!")
            #logs.error("File exists")
    except FileNotFoundError:
        raise Exception('Provide correct file')
        sys.exit()
        #print('File does not exist!!!')
        #logs.error("File does not exist!!!")
    except:
        raise Exception('Provide correct file')
        sys.exit()
        #print('Something went wrong!!!')
        #logs.error('Something went wrong!!!')	



    my_df = pd.read_csv(inpFile)
    #himanshu_df=df
    if len(my_df.columns) <= 3:
        raise Exception('Inappropriate no. of columns ')
        #sys.exit()
        #logs.error('Invalid no. of columns')

    no_of_col = len(my_df.columns)-1
    w = wts.split(',')
    i = impacts.split(',')
    for j in range(len(i)):
        if i[j]=="+":
            i[j]="1"
        elif i[j]=="-":
            i[j]="-1"
        else:
            raise Exception('Invalid impacts provided')
            
    w_len = len(w) 
    i_len = len(i)
    #result_file = sys.argv[4]

    my_df.iloc[:,1:].apply(lambda h:pd.to_numeric(h,errors='raise').notnull().all())
    if(w_len!=i_len or i_len!=no_of_col or no_of_col!=w_len):
        raise Exception('weight and impact and columns numbers are not equal')
    #print(no_of_col)
    #print(w)
    #print(i)
    #print(df)

    if not(all(map(str.isdigit, w))):
        print('Weights should be numeric and separated by commas')
        sys.exit()

    wts = [int(i) for i in w]
    impact = [int(j) for j in i]
    df = my_df.drop(columns="Fund Name",axis=0)

    rootSumSquares = []
    for i in df.columns:
        sum = 0
        for j in df[i]:
            sum += (j**2)
        sum = sum**0.5
        rootSumSquares.append(sum)
    #print(df)
    print(rootSumSquares)

    j=0
    for i in df.columns:
        df[i]/=rootSumSquares[j]
        j = j+1

    #wts = [1]*len(df.columns)

    j=0
    for i in df.columns:
        df[i] *= wts[j]
        j = j+1

    idlBest = []
    idlWorst = []
    #impact=[1,1,1,1,1]

    k=0
    for i in df.columns:
        if impact[k]==1:
            idlBest.append(max(df[i]))
            idlWorst.append(min(df[i]))
        else:
            idlBest.append(min(df[i]))
            idlWorst.append(max(df[i]))
            k=k+1

    #print(idlBest)
    #print(idlWorst)

    eucBest = []
    eucWorst = []

    for i in range(len(df)):
        temp1=0
        temp2=0
        for j in range(len(df.columns)):
            temp1 += (df.iloc[i,j]-idlBest[j])**2
            #print(temp1)
            temp2 += (df.iloc[i,j]-idlWorst[j])**2

        eucBest.append(temp1**0.5)
        eucWorst.append(temp2**0.5)

    #print(eucBest)
    #print(eucWorst)
    topsis_score = []
    for i in range(len(df)):
        topsis_score.append(eucWorst[i]/(eucBest[i]+eucWorst[i]))

    #topsis_score


    my_df['Topsis Score'] = topsis_score
    my_df['Rank'] = my_df['Topsis Score'].rank(ascending=False)
    print(my_df)
    #df.to_csv(result_file,index=False)

#main('101917178-data.csv',"1,1,1,2,1","+,+,+,-,+")

