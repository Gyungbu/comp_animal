import os
import pandas as pd
import numpy as np
import openpyxl
import scipy

# Functions

def isNumber(s):
  try:
    float(s)
    return True
  except ValueError:
    return False

# Input data - Personal Information of the Companion Animal

input_data = {'type' : 'bird', 'sex' : 'female', 'female_status' : 'lactation', 'week' : 100, 'body_weight' : 31, 
              'dog_breed' : '고든세터', 'dog_group' : 'Moderate activity (1 – 3 h/day) (low impact activity)', 
              'cat_breed' : '노르웨이숲', 'cat_group' : 'Active cats', 'weeks_after_pregnant' : 4, 
              'weeks_of_lactation' : 4, 'number_of_puppies' : 4, 'number_of_kittens' : 4}

dict_week_lactation_dog = {1:0.75, 2:0.95, 3:1.1, 4:1.2}
dict_week_lactation_cat = {1:0.9, 2:0.9, 3:1.2, 4:1.2, 5:1.1, 6:1.0, 7:0.8}

# Check the input data - dog, cat
while True:
    if input_data['type'] not in ['dog', 'cat']:
        input_data['type'] = input('Enter animal type: ')
        print('Animal type must be either "dog" or "cat"')
        
        continue
    
    # If we get here, the animal type is valid, so we can exit the loop
    print("\n<input_data>\n")
    print(input_data)
    break
    
# Get Multiplier & Expected body weight values from dog_group & dog_breed information
if input_data['type'] == 'dog':

  # df_multiplier_dog : Multiplier information corresponding to dog group
  # df_expected_body_weight_dog : Expected body weight information corresponding to dog breed
  path_db = os.path.abspath('') + "/input/DB_companion_animal.xlsx"
  df_multiplier_dog = pd.read_excel(path_db, sheet_name = "multiplier_dog")
  df_expected_body_weight_dog = pd.read_excel(path_db, sheet_name = "expected_body_weight_dog")
  
  try:
    condition = (df_multiplier_dog.dog_group == input_data['dog_group']) 
    multiplier_dog = df_multiplier_dog[condition]['multiplier'].values[0]
    
    condition = (df_expected_body_weight_dog.dog_breed == input_data['dog_breed']) 
    if input_data['sex'] == 'male':
      expected_body_weight_dog = df_expected_body_weight_dog[condition]['expected_body_weight_male'].values[0]
      
    else:
      expected_body_weight_dog = df_expected_body_weight_dog[condition]['expected_body_weight_female'].values[0]
    
  except:
    print("Please check the name of the dog group or dog breed!")
  
## Calculate the Daily Metabolisable Energy Requirements of Dogs
  try:
    # Puppies after weaning
    if input_data['week'] < 8:
      BW = input_data['body_weight']
      ME = 250 * BW
          
    elif input_data['week'] <= 52:
      p = input_data['body_weight'] / expected_body_weight_dog
      BW = input_data['body_weight']
      ME = (254.1-135.0 * p) * (BW**0.75)
      
    elif input_data['sex'] == 'female':
      
      # Bitches in gestation
      if input_data['female_status'] == 'gestation':
        if input_data['weeks_after_pregnant'] > 4:
          BW = input_data['body_weight']
          ME = 132 * BW**0.75 + 26 * BW
          
        elif input_data['weeks_after_pregnant'] <= 4:
          BW = input_data['body_weight']
          ME = 132 * BW**0.75 
          
        else: 
          print("Check the weeks_after_pregnant value")
      
      # Bitches in lactation    
      elif input_data['female_status'] == 'lactation':
        if input_data['number_of_puppies'] <= 4:
          BW = input_data['body_weight']
          L = dict_week_lactation_dog[input_data['weeks_of_lactation']]
          n = input_data['number_of_puppies']
          ME = 145 * BW**0.75 + 24 * n * BW * L
          
        elif input_data['number_of_puppies'] <= 8:
          BW = input_data['body_weight']
          L = dict_week_lactation_dog[input_data['weeks_of_lactation']]
          n = input_data['number_of_puppies']
          ME = 145 * BW**0.75 + (96+ 12 * (n-4)) * BW * L
          
        elif input_data['number_of_puppies'] > 8:
          BW = input_data['body_weight']
          L = dict_week_lactation_dog[input_data['weeks_of_lactation']]
          n = input_data['number_of_puppies']
          ME = 145 * BW**0.75 + 144 * BW * L
        
        else: 
          print("Please check the number_of_puppies value!")
      
      # Bitches not in gestation nor lactation    
      else:
        BW = input_data['body_weight']
        ME = multiplier_dog * BW**0.75     
    
    # Males    
    elif input_data['sex'] == 'male':
      BW = input_data['body_weight']
      ME = multiplier_dog * BW**0.75  
    
    # Neutered    
    elif input_data['sex'] == 'neutered':
      BW = input_data['body_weight']
      ME = 112 * BW**0.75  
          
    # Exceptional case  
    else:
      print("Please check the sex value!")
      
  # Exceptional case    
  except:
    print("Please check the input values (ex, week, sex, female_status, number_of_puppies etc.)!")


