import sys
import glob

from tomlkit import integer

byage_header = ''

expected_title_homicides = ['Notes', 'Year', 'Year Code', 'Single Race 6', 
  'Single Race 6 Code', 'Hispanic Origin', 'Hispanic Origin Code',
  'Gender', 'Gender Code', 'Deaths', 'Population', 'Crude Rate']

expected_title_homicides_byage = ['Notes', 'Single Race 6', 'Single Race 6 Code', 
  'Hispanic Origin', 'Hispanic Origin Code', 'Year', 'Year Code', 
  'Single-Year Ages', 'Single-Year Ages Code', 'Gender', 'Gender Code', 'Deaths', 
  'Population', 'Crude Rate']

files_list = []

for filename in glob.glob('*original*.csv'):
    
  print('processing file:', filename)

  files_list.append(filename[:-4])  # new file name

  year_low = 9999
  year_high = 0
  out = {}
  with open(filename, 'r') as infile:

    # Verify the title line is correct 
    w = infile.readline().replace('"','').replace('\n','').split('\t')  # tab seperated csv file

    if w == expected_title_homicides: # verify that the title is correct
      type = 'homicides'

    elif w == expected_title_homicides_byage: # verify that the title is correct
      type = 'homicides_byage'
      age_col = w.index('Single-Year Ages Code')

    else:  
      print('Aborting because CDC report title line is not correct:', 
        '\n  expected:', expected_title_homicides,
        '\n        or:', expected_title_homicides_byage,
        '\n  found:', w)
      exit()

    notes_col = w.index('Notes')
    year_col = w.index('Year')
    race_col = w.index('Single Race 6')
    ethnic_col = w.index('Hispanic Origin')
    gender_col = w.index('Gender')
    deaths_col = w.index('Deaths')
    population_col = w.index('Population')
    per100k_col = w.index('Crude Rate') 
    if w[per100k_col] and w[per100k_col].isdigit():  # make sure all numbers have 1 decimal digit
      w[per100k_col] += ".0"

    for line in infile:

      w = line.replace('"','').replace('\n','').replace('Unreliable','').replace('Not Applicable','').split('\t')  # tab seperated file

      if (w[notes_col] == 'Total' and w[1] == '') or w[notes_col] == '---':  # Total for all years is last line of data
        break # finished data  

      # Ignore race without an ethnicity total lines
      if w[notes_col] == 'Total':
        if w[ethnic_col] == '' and w[race_col] != '':
          continue
        if type == 'homicides_byage' and w[age_col] == '':
          continue

      year = int(w[year_col].strip(''))

      # Simplify text
      if w[race_col] == 'Black or African American':
        w[race_col] = 'Black'
      if w[ethnic_col] == 'Hispanic or Latino':
        w[ethnic_col] = 'Hispanic'
      elif w[ethnic_col] == 'Not Hispanic or Latino':
        w[ethnic_col] = 'Not Hispanic'

      if type == 'homicides_byage':
        key = w[race_col].strip('') + ' (' + w[ethnic_col].strip('') + ') ' + w[gender_col].strip('') + ' ' + w[year_col].strip('')
      elif w[year_col+2] == '':  # Total for the year
        key = 'Total by year'
      else:
        key = w[race_col].strip('') + ' (' + w[ethnic_col].strip('') + ') ' + w[gender_col].strip('')

      # if new key then we must create it
      if out.get(key,'') == '':  # new row
        if type == 'homicides_byage':
          out[key] = { 'deaths' : ['']*102, 'per100k' : ['']*102, 'population' :['']*102 }
        else:
          out[key] = {'deaths':{}, 'per100k':{}, 'population':{}}

      # "by age" spreadsheet
      if type == 'homicides_byage':
        if w[age_col] == "NS":
          age = 101      # Not stated column
        else:
          age = integer(w[age_col])
        out[key]['deaths'][age] = w[deaths_col]
        out[key]['per100k'][age] = w[per100k_col]   # remove newline
        out[key]['population'][age] = w[population_col]

      # by year spreadsheet
      else:  # by year
        if year < year_low:
          year_low = year
        if year > year_high:
          year_high = year
        out[key]['deaths'][year] = int(w[deaths_col])
        out[key]['per100k'][year] = w[per100k_col]   # remove newline
        out[key]['population'][year] = w[population_col]

    infile.close()

  with open('graph_'+filename[filename.lower().find(' cdc ')+5:], 'w') as outfile:
    # CDC graphs by race, gender & year
    if type == 'homicides_byage':
      if byage_header == '':
        age_seperated_by_tab = 'year, gender, race\t< 1\t'
        for i in range(1,100):
          byage_header += str(i) + '\t'
        byage_header = 'year, gender, race\tsort values\t"Per 100K\nby age <1"\t' + byage_header + '100+\tnot stated\t"Actual\nBy Age <1"\t' + byage_header + '100+\tnot stated\n'
      
      outfile.write(byage_header) 

      for key in out:
        byAgeSortValue = 0
        for y in out[key]['per100k']:
          if y != "":
            byAgeSortValue += float(y)
        outfile.write(key+ '\t' + str(round(byAgeSortValue,0)) + '\t' + '\t'.join(out[key]['per100k']) + '\t' + '\t'.join(out[key]['deaths']) + '\tverify column\t\n')

    # CDC graphs by race
    else:
      work = ''
      work2 = ''
      for year in range(year_low, year_high+1):
        work += '"' + str(year) + '\n per 100K"\t"'+ str(year) + '\nactual"\t'
        if year != year_low:
          work2 += '"' + str(year) + '\n% change"\t'
      outfile.write('race & gender\tsort value\t' + work + work2 + '\n')
      for key in out:
        sortValue = out[key]['per100k'].get(year_high,'')
        outfile.write(key + '\t' + sortValue + '\t')
        for y in range(year_low, year_high+1):
          outfile.write( out[key]['per100k'].get(y,'0') + '\t' + str(out[key]['deaths'].get(y,'0')) + '\t')
        # Insert % Change by year columns
        for y in range(year_low+1,year_high+1): 
          if out[key]['deaths'].get(y-1,0) != 0:  # Can't divide by 0
            outfile.write( str(round(((out[key]['deaths'].get(y,0)-out[key]['deaths'].get(y-1,0))/out[key]['deaths'].get(y-1,0)),2)) + '\t')
          else:
            outfile.write('\t')
        outfile.write('verify column\t\n')

    outfile.write('table_info data_filename="' + filename + '" data_type="' + type + '"\n')

    outfile.close()

with open('cdc_csv_files.csv', 'w') as outfile:
  for filename in files_list:   # files created for graphing
    outfile.write( 'graph_' + filename[filename.lower().find(' cdc ')+5:] + '\n')
  for filename in files_list:   # files created for graphing
    outfile.write( filename + '\n')
print('all done')