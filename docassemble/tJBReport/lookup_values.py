import pandas
from docassemble.base.util import path_and_mimetype

__all__ = ['get_score', 'get_choices', '_read_data', 'get_classification', 'value_in_list', 'validate_data_types', 'check_this_value']

def _read_data(file_name):
    the_xlsx_file, mimetype = path_and_mimetype(file_name)  # pylint: disable=unused-variable
    df = pandas.read_excel(the_xlsx_file, sheet_name=None, dtype=str,parse_dates=False)
    return df
  
def get_choices(tab_name, variable):
  try:
    if isinstance(variable, str):
      col_values = df[tab_name][variable].tolist()
      col_values = [[str(x).replace('.0', ''),str(x).replace('>', '\>')] for x in col_values]
      col_values = [["*INVALID RESPONSE*", "skip"]] + col_values
      return col_values
    elif isinstance(variable, list):
      col_values = df[tab_name][variable].to_dict(orient='records')
      return col_values
  except KeyError:
    raise ValueError(f'cannot find key: {tab_name} {variable}')
    

def value_in_list(x, value_list):
  values = [v[0] for v in value_list]
  return x[0] in values
    
def _lookup_value(df, value, lookup_variable: str='score', return_variable: str='percent', return_all: bool=False):
  try:
    if value in ['skip', '*INVALID RESPONSE*']:
      return '*INVALID RESPONSE*'

    values = df[df[lookup_variable] == value][return_variable].tolist()

    if return_all:
      return values
    else:
      return values[0]
  except:
      raise
      #return 'ERROR - FIX THIS CALCULATION: no value returned from lookup'

def get_score(value, tab_name, lookup_variable='score', return_variable='percent', return_all=False):
  try:
    #tab_name = [x for x in VARIABLE_CONFIG if x['variable'] == value][0]['type'].lower()
    print(df[tab_name])
    vals = _lookup_value(
        df=df[tab_name], 
        value=value,
        lookup_variable=lookup_variable,
        return_variable=return_variable,
        return_all=return_all
     )
    return vals
  except Exception as e:
    raise ValueError(f'there was an error in the "{value}" variable. we could not find a value of {value} in the "{lookup_variable}" column in the "{tab_name}" table. please check that you are entering a value for the correct lookup type (standard, scaled, etc.). If you believe you are entering a proper value then the code might not be configured properly for this variable. Please contact the developer to have that changed. full python error: {repr(e)}')

def get_classification(value, return_all=False):
  try:
    tab_name = 'classification'
    lookup_variable = 'percent'
    return_variable = 'classification'
    
    print(df[tab_name])
    vals = _lookup_value(
        df=df[tab_name], 
        value=value,
        lookup_variable=lookup_variable,
        return_variable=return_variable,
        return_all=return_all
     )
    return vals
  except Exception as e:
    raise ValueError(f'there was an error in the "{value}" variable. we could not find a value of {value} in the "{tab_name}" table. please check that you are entering a value for the correct lookup type (standard, scaled, etc.). If you believe you are entering a proper value then the code might not be configured properly for this variable. Please contact the developer to have that changed. full python error: {repr(e)}')
    
import gc
def get_local_objects():
  objs = gc.get_objects()
  print(objs)
  return objs

def validate_data_types():
    ### loop through all of the data entry fields and their intended field types
  ### if any of the entered values do not match the intended field type values, then it throws an error
  variable_types = get_choices(tab_name='variable', variable=['variable', 'type'])
  
  for pair in variable_types:
    variable, type = pair['variable'], pair['type']
    matching_type_choices = eval(f'{type}_CHOICES')
    if variable in vars() or variable in globals():
      if eval(variable) and eval(variable) not in [x[0] for x in matching_type_choices]:
        validation_error(f'This value is not a valid {type} variable.', field=variable)  

def check_this_value(x):
    return True

playground_file = 'docassemble.playground1PsychDoc'
prod_file = 'docassemble.JBReport'
#if user.email() == 'admin@admin.com':
#  lookup_file = playground_file
#else:
#  lookup_file = prod_file
file = f'{playground_file}:data/sources/lookup_psych2.xlsx'
df = _read_data(file)
VARIABLE_CONFIG = get_choices(tab_name='variable', variable=['variable', 'type'])
