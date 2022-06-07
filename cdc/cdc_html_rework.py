with open("homicide.htm","r") as f:
  input = f.read()
  f.close()

pos = 0
def write_data(del_text,ins_text):
  global pos
  text_start = input.find(del_text,pos)
  if text_start == -1:
    return -1
  f.write(input[pos:text_start])
  pos = text_start+len(del_text)
  f.write(ins_text)

with open("homicide_files/homicide.htm","w") as f: 

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
  write_data("-->",'''

                .normal_text p {font-size:medium; max-width:7in;}
                .normal_text td,a {font-size:medium;}
        -->''')  
  write_data("<body","<body")
  write_data(">",'''>

<div class="normal_text">

''')

  write_data("<center>","<!-- removed <center> -->")

  write_data("<h1>Overview</h1>",'''
		<h1>Firearm homicides up by staggering 35% in 2020 <br/>according to CDC data</h1>

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

  while (write_data('<a href="file:','<a href="') != -1):
    pos = input.find("#",pos)  # remove qualified web address

  write_data("</center>","<!-- removed </center> -->")

  while (write_data("./homicide_files/","./") != -1):
    "remove subdirectory"

  write_data("</body>",'''

   <!-- hitwebcounter Code START -->
   <a href="https://www.hitwebcounter.com" target="_blank">
   <img src="https://hitwebcounter.com/counter/counter.php?page=7999091&style=0006&nbdigits=5&type=ip&initCount=0" title="Free Counter" Alt="web counter"   border="0" /></a>   

</body>
''')  
  f.write(input[pos:])
  f.close()