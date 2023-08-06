import pandas as pd, numpy as np, sys

def perform_topsis():
  #exception handling
  if len(sys.argv) != 5:
    raise Exception('There must be 5 arguments. Eg, python <program.py> <InputDataFile> <Weights> <Impacts> <ResultFileName>')
  elif not sys.argv[1].endswith('.csv'):
    raise Exception('Input file extension must be .csv')

  try:
    df = pd.read_csv(sys.argv[1])
  except FileNotFoundError:
    print('File does not exist')
    sys.exit(1)


  weights = str(sys.argv[2])
  impacts = str(sys.argv[3])
  if not sys.argv[4].endswith('.csv'):
    raise Exception('Result file name extension must be .csv')
  result_file = sys.argv[4]

  #checking if number of columns >= 3
  if len(df.columns) < 3:
    raise Exception('Input file must contain three or more columns.')

  #weights
  count = 1
  n = len(df.iloc[:, 1:].columns)
  w = []
  x = ''
  for i in weights:
    if i != ',':
      x += i
    else:
      count += 1
      try:
        x = float(x)
        w.append(x)
      except:
        raise Exception('Invalid format of weights')
      x = ''
  #for last weight
  try:
      x = float(x)
      w.append(x)
  except:
      raise Exception('Invalid format of weights')
  if count != n:
    raise Exception('Number of weights and columns must be same')


  #impacts
  count = 0
  num = 0
  for i in impacts:
    if num%2 == 0:
      if i not in ['+', '-']:
        raise Exception('Impacts must only contain + and - seperated by commas')
      else:
        count += 1
    elif num%2 != 0 and i != ',':
      raise Exception('Impacts must be seperated by commas')
    num += 1
  if count != n:
    raise Exception('Number of impacts and columns must be same')
  impacts = impacts.replace(',', '')

  #making a copy
  old_df = df.copy(deep = True)

  #Handling of non-numeric values (replacing non-numeric values with 0)
  for i in df.iloc[:, 1:].columns:
    df[i] = pd.to_numeric(df[i], errors = 'coerce')
  df = df.fillna(0)


  #normalization
  sqr = np.zeros(n)
  for i in range(len(df)):
    sqr = np.add(sqr, np.power(df.iloc[i, 1:], 2))
  sqr = np.power(sqr, 0.5)
  for i in range(len(df)):
    df.iloc[i, 1:] = df.iloc[i, 1:]/sqr * w

  #finding best and worst value in each column
  best = []
  worst = []
  for i in range(len(impacts)):
    if impacts[i] == '+':
      best.append(max(df.iloc[:, i + 1]))
      worst.append(min(df.iloc[:, i + 1]))
    else:
      best.append(min(df.iloc[:, i + 1]))
      worst.append(max(df.iloc[:, i + 1]))

  #eucledian distance
  d_best = []
  d_worst = []
  for i in range(len(df)):
    d_best.append(np.linalg.norm(df.iloc[i, 1:] - best))
    d_worst.append(np.linalg.norm(df.iloc[i, 1:] - worst))

  #scores
  score = []
  for i in range(len(d_best)):
    score.append(round(d_worst[i]/(d_best[i] + d_worst[i]), 2))


  old_df['TOPSIS score'] = score

  #rank
  old_df['Rank'] = old_df['TOPSIS score'].rank(ascending = False, method ='dense')
  old_df['Rank'] = pd.to_numeric(old_df['Rank'], downcast ='signed')

  #output
  old_df.to_csv(result_file, index = False)