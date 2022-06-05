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
  expected_title_homicides_byage = ['"Notes"', '"Year"', '"Year Code"', '"Single Race 6"',
    '"Single Race 6 Code"', '"Hispanic Origin"', '"Hispanic Origin Code"', '"Single-Year Ages"',
    '"Single-Year Ages Code"', 'Deaths', 'Population', 'Crude Rate\n']
  if w == expected_title_homicides: # verify that the title is correct
    type = "homicides"
  elif w == expected_title_homicides_byage: # verify that the title is correct
    type = "homicides_black"
  else:  
    print("Aborting because CDC report title line is not correct:", 
      "\n  expected:", expected_title_homicides,
      "\n        or:", expected_title_homicides_byage,
      "\n  found:", w)
    exit()

  for line in infile:

    w = line.split("\t")  # tab seperated file

    if (w[0] == '"Total"' and w[1] == "") or w[0] == '"---"\n':  # Total for all years is last line of data
      break # finished data  

    year = int(w[1].strip('"'))

    # Ignore race without an ethnicity total lines
    if w[0] == '"Total"' and w[5] == "" and w[3] != "":
      continue

    # Simplify text
    if w[3] == '"Black or African American"':
      w[3] = '"Black"'
    if w[5] == '"Hispanic or Latino"':
      w[5] = '"Hispanic"'
    elif w[5] == '"Not Hispanic or Latino"':
      w[5] = '"Not Hispanic"'

    if w[3] == "":  # Total for the year
      key = "Total by year"
    else:
      key = '"' + w[3].strip('"') + " (" + w[5].strip('"') + ') ' + w[7].strip('"') + '"' # race, ethnicity, gender

    if out.get(key,"") == "":
      out[key] = {"deaths":{}, "per100k":{}, "population":{}}
 
    if year < year_low:
      year_low = year
    if year > year_high:
      year_high = year

    out[key]["deaths"][year] = w[9]
    out[key]["per100k"][year] = w[11].strip("\n")   # remove newline
    out[key]["population"][year] = w[10]

  infile.close()

with open("graph_"+filename, "w") as outfile1, open("graph_per100k_"+filename, "w") as outfile2:
  outfile1.write('"race"\t "2018"\t "2019"\t "2020"\t "2019\n% change"\t "2020\n% change"\t\n')
  outfile2.write('"race"\t "2018"\t "2019"\t "2020"\t "2019\n% change"\t "2020\n% change"\t\n')
  for key in out:
    w1 = key+"\t"
    w2 = key+"\t"
    for y in range(year_low, year_high+1):
      w1 += out[key]["deaths"].get(y,"0") + "\t"
      w2 += out[key]["per100k"].get(y,"0") + "\t"
    outfile1.write(w1+"\n")
    outfile2.write(w2+"\n")
  outfile1.close()
  outfile2.close()

print("all done")
