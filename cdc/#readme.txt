Information on building the CDC graphs

1. Use http://wonder.cdc.com to download additional CDC data. Look at the bottom of an original tables to see a sample selection criteria used. It will be highlighted in green.

2. Name the downloaded CSV such that the first 2 characters are used for sorting in the menu. Follow it by "original cdc" and a descriptive name to be used in the menu.

3. Run cdc_to_graph.py to load create new graph_xxx.csv files from the CDC data you downloaded.

4. Open a new OpenOffice Calc spreadsheet. Copy the OpenOffice_macros.bas into the macro's and run it. It will automaticall load all the CSV files and make the required changes. 

5. Make any changes you want to the spreadsheets to be displayed on the web page. E.g. the first 5 rows are selected to display in the graph. Remove the background color from column 1 for lines you don't want displayed and add a background color in column 1 for lines you want displayed by default.

6. Save the spreadsheets. 

7. Display the spreadsheets as a web page. Do this by clicking on file and select display as webpage option. 

8. After the web page opens, use your browsers "save as" to save the HTML. Once complete, close Openoffice Calc and the browser page showing the spreadsheets.

9. Run cdc_html_rework.py which will prompt you for the HTML you created in the previous step. Simply specify the number of the HTML file you created.

10. Make these files available thru a web server because they local files won't work because of security restrictions. E.g python has a sample webserver started by "py -m http.server 80" and you access in your web browser using http://localhost/homicide.htm.

