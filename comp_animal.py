import os
import pandas as pd
import numpy as np
import openpyxl
import scipy
import sys
import re

# Functions

def isNumber(s):
    try:
        float(s)
        return True
    except ValueError:
        return False

def is_non_negative(x):
    if isinstance(x, (int, float)):
        return x >= 0
    else:
        return False
    
def is_valid_input_data(input_data):
    """
    Checks if the input data is valid.
    
    Args:
    input_data: dict, the input data to be validated
    
    Returns:
    bool, True if the input data is valid, False otherwise
    """
    valid_animal_types = ['dog', 'cat']
    valid_sex_types = ['female', 'male']
    valid_female_status = ['lactation', 'gestation', 'none']    
    li_non_negative = ['week', 'body_weight', 'weeks_after_pregnant', 
                   'weeks_of_lactation', 'number_of_puppies', 'number_of_kittens']
    
    if input_data['type'] not in valid_animal_types:
        print('type must be either "dog" or "cat"')
        return False
 
    elif input_data['sex'] not in valid_sex_types:
        print('sex must be either "female", "male"')
        return False
    
    elif input_data['female_status'] not in valid_female_status:
        print('female_status must be either "lactation", "gestation", "none"')
        return False
    
    else:
        for var_non_negative in li_non_negative:
            var = input_data[var_non_negative]
            if not is_non_negative(var):
                print(var_non_negative, ' must be non nogative')
                return False
            
    return True


# Input data - Personal Information of the Companion Animal

input_data = {'type' : 'dog', 
              'sex' : 'male', 
              'female_status' : 'lactation', 
              'week' : 20, 
              'body_weight' : 3, 
              'dog_breed' : '살루키', 
              'dog_group' : 'Moderate activity (1 – 3 h/day) (low impact activity)', 
              'cat_breed' : '노르웨이숲', 
              'cat_group' : 'Active cats', 
              'weeks_after_pregnant' : 4, 
              'weeks_of_lactation' : 4, 
              'number_of_puppies' : 4, 
              'number_of_kittens' : 4
             }

dict_week_lactation_dog = {1:0.75, 2:0.95, 3:1.1, 4:1.2}
dict_week_lactation_cat = {1:0.9, 2:0.9, 3:1.2, 4:1.2, 5:1.1, 6:1.0, 7:0.8}

# Check the type of the input data - dog, cat

if not is_valid_input_data(input_data):
    sys.exit() 
else:
    print("\n<input_data>\n")
    print(input_data)
    
# Get Multiplier & Expected body weight values from dog_group & dog_breed information
if input_data['type'] == 'dog':
    try:
        # df_multiplier_dog : Multiplier information corresponding to dog group
        # df_expected_body_weight_dog : Expected body weight information corresponding to dog breed
        path_db = os.path.abspath('') + "/input/DB_companion_animal.xlsx"
        df_multiplier_dog = pd.read_excel(path_db, sheet_name = "multiplier_dog")
        df_expected_body_weight_dog = pd.read_excel(path_db, sheet_name = "expected_body_weight_dog")
  
        condition = (df_multiplier_dog.dog_group == input_data['dog_group']) 
        multiplier_dog = df_multiplier_dog[condition]['multiplier'].values[0]
    
        condition = (df_expected_body_weight_dog.dog_breed == input_data['dog_breed']) 
        if input_data['sex'] == 'male':
            expected_body_weight_dog = df_expected_body_weight_dog[condition]['expected_body_weight_male'].values[0]
      
        else:
            expected_body_weight_dog = df_expected_body_weight_dog[condition]['expected_body_weight_female'].values[0]
        

    
        ## Calculate the Daily Metabolisable Energy Requirements of Dogs
        # Puppies after weaning
        
        if input_data['week'] < 0:
            sys.exit() 
        
        elif input_data['week'] < 8:
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
                    sys.exit()
      
            # Bitches not in gestation nor lactation    
            else:
                BW = input_data['body_weight']
                ME = multiplier_dog * BW**0.75     
    
        # Males    
        elif input_data['sex'] == 'male':
            BW = input_data['body_weight']
            ME = multiplier_dog * BW**0.75     
          
        # Exceptional case  
        else:
            print("Please check the sex value!")
            sys.exit()
            
    # Exceptional case    
    except:
        print("Please check the input values (ex, dog_group, dog_breed, week, sex, female_status, number_of_puppies etc.)!")
        sys.exit()


