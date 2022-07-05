# Rework the saved HTML from OpenOffice Calc to be more friendly and readable 

# Using OpenOffice Calc (file -> preview in web browser) to create the HTML. Once the browser opens the page,
# use "save page as" to create the HTML file as homicide.htm. Run this program from that directory and it will
# create homicide_files/homicide.htm and homicide_files/homicide_cdc_original.htm which is the updated
# web pages.

import glob

def html_aref(filename, description):
  if description == '':
    description = 'all'
  return '<li><a id="' + filename + '" onclick="load_table(this);">' + description + '</a></li>\n'

filelist = glob.glob('*.htm*')
filename = ""
while filename == '':
  for i in range(0, len(filelist) ):
    print(i, filelist[i])
  i = input('Enter number of the file of the web page saved from OpenOffice Calc: ')
  if i.isdigit() and int(i) < len(filelist):
    filename = filelist[int(i)]    
  else:
    print('\n', i, ' is not a number in the file list \n')
print('\nProcessing file: ', filename)

with open( filename,"r") as infile:
  input = infile.read()
  infile.close()

# The <a href="$xxxx" statments for the menu
byage = ''
homicides = ''
unknown = ''
original = ''

next_table = input.find("<a ", input.find("</center>")) # First spreadsheet is after the </center> 
while next_table > 0:
  work = input[next_table:]
  table_name = input[input.find('<em>',next_table)+4 : input.find('</em>', next_table)].lower()

  with open("./" + table_name + ".table","w") as outfile:
    outfile.write(input[next_table: input.find("</table>", next_table)+8 ])
    outfile.close()

  next_table = input.find("<a ", next_table+3) 

  # Add table to the to the appropriate menu
  if table_name.lower().find("original") >= 0:
    original += html_aref(table_name, table_name ) 

  elif table_name.find("by age") >= 0:
    byage += html_aref(table_name, table_name.replace("by age","") ) 

  elif table_name.find("homicide") >= 0:
    homicides += html_aref(table_name, table_name.replace("homicides","").replace("homicide","") ) 

  else: 
    unknown += html_aref(table_name, table_name)

if unknown != "":
  unknown = '''<li><a>graphs with errors</a>
            <ul>
            ''' + unknown + '''
            </ul>
          </li>
          '''

def build_menu(menu_data):
  with open("menuHomicide.table","w") as outfile:
    for data in menu_data:
      outfile.write( data )
    outfile.close()

build_menu( [ '''
            <li><a>Homicides</a>
              <ul id="first_graph_display">
              ''', homicides, '''
              </ul>
            </li>
            <li><a>homicides/suicides by age</a>
              <ul>
              ''', byage, '''
              </ul>
            </li>
            ''', unknown 
] )

#            <li><a>Original CDC data</a>
#              <ul>
#              ''', original, '''
#              </ul>
#             </li>

print("Completed")