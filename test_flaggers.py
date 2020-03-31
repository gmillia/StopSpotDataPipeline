from flaggers.flagger import flaggers, Flags
from flaggers.dataRow import dataRow
import json

# These structures are only to demosntrate that flaggers work,
# and not a final say on what our data should look like.
data_dict = {"Placeholder" : [], "Data" : []}

# for data in data_dict.keys():
#   for flagger in flaggers:
#     flags = flagger.flag(data)
#     data_dict[data] += flags

# print(data_dict)

#Helper function that tests all Null flags individually (one at a time)
#@positive=true, tests so that flags 'fire'
#@positive=false, test so that flags don't 'fire'
def testNullFlagsIndividual(null_flagger, positive):
  corr_cnt = 0  #count for correct null flag checks
  inc_cnt = 0    #count for incorrect null flag checks
  #Step 1: Transform Nulls class fields into dict, and then transform into keys and vals lists
  data = dataRow()          #create Nulls object
  data_vars = vars(data)      #create dict from object
  data_names = list(data_vars.keys())    #create keys list from dict
  data_vals = list(data_vars.values())  #create vals list from dict

  #Step 2: Check for each flag and its value
  for i in range(len(data_vars)):
    if(positive): json_obj = '{"' + data_names[i] + '":null}'  #create JSON object with 1 value: current flag
    else: json_obj = '{"' + data_names[i] + '":"good"}'
    
    python_obj = json.loads(json_obj)        #create Python object from JSON object

    ret_flag = null_flagger.flag(python_obj)  #check Python object with 1 value for a flag

    #Testing positive: should fire
    if(positive and len(ret_flag) > 0): 
      correct = ret_flag[0].value == i+1    #i + 1 since flags start from 1
      if(correct): corr_cnt += 1
      else: inc_cnt += 1
      #print('NULL CHECK -', ret_flag[0].name, ':', correct)
    #Testing negative: shouldn't fire
    else:
      if(len(ret_flag) == 0): corr_cnt += 1
      else: inc_cnt += 1

  print('-------------------------------------------------------------------------------')
  if(positive): print('Testing INDIVIDUAL for Positives [null flags should fire = return null_flag]')
  else: print('Testing INDIVIDUAL for Negatives [null flags shouldn\'t fire = not return null flag]')
  print('Correct:', corr_cnt)
  print('Incorrect:', inc_cnt)
  print('Success Rate:', (corr_cnt / len(data_names)) * 100, '%')
  print('-------------------------------------------------------------------------------')


#Tests full object (not one flag at a time)
def testNullFlagsFull(null_flagger, positive):
  #Step 1: Transform Nulls class fields into dict, and then transform into keys and vals lists
  data = dataRow()
  data_vars = vars(data)      #create dict from object, to import all the fields
  data_names = list(data_vars.keys())    #create keys list from dict
  data_vals = list(data_vars.values())  #create vals list from dict
  incorrect = 0

  #positive = must return a list of flags
  if(positive):
    ret_flags = flagger.flag(data_vars)
    correct = len(ret_flags)
    if(len(ret_flags) != len(data_vars)): 
      incorrect = len(data_vars) - len(ret_flags)
  #Negative = must return empty list
  else: 
    for i in range(len(data_vars)):
      data_vars[data_names[i]] = 'good_data'

    ret_flags = null_flagger.flag(data_vars)
    correct = len(ret_flags)
    if(len(ret_flags) != len(data_vars)): 
      incorrect = len(data_vars) - len(ret_flags)

  print('-------------------------------------------------------------------------------')
  if(positive): print('Testing  FULL for Positives [null flags should fire = return ret_flag list]')
  else: print('Testing FULL for Negatives [null flags shouldn\'t fire = empty ret_flag list]')
  print('Correct:', correct)
  print('Incorrect:', incorrect)
  print('Success rate:', (correct / len(data_vars)) * 100, '%')
  print('-------------------------------------------------------------------------------')

def runNullTests(flagger):
  #Calling Individual test functions
  testNullFlagsIndividual(flagger, True)
  testNullFlagsIndividual(flagger, False)

  #Calling Full test functions
  testNullFlagsFull(flagger, True)
  testNullFlagsFull(flagger, False)

for flagger in flaggers:
  #currently on a null flagger
  if(flagger.name == 'Null'): runNullTests(flagger)