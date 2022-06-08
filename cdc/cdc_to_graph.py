import sys

print("processing file:", sys.argv[1])
filename = sys.argv[1]   # input file name
# filename = "all_murders.csv"

year_low = 9999
year_high = 0
out = {}
with open(filename, "r") as infile:

  # Verify the title line is correct 
  w = infile.readline().split("\t")  # tab seperated file
  expected_title_homicides = ['"Notes"', '"Year"', '"Year Code"', '"Single Race 6"', 
    '"Single Race 6 Code"', '"Hispanic Origin"', '"Hispanic Origin Code"',
    '"Gender"', '"Gender Code"', 'Deaths', 'Population', 'Crude Rate\n']
  expected_title_homicides_byage = ['"Notes"', '"Single Race 6"', '"Single Race 6 Code"', '"Hispanic Origin"', '"Hispanic Origin Code"', '"Year"', '"Year Code"', '"Single-Year Ages"', '"Single-Year Ages Code"', '"Gender"', '"Gender Code"', 'Deaths', 'Population', 'Crude Rate\n']

  notes_col = w.index('"Notes"')
  year_col = w.index('"Year"')
  race_col = w.index('"Single Race 6"')
  ethnic_col = w.index('"Hispanic Origin"')
  gender_col = w.index('"Gender"')
  deaths_col = w.index('Deaths')
  population_col = w.index('Population')
  per100k_col = w.index('Crude Rate\n') 

  if w == expected_title_homicides: # verify that the title is correct
    type = "homicides"

  elif w == expected_title_homicides_byage: # verify that the title is correct
    type = "homicides_byage"
    age_col = w.index('"Single-Year Ages"')
  else:  
    print("Aborting because CDC report title line is not correct:", 
      "\n  expected:", expected_title_homicides,
      "\n        or:", expected_title_homicides_byage,
      "\n  found:", w)
    exit()

  for line in infile:

    w = line.split("\t")  # tab seperated file

    if (w[notes_col] == '"Total"' and w[1] == "") or w[notes_col] == '"---"\n':  # Total for all years is last line of data
      break # finished data  

    # Ignore race without an ethnicity total lines
    if w[notes_col] == '"Total"':
      if w[ethnic_col] == "" and w[race_col] != "":
        continue
      if type == "homicides_byage" and w[age_col] == "":
        continue

    year = int(w[year_col].strip('"'))

    # Simplify text
    if w[race_col] == '"Black or African American"':
      w[race_col] = '"Black"'
    if w[ethnic_col] == '"Hispanic or Latino"':
      w[ethnic_col] = '"Hispanic"'
    elif w[ethnic_col] == '"Not Hispanic or Latino"':
      w[ethnic_col] = '"Not Hispanic"'

    if type == "homicides_byage":
      key = '"' + w[race_col].strip('"') + " (" + w[ethnic_col].strip('"') + ') ' + w[gender_col].strip('"') + " " + w[year_col].strip('"') +  '"'
    elif w[year_col+2] == "":  # Total for the year
      key = "Total by year"
    else:
      key = '"' + w[race_col].strip('"') + " (" + w[ethnic_col].strip('"') + ') ' + w[gender_col].strip('"') + '"'

    if out.get(key,"") == "":  # new row
      if type == "homicides_byage":
        out[key] = { "deaths" : [""]*102, "per100k" : [""]*102, "population" :[""]*102 }
      else:
        out[key] = {"deaths":{}, "per100k":{}, "population":{}}
 
    if year < year_low:
      year_low = year
    if year > year_high:
      year_high = year

    if type == "homicides_byage":
      age = w[age_col]
      if age == '"1 year"':
        age = 1
      elif age == '"< 1 year"':
        age = 0
      elif age == '"100+ years"':
        age = 100
      elif age == '"Not Stated"':
        age = 101
      else:
        age = int(age[1:-6])    # remove word years
      out[key]["deaths"][age] = w[deaths_col]
      out[key]["per100k"][age] = w[per100k_col].strip("\n")   # remove newline
      out[key]["population"][age] = w[population_col]
    else:
      out[key]["deaths"][year] = w[deaths_col]
      out[key]["per100k"][year] = w[per100k_col].strip("\n")   # remove newline
      out[key]["population"][year] = w[population_col]

  infile.close()

with open("graph_"+filename, "w") as outfile1, open("graph_per100k_"+filename, "w") as outfile2:
  if type == "homicides_byage":
     
    outfile1.write('"race, gender, race"\t"< 1"\t  1\t  2\t  3\t  4\t  5\t  6\t  7\t  8\t  9\t  10\t  11\t  12\t  13\t  14\t  15\t  16\t  17\t  18\t  19\t  20\t  21\t  22\t  23\t  24\t  25\t  26\t  27\t  28\t  29\t 30\t  31\t  32\t  33\t  34\t  35\t  36\t  37\t  38\t  39\t  40\t  41\t  42\t  43\t  44\t  45\t  46\t  47\t  48\t  49\t  50\t  51\t  52\t  53\t  54\t  55\t  56\t  57\t  58\t  59\t  60\t  61\t  62\t  63\t  64\t  65\t  66\t  67\t  68\t  69\t  70\t  71\t  72\t  73\t  74\t  75\t  76\t  77\t  78\t  79\t  80\t  81\t  82\t  83\t  84\t  85\t  86\t  87\t  88\t  89\t  90\t  91\t  92\t  93\t  94\t  95\t  96\t  97\t  98\t  99\t  "100+"\t  "Not Stated"\t\n') 

    outfile2.write('"year, race & gender"\t"< 1"\t  1\t  2\t  3\t  4\t  5\t  6\t  7\t  8\t  9\t  10\t  11\t  12\t  13\t  14\t  15\t  16\t  17\t  18\t  19\t  20\t  21\t  22\t  23\t  24\t  25\t  26\t  27\t  28\t  29\t 30\t  31\t  32\t  33\t  34\t  35\t  36\t  37\t  38\t  39\t  40\t  41\t  42\t  43\t  44\t  45\t  46\t  47\t  48\t  49\t  50\t  51\t  52\t  53\t  54\t  55\t  56\t  57\t  58\t  59\t  60\t  61\t  62\t  63\t  64\t  65\t  66\t  67\t  68\t  69\t  70\t  71\t  72\t  73\t  74\t  75\t  76\t  77\t  78\t  79\t  80\t  81\t  82\t  83\t  84\t  85\t  86\t  87\t  88\t  89\t  90\t  91\t  92\t  93\t  94\t  95\t  96\t  97\t  98\t  99\t  "100+"\t  "Not Stated"\t\n') 

    for key in out:
      outfile1.write(key+"\t" + "\t".join(out[key]["deaths"]) + "\n")
      outfile2.write(key+"\t" + "\t".join(out[key]["per100k"]) + "\n")
  else:
    outfile1.write('"race & gender"\t "2018"\t "2019"\t "2020"\t "2019\n% change"\t "2020\n% change"\t\n')
    outfile2.write('"race & gender"\t "2018"\t "2019"\t "2020"\t "2019\n% change"\t "2020\n% change"\t\n')
    for key in out:
      outfile1.write(key+"\t")
      outfile2.write(key+"\t")
      for y in range(year_low, year_high+1):
        outfile1.write(out[key]["deaths"].get(y,"0") + "\t")
        outfile2.write(out[key]["per100k"].get(y,"0") + "\t")
      outfile1.write("\n")
      outfile2.write("\n")

  outfile1.close()
  outfile2.close()

print("all done")