# Get Multiplier & Expected body weight values from cat_group & cat_breed information
elif input_data['type'] == 'cat':

  # df_multiplier_cat : Multiplier information corresponding to cat group
  # df_expected_body_weight_cat : Expected body weight information corresponding to cat breed
  path_db = os.path.abspath('') + "/input/DB_companion_animal.xlsx"
  df_multiplier_cat = pd.read_excel(path_db, sheet_name = "multiplier_cat")
  df_expected_body_weight_cat = pd.read_excel(path_db, sheet_name = "expected_body_weight_cat")
  
  try:
    condition = (df_multiplier_cat.cat_group == input_data['cat_group']) 
    multiplier_cat = df_multiplier_cat[condition]['multiplier'].values[0]
    
    condition = (df_expected_body_weight_cat.cat_breed == input_data['cat_breed']) 
    if input_data['sex'] == 'male':
      expected_body_weight_cat = df_expected_body_weight_cat[condition]['expected_body_weight_male'].values[0]
      
    else:
      expected_body_weight_cat = df_expected_body_weight_cat[condition]['expected_body_weight_female'].values[0]
    
  except:
    print("Please check the name of the cat group or cat breed!")

## Calculate the Daily Metabolisable Energy Requirements of Cats
  try:
    # Kittens after weaning
    if input_data['week'] <= 52:
      p = input_data['body_weight'] / input_data['expected_mature_body_weight']
      BW = input_data['body_weight']
      ME = 100 * BW**0.67 * 6.7 * (np.exp(-0.189*p)-0.66)

    elif input_data['sex'] == 'female':
      
      # Queens in gestation
      if input_data['female_status'] == 'gestation':
        BW = input_data['body_weight']
        ME = 140 * BW**0.67 

      # Queens in lactation    
      elif input_data['female_status'] == 'lactation':
        if input_data['number_of_kittens'] < 3:
          BW = input_data['body_weight']
          L = dict_week_lactation_cat[input_data['weeks_of_lactation']]
          ME = 100 * BW**0.67 + 18 * BW * L
          
        elif input_data['number_of_kittens'] <= 4:
          BW = input_data['body_weight']
          L = dict_week_lactation_cat[input_data['weeks_of_lactation']]
          ME = 100 * BW**0.67 + 60 * BW * L
          
        elif input_data['number_of_kittens'] > 4:
          BW = input_data['body_weight']
          L = dict_week_lactation_cat[input_data['weeks_of_lactation']]
          ME = 100 * BW**0.67 + 70 * BW * L
        
        else: 
          print("Please check the number_of_kittens value!")          

      # Queens not in gestation nor lactation    
      else:
        BW = input_data['body_weight']
        ME = multiplier_cat * BW**0.67     
    
    # Males    
    elif input_data['sex'] == 'male':
      BW = input_data['body_weight']
      ME = multiplier_cat * BW**0.67  
    
    # Neutered    
    elif input_data['sex'] == 'neutered':
      BW = input_data['body_weight']
      ME = 75 * BW**0.67  
          
    # Exceptional case  
    else:
      print("Please check the sex value!")
      
  # Exceptional case    
  except:
    print("Please check the input values (ex, week, sex, female_status, number_of_kittens etc.)!")      