# Get Multiplier & Expected body weight values from cat_group & cat_breed information
elif input_data['type'] == 'cat':
    try:
        # df_multiplier_cat : Multiplier information corresponding to cat group
        # df_expected_body_weight_cat : Expected body weight information corresponding to cat breed
        path_db = os.path.abspath('') + "/input/DB_companion_animal.xlsx"
        df_multiplier_cat = pd.read_excel(path_db, sheet_name = "multiplier_cat")
        df_expected_body_weight_cat = pd.read_excel(path_db, sheet_name = "expected_body_weight_cat")
  
        condition = (df_multiplier_cat.cat_group == input_data['cat_group']) 
        multiplier_cat = df_multiplier_cat[condition]['multiplier'].values[0]
    
        condition = (df_expected_body_weight_cat.cat_breed == input_data['cat_breed']) 
        if input_data['sex'] == 'male':
            expected_body_weight_cat = df_expected_body_weight_cat[condition]['expected_body_weight_male'].values[0]
      
        else:
            expected_body_weight_cat = df_expected_body_weight_cat[condition]['expected_body_weight_female'].values[0]
        
        ## Calculate the Daily Metabolisable Energy Requirements of Cats
        # Kittens after weaning
        
        if input_data['week'] < 0:
            sys.exit() 
        
        elif input_data['week'] <= 52:
    
            p = input_data['body_weight'] / expected_body_weight_cat
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
          
        # Exceptional case  
        else:
            print("Please check the sex value!")
            sys.exit()
      
    # Exceptional case    
    except:
        print("Please check the input values (ex, cat_group, cat_breed, week, sex, female_status, number_of_kittens etc.)!")   
        sys.exit()

print("\n<1.Result of the Metabolisable Energy>\n")
print("Metabolisable Energy:",  ME, "kcal")
print("건물섭취량:",  ME/4, "g")

## Calculate the Recommended nutrients for Dogs 

