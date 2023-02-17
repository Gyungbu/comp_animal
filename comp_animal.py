import os
import pandas as pd
import numpy as np

input_data = {'type' : 'cat', 'sex' : 'female', 'female_status' : 'lactation', 'week' : 100, 'body_weight' : 31, 'dog_breed' : '고든세터', 'dog_group' : 'Moderate activity (1 – 3 h/day) (low impact activity)', 'cat_breed' : '노르웨이숲', 'cat_group' : 'Active cats', 'weeks_after_pregnant' : 4, 'weeks_of_lactation' : 4, 'number_of_puppies' : 4, 'number_of_kittens' : 4}

dict_week_lactation_dog = {1:0.75, 2:0.95, 3:1.1, 4:1.2}
dict_week_lactation_cat = {1:0.9, 2:0.9, 3:1.2, 4:1.2, 5:1.1, 6:1.0, 7:0.8}
  

# Get Multiplier & Expected body weight values from dog_group & dog_breed information
if input_data['type'] == 'dog':

  # df_multiplier_dog : Multiplier information corresponding to dog group
  # df_expected_body_weight_dog : Expected body weight information corresponding to dog breed
  path_db = os.path.dirname(os.path.abspath(__file__)) + "/input/DB_companian_animal.xlsx"
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
  
## Calculate the Daily Metabolizable Energy Requirements of Dogs
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
if input_data['type'] == 'cat':

  # df_multiplier_cat : Multiplier information corresponding to cat group
  # df_expected_body_weight_cat : Expected body weight information corresponding to cat breed
  path_db = os.path.dirname(os.path.abspath(__file__)) + "/input/DB_companian_animal.xlsx"
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

## Calculate the Daily Metabolizable Energy Requirements of Cats
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

print("Metabolisable Energy:",  ME, "kcal")