print("\n<1.Result of the Metabolisable Energy>\n")
print("Metabolisable Energy:",  ME, "kcal")
print("건물섭취량:",  ME/4, "g")

## Calculate the Recommended nutrients for Dogs 

if input_data['type'] == 'dog':
  # df_recom_nutrient_dog : Recommended nutrient levels per 1000kcal of ME for dog
  path_db = os.path.abspath('') + "/input/DB_companion_animal.xlsx"
  df_recom_nutrient_dog = pd.read_excel(path_db, sheet_name = "recom_nutrient_dog")    
  
  df_recom_nutrient_dog['min_nutrient'] = '-'
   
  for idx, row in df_recom_nutrient_dog.iterrows():
    if input_data['week'] < 14:
      if row['early_growth'] != '-':
        df_recom_nutrient_dog.loc[idx, 'min_nutrient'] = float(row['early_growth']) * ME / 1000  
      else:
        df_recom_nutrient_dog.loc[idx, 'min_nutrient'] = '-'

    elif input_data['week'] <= 52:
      if row['late_growth'] != '-':
        df_recom_nutrient_dog.loc[idx, 'min_nutrient'] = float(row['late_growth']) * ME / 1000  
      else:
        df_recom_nutrient_dog.loc[idx, 'min_nutrient'] = '-'

    elif input_data['sex'] == 'female':
      if (input_data['female_status'] == 'gestation') | (input_data['female_status'] == 'lactation'):
        if row['reproduction'] != '-':
          df_recom_nutrient_dog.loc[idx, 'min_nutrient'] = float(row['reproduction']) * ME / 1000  
        else:
          df_recom_nutrient_dog.loc[idx, 'min_nutrient'] = '-'
        
    else:
      if row['adult'] != '-':
        df_recom_nutrient_dog.loc[idx, 'min_nutrient'] = float(row['adult']) * ME / 1000  
      else:
        df_recom_nutrient_dog.loc[idx, 'min_nutrient'] = '-'
  
  df_recom_nutrient_dog = df_recom_nutrient_dog[['nutrient','unit', 'min_nutrient']]
  df_recom_nutrient_output =  df_recom_nutrient_dog
  df_recom_nutrient_output.loc[-1] = ['Metabolisable Energy', 'kcal', ME]
  print("\n<2.Result of the Recommended Nutrients>\n")
  print(df_recom_nutrient_output)

## Calculate the Recommended nutrients for Cats 

elif input_data['type'] == 'cat':
  # df_recom_nutrient_cat : Recommended nutrient levels per 1000kcal of ME for cat
  path_db = os.path.abspath('') + "/input/DB_companion_animal.xlsx"
  df_recom_nutrient_cat = pd.read_excel(path_db, sheet_name = "recom_nutrient_cat")    
  
  df_recom_nutrient_cat['min_nutrient'] = '-'
   
  for idx, row in df_recom_nutrient_cat.iterrows():
    if input_data['week'] <= 52:
      if row['growth'] != '-':
        df_recom_nutrient_cat.loc[idx, 'min_nutrient'] = float(row['growth']) * ME / 1000  
      else:
        df_recom_nutrient_cat.loc[idx, 'min_nutrient'] = '-'

    elif input_data['sex'] == 'female':
      if (input_data['female_status'] == 'gestation') | (input_data['female_status'] == 'lactation'):
        if row['reproduction'] != '-':
          df_recom_nutrient_cat.loc[idx, 'min_nutrient'] = float(row['reproduction']) * ME / 1000  
        else:
          df_recom_nutrient_cat.loc[idx, 'min_nutrient'] = '-'
        
    else:
      if row['adult'] != '-':
        df_recom_nutrient_cat.loc[idx, 'min_nutrient'] = float(row['adult']) * ME / 1000  
      else:
        df_recom_nutrient_cat.loc[idx, 'min_nutrient'] = '-'

  df_recom_nutrient_cat = df_recom_nutrient_cat[['nutrient','unit', 'min_nutrient']]
  df_recom_nutrient_output =  df_recom_nutrient_cat 
  df_recom_nutrient_output.loc[-1] = ['Metabolisable Energy', 'kcal', ME]
  print("\n<2.Result of the Recommended Nutrients>\n")
  print(df_recom_nutrient_output)