try:
    if input_data['type'] == 'dog':
        # df_recom_nutrient_dog : Recommended nutrient levels per 1000kcal of ME for dog
        path_db = os.path.abspath('') + "/input/DB_companion_animal.xlsx"
        df_recom_nutrient_dog = pd.read_excel(path_db, sheet_name = "recom_nutrient_dog")    

        df_recom_nutrient_dog['min_nutrient'] = '-'
        df_recom_nutrient_dog['max_nutrient'] = '-'
        
        # Calculate the Maximum Recommended nutrients
        for idx, row in df_recom_nutrient_dog.iterrows():
            if row['adult'] != '-':
                adult_max = row['max'] * row['adult']
                if (row['adult_max'] == '-') or (adult_max <= row['adult_max']):
                    df_recom_nutrient_dog.loc[idx, 'adult_max'] = row['max'] * row['adult']

            if row['early_growth'] != '-':
                adult_max = row['max'] * row['early_growth']
                if (row['early_growth_max'] == '-') or (adult_max <= row['early_growth_max']):
                    df_recom_nutrient_dog.loc[idx, 'early_growth_max'] = row['max'] * row['early_growth'] 
            
            if row['late_growth'] != '-':
                adult_max = row['max'] * row['late_growth']
                if (row['late_growth_max'] == '-') or (adult_max <= row['late_growth_max']):
                    df_recom_nutrient_dog.loc[idx, 'late_growth_max'] = row['max'] * row['late_growth'] 
                    
            if row['reproduction'] != '-':
                adult_max = row['max'] * row['reproduction']
                if (row['reproduction_max'] == '-') or (adult_max <= row['adult_max']):
                    df_recom_nutrient_dog.loc[idx, 'reproduction_max'] = row['max'] * row['reproduction']                    
                                                       
        
        for idx, row in df_recom_nutrient_dog.iterrows():
            min_nutrient = '-'
            max_nutrient = '-'
            unit_conv = ME / 1000
 
            if row['nutrient'] == 'Ca / P ratio':
                unit_conv = 1             
            
            if input_data['week'] < 14:
                if row['early_growth'] != '-':
                    min_nutrient = float(row['early_growth']) * unit_conv  

                if row['early_growth_max'] != '-':
                    max_nutrient = float(row['early_growth_max']) * unit_conv
                 
            elif input_data['week'] <= 52:              
                if row['late_growth'] != '-':
                    
                    if (expected_body_weight_dog > 15) & (input_data['week'] >= 25) & (row['nutrient'] == 'Calcium'):
                        min_nutrient = 2.0 * unit_conv
                    
                    elif (expected_body_weight_dog <= 15) & (row['nutrient'] == 'Calcium'):
                        min_nutrient = 2.0 * unit_conv                        
                    
                    else:                      
                        min_nutrient = float(row['late_growth']) * unit_conv                        
                      
                if row['late_growth_max'] != '-':
                   
                    if (expected_body_weight_dog > 15) & (input_data['week'] >= 25) & (row['nutrient'] == 'Ca / P ratio'):
                        max_nutrient = 1.8 * unit_conv
                    elif (expected_body_weight_dog <= 15) & (row['nutrient'] == 'Ca / P ratio'):
                        max_nutrient = 1.8 * unit_conv                        
                    else:                      
                        max_nutrient = float(row['late_growth_max']) * unit_conv
                    
            elif input_data['sex'] == 'female':
                if (input_data['female_status'] == 'gestation') | (input_data['female_status'] == 'lactation'):
                    if row['reproduction'] != '-':
                        min_nutrient = float(row['reproduction']) * unit_conv

                    if row['reproduction_max'] != '-':
                        max_nutrient = float(row['reproduction_max']) * unit_conv 
                        
                else:
                    if row['adult'] != '-':
                        min_nutrient = float(row['adult']) * unit_conv

                    if row['adult_max'] != '-':
                        max_nutrient = float(row['adult_max']) * unit_conv
                        
            else:
                if row['adult'] != '-':
                    min_nutrient = float(row['adult']) * unit_conv 
                    
                if row['adult_max'] != '-':
                    max_nutrient = float(row['adult_max']) * unit_conv                
        
            df_recom_nutrient_dog.loc[idx, 'min_nutrient'] = min_nutrient
            df_recom_nutrient_dog.loc[idx, 'max_nutrient'] = max_nutrient
                    
        df_recom_nutrient_dog = df_recom_nutrient_dog[['nutrient','unit', 'min_nutrient', 'max_nutrient']]
        df_recom_nutrient_output =  df_recom_nutrient_dog
        df_recom_nutrient_output.loc[-1] = ['Metabolisable Energy', 'kcal', ME, 1.3*ME]
        print("\n<2.Result of the Recommended Nutrients>\n")
        print(df_recom_nutrient_output)
    
    ## Calculate the Recommended nutrients for Cats 

    elif input_data['type'] == 'cat':
        # df_recom_nutrient_cat : Recommended nutrient levels per 1000kcal of ME for cat
        path_db = os.path.abspath('') + "/input/DB_companion_animal.xlsx"
        df_recom_nutrient_cat = pd.read_excel(path_db, sheet_name = "recom_nutrient_cat")    

        df_recom_nutrient_cat['min_nutrient'] = '-'
        df_recom_nutrient_cat['max_nutrient'] = '-'
        
        
        # Calculate the Maximum Recommended nutrients
        for idx, row in df_recom_nutrient_cat.iterrows():
            if row['adult'] != '-':
                adult_max = row['max'] * row['adult']
                if (row['adult_max'] == '-') or (adult_max <= row['adult_max']):
                    df_recom_nutrient_cat.loc[idx, 'adult_max'] = row['max'] * row['adult']

            if row['growth'] != '-':
                adult_max = row['max'] * row['growth']
                if (row['growth_max'] == '-') or (adult_max <= row['growth_max']):
                    df_recom_nutrient_cat.loc[idx, 'growth_max'] = row['max'] * row['growth'] 
                 
            if row['reproduction'] != '-':
                adult_max = row['max'] * row['reproduction']
                if (row['reproduction_max'] == '-') or (adult_max <= row['adult_max']):
                    df_recom_nutrient_cat.loc[idx, 'reproduction_max'] = row['max'] * row['reproduction']                    
        
              
        for idx, row in df_recom_nutrient_cat.iterrows():
            min_nutrient = '-'
            max_nutrient = '-'
            unit_conv = ME / 1000
            if row['nutrient'] == 'Ca / P ratio':
                unit_conv = 1
                
            if input_data['week'] <= 52:
                if row['growth'] != '-':
                    min_nutrient = float(row['growth']) * unit_conv  

                if row['growth_max'] != '-':
                    max_nutrient = float(row['growth_max']) * unit_conv                

            elif input_data['sex'] == 'female':
                if (input_data['female_status'] == 'gestation') | (input_data['female_status'] == 'lactation'):
                    if row['reproduction'] != '-':
                        min_nutrient = float(row['reproduction']) * unit_conv  

                    if row['reproduction_max'] != '-':
                        max_nutrient = float(row['reproduction_max']) * unit_conv                       

                else:
                    if row['adult'] != '-':
                        min_nutrient = float(row['adult']) * unit_conv  

                    if row['adult_max'] != '-':
                        max_nutrient = float(row['adult_max']) * unit_conv   
                        
                        
            else:
                if row['adult'] != '-':
                    min_nutrient = float(row['adult']) * unit_conv  

                if row['adult_max'] != '-':
                    max_nutrient = float(row['adult_max']) * unit_conv     
                    
            df_recom_nutrient_cat.loc[idx, 'min_nutrient'] = min_nutrient
            df_recom_nutrient_cat.loc[idx, 'max_nutrient'] = max_nutrient                    

        df_recom_nutrient_cat = df_recom_nutrient_cat[['nutrient','unit', 'min_nutrient', 'max_nutrient']]
        df_recom_nutrient_output =  df_recom_nutrient_cat 
        df_recom_nutrient_output.loc[-1] = ['Metabolisable Energy', 'kcal', ME, 1.3*ME]
        print("\n<2.Result of the Recommended Nutrients>\n")
        print(df_recom_nutrient_output)
             
