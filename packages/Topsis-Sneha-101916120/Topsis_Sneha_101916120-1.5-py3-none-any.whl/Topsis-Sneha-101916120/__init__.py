import pandas as pd
import numpy as np
import sys
import os
def topsis(file,weight,impact,result):
  try:
    df=pd.read_csv(file)
  except:
    print("Error!! file name is incorrect or the file don't exist")
    sys.exit()
  df.set_index('Fund Name',inplace=True)
    
  df.shape[1] == df.select_dtypes(include=np.number).shape[1]
  if(df.shape[1]!=5):
    print("From 2nd to last columns must contain numeric values only (Handling of non-numeric values)")
    sys.exit()
  try:
    w=[float(i) for i in weight.split(',')]
    im=[str(i) for i in impact.split(',')]
  except:
    print('Input Weights or impacts are not seperated by commas')
    sys.exit()
  l=len(df.columns)
  if(l<3):
    print("Input file must contain three or more columns")
    sys.exit()
  if(len(im)!=l or len(w)!=l):
    print("Number of weights, number of impacts and number of columns (from 2nd to last columns) must be same")
    sys.exit()
  for i in range(0,len(im)):
    if(im[i]!='+' and im[i]!='-'):
      print("Impacts must be either +ve or -ve not ",im[i])
      sys.exit()
  ndf=df.copy()
  for i in range(0,l):
    sum=0
    for j in range(0,len(ndf)):
      sum=sum +ndf.iloc[j, i]**2
    sum=sum**0.5
    for j in range(len(ndf)):
      ndf.iat[j, i] = (ndf.iloc[j, i] /sum)*w[i]  
  
  ideal_b= (ndf.max().values)[0:]
  ideal_w= (ndf.min().values)[0:]
  for i in range(0,l):
    if im[i] == '-':
      tt=ideal_b[i]
      ideal_b[i] = ideal_w[i]
      ideal_w[i] =tt
  score = [] 
  pp = [] 
  nn = []
  for i in range(len(ndf)):
    temp_p, temp_n = 0, 0
    for j in range(0,l):
      temp_p = temp_p + (ideal_b[j] - ndf.iloc[i, j])**2
      temp_n = temp_n + (ideal_w[j] - ndf.iloc[i, j])**2
    temp_p, temp_n = temp_p**0.5, temp_n**0.5
    score.append(temp_n/(temp_p + temp_n))
    nn.append(temp_n)
    pp.append(temp_p)
  df['Topsis Score'] =score
  df['Rank'] = (df['Topsis Score'].rank(method='max', ascending=False))
  df= df.astype({"Rank": int})
  df.to_csv(result,index=None)