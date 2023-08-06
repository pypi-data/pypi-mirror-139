import topsispy as tp
import pandas as pd

def top_score(arr,weights,impacts):
  score = tp.topsis(arr,weights,impacts)
  z = score[1]
  df = pd.DataFrame(arr)
  df['Topsis Score'] = z
  df['Rank'] = df["Topsis Score"].rank(ascending=False)
  print(score[0],'is the required model that best satisfies all your requirements \n')
  return df