except:
    print("Please check the DB_companion_animal")   
    sys.exit()
### Calculate the pet feeding ratios by using the Linear Programming Method

# df_raw_material : Raw material - Nutrient information

try:

    path_db_raw_material = os.path.abspath('') + "/input/DB_raw_materials_v2.xlsx"
    df_raw_material = pd.read_excel(path_db_raw_material, sheet_name='국가표준식품성분 Database 10.0')
    df_raw_material = df_raw_material.iloc[0:,3:]
    df_raw_material = df_raw_material.rename(columns=df_raw_material.iloc[0])
    df_raw_material = df_raw_material.drop(df_raw_material.index[0])
    df_raw_material = df_raw_material.dropna(subset=['가격']) 

    # dict_recom_nut : Dictionary of the Recommended nutrients    
        # Ca / P ratio, EPA + DHA (ω-3), Chloride, 
        # Vitamin B9 (Folic acid), Choline, Selenium  (dry diets), Selenium  (wet diets)
        # Methionine + Cystine, Phenylalanine + Tyrosine
        # Vitamin A, D, E, K, B7
        
    dict_recom_nut =   {'단백질':'Protein', 
                        '아르기닌':'Arginine', 
                        '히스티딘':'Histidine', 
                        '이소류신':'Isoleucine', 
                        '류신':'Leucine',
                        '라이신':'Lysine',
                        '메티오닌':'Methionine',
                        '페닐알라닌':'Phenylalanine',          
                        '트레오닌':'Threonine',
                        '트립토판':'Tryptophan',
                        '발린':'Valine',
                        '지방 ':'Fat',
                        '리놀레산\n(18:2(n-6))':'Linoleic acid (ω-6)',
                        '아라키돈산\n(20:4(n-6))':'Arachidonic acid (ω-6)',
                        '알파 \n리놀렌산\n(18:3 (n-3))':'Alpha-linolenic acid (ω-3)',
                        '칼슘':'Calcium', 
                        '인':'Phosphorus',
                        '칼륨':'Potassium',
                        '나트륨':'Sodium',
                        '마그네슘':'Magnesium',
                        '구리':'Copper',
                        '요오드':'Iodine',
                        '철':'Iron',
                        '망간':'Manganese',
                        '티아민':'Vitamin B1 (Thiamine)',
                        '리보플라빈':'Vitamin B2 (Riboflavin)',
                        '판토텐산':'Vitamin B5 (Pantothenic acid)',
                        '피리독신':'Vitamin B6 (Pyridoxine)',
                        '비타민 B12':'Vitamin B12 (Cyanocobalamin)',
                        '니아신':'Vitamin B3 (Niacin)',
                        '에너지':'Metabolisable Energy'
                        
                       }
    li_recom_nut_kor = list(dict_recom_nut.keys())
    li_recom_nut_eng = list(dict_recom_nut.values())
    
    df_raw_material = df_raw_material[['식품명', '가격', '최소 원료제한', '최대 원료제한']+li_recom_nut_kor]
    
    df_raw_material = df_raw_material.replace(np.nan, 0)  
    df_raw_material[li_recom_nut_kor]
    
    df_raw_material = df_raw_material.rename(columns=dict_recom_nut)
    df_raw_material = df_raw_material.rename(columns={'식품명':'raw_material', '가격':'price', 
                                                      '최소 원료제한':'min', '최대 원료제한':'max'})
    
    
    
    
    
    for idx, row in df_raw_material.iterrows():
        for nutrient in li_recom_nut_eng:
            if row[nutrient] == '-':
                df_raw_material.loc[idx, nutrient] = 0
            elif not isNumber(row[nutrient]):
                if idx>1:
                    if (')'  in row[nutrient]):
                        if ('.'  in row[nutrient]):
                            df_raw_material.loc[idx, nutrient] = float(re.findall("\d+.\d+",row[nutrient])[0])
                    
                        elif len(row[nutrient]) > 3:
                            df_raw_material.loc[idx, nutrient] = float(re.findall("\d+\d+",row[nutrient])[0])

                        else:
                            df_raw_material.loc[idx, nutrient] = float(re.findall("\d+",row[nutrient])[0])
                    else:
                        df_raw_material.loc[idx, nutrient] = 0
            else:
                df_raw_material.loc[idx, nutrient] = float(row[nutrient])
    
            df_raw_material.loc[1, nutrient]
            
            if idx>1:
            
                if df_raw_material.loc[1, nutrient] == 'g':
                    df_raw_material.loc[idx, nutrient] *= 10
                elif df_raw_material.loc[1, nutrient] == 'mg':
                    df_raw_material.loc[idx, nutrient] *= 10*0.001
                elif df_raw_material.loc[1, nutrient] == 'μg':
                    df_raw_material.loc[idx, nutrient] *= 10*0.000001                     
                elif df_raw_material.loc[1, nutrient] == 'kcal':
                    df_raw_material.loc[idx, nutrient] *= 10       
        
        
        if row['min'] is None:
            df_raw_material.loc[idx, 'min'] = 0 
        if row['max'] is None:
            df_raw_material.loc[idx, 'max'] = 100         
        

    df_raw_material.drop([1], axis=0, inplace=True)

    np_coeff = df_raw_material[li_recom_nut_eng].transpose().values
    np_coeff *= -1
    np_coeff = np.concatenate([np_coeff, -np_coeff], 0)

    A_ub = np_coeff.tolist()
   


    # Unit Conversion of the Required nutrient requirements 

    b_ub = []
    
    for nutrient in li_recom_nut_eng:
        condition = (df_recom_nutrient_output.nutrient == nutrient)
        min_nutrient = df_recom_nutrient_output[condition]['min_nutrient'].values[0]    
        unit = df_recom_nutrient_output[condition]['unit'].values[0]    

        if unit == 'g':
            b_ub.append(min_nutrient*-1)  

        elif unit == 'mg':
            b_ub.append(min_nutrient*-0.001)  

        elif unit == 'µg':
            b_ub.append(min_nutrient*-0.000001)  

        else:
            b_ub.append(min_nutrient*-1)
            
    for nutrient in li_recom_nut_eng:
        condition = (df_recom_nutrient_output.nutrient == nutrient)
        max_nutrient = df_recom_nutrient_output[condition]['max_nutrient'].values[0]    
        unit = df_recom_nutrient_output[condition]['unit'].values[0]    

        if unit == 'g':
            b_ub.append(max_nutrient)  

        elif unit == 'mg':
            b_ub.append(max_nutrient*0.001)  

        elif unit == 'µg':
            b_ub.append(max_nutrient*0.000001)  

        else:
            b_ub.append(max_nutrient)
            
    # Optimization - Price of the raw materials        
    c = df_raw_material['price'].values.tolist()

    # Constraint - Sum of the combined ratio is equal to 1
    A_eq = np.ones((1,np_coeff.shape[1])).tolist()
    b_eq = [0.5]

    # Non-Negativity Constraints

    bounds = []
    for idx, row in df_raw_material[['min', 'max']].iterrows():
        bounds.append((row['min']*b_eq[0]/100,row['max']*b_eq[0]/100))

   

    # Linear Programming
    result = scipy.optimize.linprog(c=c, A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq, bounds=bounds)
    #result = scipy.optimize.linprog(A_ub=A_ub, b_ub=b_ub, A_eq=A_eq, b_eq=b_eq, bounds=bounds)

    # Show the result of the pet feeding ratios

    print("\n<3.Result of the Pet Feeding Ratio[%]>\n")
    
    if result.success:
        for idx in range(len(result.x)):
            if result.x[idx] != 0:
                weight_raw = round(result.x[idx], 3)
                ratio_raw = round(result.x[idx]/b_eq[0]*100, 3)
                print(df_raw_material.iloc[idx]['raw_material'], weight_raw,'[kg]',ratio_raw,'[%]')

    else:
        print("No solution for pet feeding ratios")
        sys.exit()
 
 
except:
    print("No solution for pet feeding ratios")   
    sys.exit()