### Calculate the pet feeding ratios by using the Linear Programming Method

# df_raw_material : Raw material - Nutrient information
path_db_raw_material = os.path.abspath('') + "/input/DB_raw_materials.xlsx"
sheet = openpyxl.load_workbook(path_db_raw_material).sheetnames

df_raw_material = pd.DataFrame([])
for i in sheet:
    df = pd.read_excel(path_db_raw_material, sheet_name=i)
    df_raw_material = pd.concat([df_raw_material, df])

# Calculate the Gross Energy of the Raw materials (Missing value to Zero)

dict_GE = {'단백질\n(%)':5.7,'지방\n(%)':9.4, '탄수화물\n(%)':4.1, '조섬유\n(%)':4.1}

df_raw_material['gross_energy\n(kcal)'] = 0
df_raw_material = df_raw_material.replace(np.nan, 0)

for idx, row in df_raw_material.iterrows():
    for str_nutrient in dict_GE:
        if isNumber(row[str_nutrient]):
            df_raw_material.loc[idx, 'gross_energy\n(kcal)'] += 0.01 * row[str_nutrient] * dict_GE[str_nutrient] * 1000

# li_recom_nut_kor : List of the Recommended nutrients in Korean form  
# li_recom_nut_eng : List of the Recommended nutrients in English form  

li_recom_nut_kor = ['단백질\n(%)', '트립토판\n(%)', '칼슘\n(%)', '인\n(%)', '지방\n(%)',
                    '리놀레산\n(%)','나트륨\n(%)','칼륨\n(%)','마그네슘\n(%)',
                    'gross_energy\n(kcal)']

np_coeff = df_raw_material[li_recom_nut_kor].transpose().values

np_coeff[:-1,:] /= 100
np_coeff *= -1
A_ub = np_coeff.tolist()

li_recom_nut_eng = ['Protein', 'Tryptophan', 'Calcium', 'Phosphorus', 'Fat', 
                    'Linoleic acid (ω-6)', 'Sodium', 'Potassium', 'Magnesium',
                    'Metabolisable Energy']

# Unit Conversion of the Required nutrient requirements 

b_ub = []

for nutrient in li_recom_nut_eng:
    condition = (df_recom_nutrient_output.nutrient == nutrient)
    min_nutrient = df_recom_nutrient_output[condition]['min_nutrient'].values[0]    
    unit = df_recom_nutrient_output[condition]['unit'].values[0]    

    if unit == 'g':
        b_ub.append(min_nutrient*-0.001)  
        
    elif unit == 'mg':
        b_ub.append(min_nutrient*-0.000001)  
        
    elif unit == 'µg':
        b_ub.append(min_nutrient*-0.000000001)  
        
    else:
        b_ub.append(min_nutrient*-1)

# Optimization - Price of the raw materials        
c = df_raw_material['원료가격\n(원/kg)'].values.tolist()

# Constraint - Sum of the combined ratio is equal to 100
A_eq = np.ones((1,np_coeff.shape[1])).tolist()
b_eq = [100]

# Non-Negativity Constraints
bounds = [(0, None)]*np_coeff.shape[1]

# Linear Programming
result = scipy.optimize.linprog(c=c, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq, bounds=bounds)

# Show the result of the pet feeding ratios

print("\n<3.Result of the Pet Feeding Ratio[%]>\n")

if result.success:
    for idx in range(len(result.x)):
        if result.x[idx] != 0:
            print(df_raw_material.iloc[idx]['원료'], result.x[idx] )

else:
    print("No solution")



