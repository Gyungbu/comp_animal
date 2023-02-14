import os
import pandas as pd
import numpy as np

input_data = {'type' : 'cat', 'sex' : 'female', 'female_status' : 'lactation', 'age' : 10, 'body_weight' : 25, 'expected_mature_body_weight' : 50, 'dog_group' : 'young_active', 'cat_group' : 'domestic_lean', 'weeks_after_pregnant' : 4, 'weeks_of_lactation' : 4, 'number_of_puppies' : 4}

dict_week_lactation_dog = {1:0.75, 2:0.95, 3:1.1, 4:1.2}
dict_week_lactation_cat = {1:0.9, 2:0.9, 3:1.2, 4:1.2, 5:1.1, 6:1.0, 7:0.8}
  

# Get Multiplier value from dog_group information
if input_data['type'] == 'dog':

  # df_multiplier_dog : Multiplier information corresponding to dog group
  path_multiplier_dog = os.path.dirname(os.path.abspath(__file__)) + "/input/multiplier_dog.xlsx"
  df_multiplier_dog = pd.read_excel(path_multiplier_dog)
  
  try:
    condition = (df_multiplier_dog.dog_group == input_data['dog_group']) 
    multiplier_dog = df_multiplier_dog[condition]['multiplier'].values[0]
    
  except:
    print("Please check the name of the dog group!")
  
## Calculate the Daily Metabolizable Energy Requirements of Dogs
  try:
    # Puppies after weaning
    if input_data['age'] <= 1:
      p = input_data['body_weight'] / input_data['expected_mature_body_weight']
      BW = input_data['body_weight']
      ME = multiplier_dog * BW**0.75 * 3.2 * (np.exp(-0.87*p)-0.1)
      
    elif input_data['sex'] == 'female':
      
      # Bitches in gestation
      if input_data['female_status'] == 'gestation':
        if input_data['weeks_after_pregnant'] > 4:
          BW = input_data['body_weight']
          ME = multiplier_dog * BW**0.75 + 26 * BW
          
        elif input_data['weeks_after_pregnant'] <= 4:
          BW = input_data['body_weight']
          ME = multiplier_dog * BW**0.75 
          
        else: 
          print("Check the weeks_after_pregnant value")
      
      # Bitches in lactation    
      elif input_data['female_status'] == 'lactation':
        if input_data['number_of_puppies'] <= 4:
          BW = input_data['body_weight']
          L = dict_week_lactation_dog[input_data['weeks_of_lactation']]
          n = input_data['number_of_puppies']
          ME = multiplier_dog * BW**0.75 + 24 * n * BW * L
          
        elif input_data['number_of_puppies'] <= 8:
          BW = input_data['body_weight']
          L = dict_week_lactation_dog[input_data['weeks_of_lactation']]
          n = input_data['number_of_puppies']
          ME = multiplier_dog * BW**0.75 + (96+ 12 * n) * BW * L
          
        elif input_data['number_of_puppies'] > 8:
          BW = input_data['body_weight']
          L = dict_week_lactation_dog[input_data['weeks_of_lactation']]
          n = input_data['number_of_puppies']
          ME = multiplier_dog * BW**0.75 + 192 * BW * L
        
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
    print("Please check the input values (ex, age, sex, female_status, number_of_puppies etc.)!")


# Get Multiplier value from cat_group information
elif input_data['type'] == 'cat':
  
  # df_multiplier_cat : Multiplier information corresponding to cat group
  path_multiplier_cat = os.path.dirname(os.path.abspath(__file__)) + "/input/multiplier_cat.xlsx"
  df_multiplier_cat = pd.read_excel(path_multiplier_cat)  

  try:
    condition = (df_multiplier_cat.cat_group == input_data['cat_group']) 
    multiplier_cat = df_multiplier_cat[condition]['multiplier'].values[0]
    
  except:
    print("Please check the name of the cat group!")

## Calculate the Daily Metabolizable Energy Requirements of Cats
  try:
    # Kittens after weaning
    if input_data['age'] <= 1:
      p = input_data['body_weight'] / input_data['expected_mature_body_weight']
      BW = input_data['body_weight']
      ME = multiplier_cat * BW**0.67 * 6.7 * (np.exp(-0.189*p)-0.66)

    elif input_data['sex'] == 'female':
      
      # Queens in gestation
      if input_data['female_status'] == 'gestation':
        BW = input_data['body_weight']
        ME = multiplier_cat * BW**0.67 

      # Queens in lactation    
      elif input_data['female_status'] == 'lactation':
        if input_data['number_of_puppies'] < 3:
          BW = input_data['body_weight']
          L = dict_week_lactation_cat[input_data['weeks_of_lactation']]
          ME = multiplier_cat * BW**0.67 + 18 * BW * L
          
        elif input_data['number_of_puppies'] <= 4:
          BW = input_data['body_weight']
          L = dict_week_lactation_cat[input_data['weeks_of_lactation']]
          ME = multiplier_cat * BW**0.67 + 60 * BW * L
          
        elif input_data['number_of_puppies'] > 4:
          BW = input_data['body_weight']
          L = dict_week_lactation_cat[input_data['weeks_of_lactation']]
          ME = multiplier_cat * BW**0.67 + 70 * BW * L
        
        else: 
          print("Please check the number_of_puppies value!")          

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
      ME = 84 * BW**0.67  
          
    # Exceptional case  
    else:
      print("Please check the sex value!")
      
  # Exceptional case    
  except:
    print("Please check the input values (ex, age, sex, female_status, number_of_puppies etc.)!")      

