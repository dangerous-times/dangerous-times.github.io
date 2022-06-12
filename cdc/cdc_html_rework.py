# Rework the saved HTML from OpenOffice Calc to be more friendly and readable 

# Using OpenOffice Calc (file -> preview in web browser) to create the HTML. Once the browser opens the page,
# use "save page as" to create the HTML file as homicide.htm. Run this program from that directory and it will
# create homicide_files/homicide.htm and homicide_files/homicide_cdc_original.htm which is the updated
# web pages.

with open("homicide.htm","r") as infile:
  input = infile.read()
  infile.close()

print("creating menu")

# Get the <a href="$xxxx" statments for the menu
end_center = input.find("</center>")
overview = input[input.find("<center>"): end_center].lower().split("#")   # <a href=#xxxx
del overview[0]  # Get rid of leading <a info"
byage = []
per100k = []
homicides = []
unknown = []
original = []
sheet_count = len(overview)

html_a = ["",""]     #  A HREF tag and description    
while len(overview):
  work = overview.pop(0)
  html_a[0] = work[:work.find('"')]
  html_a[1] = work[work.find('>')+1: work.find('</a>')]

  if html_a[1].find("original") >= 0:
    original.append(html_a.copy()) 

  elif html_a[1].find("by age") >= 0:
    html_a[1] = html_a[1].replace("by age","")
    byage.append(html_a.copy()) 

  elif html_a[1].find("per 100k") >= 0:
    html_a[1] = html_a[1].replace("per 100k","").replace("homicides","").replace("homicide","").replace("> <",">all usa<")
    per100k.append(html_a.copy()) 

  elif html_a[1].find("homicide") >= 0:
    html_a[1] = html_a[1].replace("homicides","").replace("homicide","").replace("><",">all usa<")
    homicides.append(html_a.copy()) 

  else: 
    unknown.append(html_a.copy())

def build_menu(menu_data):
  with open("./homicide_files/menu_list.js","w") as outfile:
    outfile.write("work = `")
    for menu_list in menu_data:
      if isinstance(menu_list,str):
        outfile.write(menu_list)
      else:
        for menu_item in menu_list:
          menu_item[1] = menu_item[1].strip(" ")
          if menu_item == []:
            print("null menu item")
            continue
          if menu_item[1] == "":
            menu_item[1] = "all USA"
          outfile.write('<li><a href="#" onclick="change_graph(\'' + menu_item[0] + '\');">' + menu_item[1] + '</a></li>\n')
    outfile.write("""`;
      load_menu_2(work);
      delete work;
      """)
    outfile.close()

build_menu( ['''
  <div class="menu">
    <nav>
      <ul class="nav-menu nav-center">
        <li><a href="#" class="nav-active">Home</a></li>
        <li><a>Homicide graphs</a>
          <ul>
            <li><a>Per 100K</a>
              <ul>
              ''', per100k,  '''
              </ul>
            </li>
            <li><a>All homicides</a>
              <ul>
              ''', homicides, '''
              </ul>
            </li>
            <li><a name="uuuu">All homicides by age</a>
              <ul>
              ''', byage, '''
              </ul>
            </li>
            <li><a>graphs with errors</a>
              <ul>
              ''', unknown, '''
              </ul>
            </li>
          </ul>
        </li>
        <li><a href="#">Original CDC data</a>
          <ul>
          ''', original, '''
          </ul>
        </li>
        <li><a href="#">Download spreadsheet</a>
          <ul>
            <li><a href="cdc_to_graph.py" target="__blank">cdc_to_graph.py</a>.</li>
          </ul>
        </li>
      </ul>
    </nav>
  </div>
'''])

next_table = input.find("<a ",end_center)
while next_table > 0:
  table_name_start = input.find('"',next_table)+1 
  table_name = input[table_name_start: input.find('"',table_name_start)]
  with open("./homicide_files/" + table_name + ".table","w") as outfile:
    outfile.write(input[next_table: input.find("</table>", next_table)+8])
    outfile.close()
  next_table = input.find("<a ", next_table+3) 

print("Completed")