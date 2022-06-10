# Rework the saved HTML from OpenOffice Calc to be more friendly and readable 

# Using OpenOffice Calc (file -> preview in web browser) to create the HTML. Once the browser opens the page,
# use "save page as" to create the HTML file as homicide.htm. Run this program from that directory and it will
# create homicide_files/homicide.htm and homicide_files/homicide_cdc_original.htm which is the updated
# web pages.

with open("homicide.htm","r") as infile:
  input = infile.read()
  infile.close()

pos = 0
def write_data(del_text, ins_text, file="both"):
  global pos
  text_start = input.find(del_text,pos)
  if text_start == -1:
    return -1
  if file != "file2":
    outfile1.write(input[pos:text_start])
    outfile1.write(ins_text)
  if file != "file1":
    outfile2.write(input[pos:text_start])
    outfile2.write(ins_text)
  pos = text_start+len(del_text)

with open("homicide_files/homicide.htm","w") as outfile1, open("homicide_files/homicide_cdc_original.htm","w") as outfile2: 

  write_data("<!--","")
  pos = input.find("-->",pos)  # remove first comment line

  write_data("<title></title>",'''
<!--
Meta data integrates the page to social media like twitter & facebook. Generated meta tags using https://metatags.io/ using <h1> above for title and first <p> for description. Don't forget to remove <br/>.
OG:URL & TWITTER:URL point to the full web address of the HTML.
OG:IMAGE & TWITTER:IMAGE point full web address of a PNG (not JPG) image. to be displayed. 
change OG:TYPE to article.
-->

<!-- Primary Meta Tags -->
<title>Firearm homicides up by staggering 35% in 2020 according to CDC data</title>
<meta name="title" content="Firearm homicides up by staggering 35% in 2020 according to CDC data">
<meta name="description" content="All Homicides up by 30% in 2020 for a total of 24,576! Black male homicide reached 59 per 100K black males while white male homicide was a mere 4 per 100K white males. Per capita, that's 18X! Look at the graphs and CDC data to see for yourself.">

<!-- Open Graph / Facebook -->
<meta property="og:type" content="article">
<meta property="og:url" content="https://dangerous-times.github.io/cdc/homicide.htm">
<meta property="og:title" content="Firearm homicides up by staggering 35% in 2020 according to CDC data">
<meta property="og:description" content="All Homicides up by 30% in 2020 for a total of 24,576! Black male homicide reached 59 per 100K black males while white male homicide was a mere 4 per 100K white males. Per capita, that's 18X! Look at the graphs and CDC data to see for yourself.">
<meta property="og:image" content="https://dangerous-times.github.io/cdc/social_media_photo1.png">


<!-- Twitter -->
<meta property="twitter:card" content="summary_large_image">
<meta property="twitter:url" content="https://dangerous-times.github.io/cdc/homicide.htm">
<meta property="twitter:title" content="Firearm homicides up by staggering 35% in 2020 according to CDC data">
<meta property="twitter:description" content="All Homicides up by 30% in 2020 for a total of 24,576! Black male homicide reached 59 per 100K black males while white male homicide was a mere 4 per 100K white males. Per capita, that's 18X! Look at the graphs and CDC data to see for yourself.">
<meta property="twitter:image" content="https://dangerous-times.github.io/cdc/social_media_photo1.png">

''')

  write_data('<meta name="AUTHOR" content="','<meta name="AUTHOR" content="')
  pos = input.find('"',pos)    # delete text
  write_data('<meta name="CHANGEDBY" content="','<meta name="CHANGEDBY" content="')
  pos = input.find('"',pos)    # delete text
  
  write_data("<style>","<!-- <style> -->")  #remove style
  write_data("</style>","<!-- </style>  -->")

  write_data("<body","<body")
  write_data(">",'''>

<a name="top"></a><br/>

<div style="position: fixed; top: 0px; left: 0px; background-color: white;">
	&nbsp;
	<a style="background-color: lightgreen;" href="#top">return to top</a> &nbsp; &nbsp;
	<a id="h1" style="background-color: lightgreen;" href="homicide.htm" >Display homicide graphs</a> &nbsp; &nbsp
	<a id="h2" style="background-color: lightgreen;" href="homicide_cdc_original.htm">Display original CDC homicide data</a> &nbsp; &nbsp;
	<a style="background-color: lightgreen;" href="homicide.ods">Download graph & CDC data spreadsheet</a>
</div>

<script>
  if (document.location.pathname.substr(-12) == "homicide.htm") {
    document.getElementById("h1").style.display = "none";
  } else {
	document.getElementById("h2").style.display = "none";	
  }
</script>

''')

  outfile1.write("<p></p><h1>Graphs of USA homicides</h1>\n")
  outfile2.write("<p></p><h1>Original CDC data</h1>\n")

  write_data("<center>","<!-- removed <center> -->")

  end_center = input.find("</center>",pos)
  overview = input[pos:end_center].lower().split("#")   # <a href=#xxxx
  del overview[0]  # Get rid of leading <a info"
  pos = end_center    # past </center>
  byage = []
  per100k = []
  homicides = []
  unknown = []
  original = []
  sheet_count = len(overview)
  
  while len(overview):
    html_a = overview.pop(0)
    html_a = '<a style="background-color: lightgreen;" href="#' + html_a[:html_a.find("</a>")+4]

    if html_a.find("original") >= 0:
      original.append(html_a) 

    elif html_a.find("by age") >= 0:
      html_a = html_a.replace("by age","")
      byage.append(html_a) 

    elif html_a.find("per 100k") >= 0:
      html_a = html_a.replace("per 100k","").replace("homicides","").replace("homicide","").replace("> <",">all usa<")
      per100k.append(html_a) 

    elif html_a.find("homicide") >= 0:
      html_a = html_a.replace("homicides","").replace("homicide","").replace("><",">all usa<")
      homicides.append(html_a) 

    else: 
      unknown.append(html_a)

  outfile1.write("\n<p>Graphs homicides per 100K: \n")
  outfile1.write(" &nbsp; \n".join(per100k))
    
  outfile1.write("\n<br/>\nGraphs homicides: \n")
  outfile1.write(" &nbsp; \n".join(homicides))

  outfile1.write("\n<br/>\nGraphs by age: \n")
  outfile1.write(" &nbsp; \n".join(byage))

  if len(unknown) != 0: 
    outfile1.write("\n</p>\n--problem graphs: \n")
    outfile1.write(" &nbsp; \n".join(unknown) + "\n</p>\n")

  outfile1.write("\n</p>\n")

  outfile2.write("<br/>\n".join(original) + "<br/>\n") 

  write_data("<h1>Overview</h1>","<h1>Firearm homicides up by staggering 35% in 2020 <br/>according to CDC data</h1>\n")

  outfile1.write('''
                <p>All Homicides up by 30% in 2020 for a total of 24,576! Black male homicide reached 59 per 100K black males while white male homicide was a mere 4 per 100K white males. Per capita, that's 18X! Look at the graphs and CDC data to see for yourself. </p>

                <p>California proves that strict gun laws do NOT prevent gun violence. California has a high firearm homicide rate despite difficulties in purchasing firearms and munitions along with severely restricting your ability to access them. See <a target="_blank" href="https://oag.ca.gov/firearms/travel">transporting firearms in California at https://oag.ca.gov/firearms/travel</a>) which infers your firearm will rarely be legally with you.</p>

                <p>CDC WONDER was used to extract the following graphs and data.
                E.g. saved CDC firearm homicide report <a target="_blank" href="https://wonder.cdc.gov/controller/saved/D158/D293F524">https://wonder.cdc.gov/controller/saved/D158/D293F524</a></p>

                 <p>The exported CDC data was reformatted using python program <a href="cdc_to_graph.py" target="_blank">cdc_to_graph.py</a>. The CDC exported file name is specified as a parm. The program generates 2 files (per 100K & simple reformat.</p>

                 <p>The 2 reformatted CDC data files are inserted to openoffice calc spreadsheets and I generated charts from each. I also inserte the original CDC files for each.
                  </p>
 
                  <p>You can download my OpenOffice spreadsheet dataset <a target="_blank" href="homicide.ods">homicide.ods</a>.</p>

                  <p>You may scroll through all the graphs and data below. Or alternatively you can go to a specific graph and data by click one of the following links: </p>
''')

  write_data("</center>","<!-- removed </center> -->")

  write_data("<hr>","<hr>")

  while write_data("./homicide_files/", "./", "file1") != -1:
    "Remove directory from all graph <img> files"

  first_original_cdc_sheet_pos = input.find("table" + str(sheet_count-len(original)), pos)
  first_original_cdc_sheet_pos = input.rfind("<!--",0,first_original_cdc_sheet_pos)
  outfile1.write(input[pos:first_original_cdc_sheet_pos])
  pos = first_original_cdc_sheet_pos
  write_data("</body>","","file2")
  pos -= 7    # point to being of </body>

  outfile1.write(input[pos:])
  outfile1.close()
  outfile2.write(input[pos:])
  outfile2.close()