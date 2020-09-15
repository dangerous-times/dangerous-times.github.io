#! /usr/bin/python3
import sys
import mysql.connector



table = "policeKilledByState"
table = "blacksKilledByCity"

race_table = {'Black' : 'Black',
    'Hispanic' : 'Hispanic',
    'White' : 'White'}

mydb = mysql.connector.connect(
    host="localhost",
    user="jon",
    database="police_shootings",
    passwd="465Gabilan"
    )

mycursor = mydb.cursor()




def main():
    sys.stdout.write("please enter some data: ")
    sys.stdout.flush()
    table = sys.stdin.readline()
    table = "mpvSummary\n"
    if table == "mpvSummary\n":
        mpvSummary() 
        return
    elif table == "blacksKilledByAgency\n":
        blacksKilledByAgency() 
        return
    elif table == "blacksKilledByCity":
        blacksKilledByCity() 
        return
    elif table == "policeKilledByState":
        policeKilledByState() 
        return
    elif table == "FBIarrests":
        FBIarrests() 
        return
    elif table == "allDeaths":
        allDeaths() 
        return
    elif table == "fbi":
        print("<h2>fbi report</h2>")
        sql = """
            SELECT *  
                FROM police_shootings. fbi_arrests
                limit 1000
            """
        race_table = {'B' : 'Black',
            'H' : 'Hispanic',
            'W' : 'White'}
    elif False:
        print("<h2>Unarmed or attacking deaths by race and year</h2>")
        sql = """
            SELECT race, substring(date,1,4), count(DISTINCT(`name`))  
                FROM police_shootings. washingtonPost
                where (armed like 'un%' or armed = '') and threat_level != 'attack'
                group by race, substring(date,1,4)
                limit 1000
            """
        race_table = {'B' : 'Black',
            'H' : 'Hispanic',
            'W' : 'White'}
    elif False:
        print("<h2>Unarmed not attacking deaths by race and year</h2>")
        sql = """
            SELECT race, substring(date,1,4), count(DISTINCT(`name`))  
                FROM police_shootings. mappingPoliceViolence
                where (unarmed = 'unarmed' or unarmed like 'un%' or unarmed = '') 
                    and alleged_threat_level != 'attack'
                    and substr(date,1,4) >= 2015
                group by race, substring(date,1,4)
                limit 1000
            """
    elif False:
        print("<h2>All deaths by race and year</h2>")
        sql = """
            SELECT race, substring(date,1,4), count(DISTINCT(name))  
                FROM police_shootings. mappingPoliceViolence
                where substr(date,1,4) >= 2015
                group by race, substring(date,1,4)
                limit 1000
            """


    print("<p class='hilite'>"+sql+"</p>\n")

    mycursor.execute(sql)
    myresult = mycursor.fetchall()

    if table == "fbi":
        fbi(myresult)
        exit()

    genericTable(myresult)


def mpvSummary():
    def sqlcmd(sqldata):
        print("<p class='hilmpite'>"+sqldata+"</p>\n")

        mycursor.execute(sqldata)
        myresult = mycursor.fetchall()
        return(myresult)

    def prt(cls,row):
        cAgency = ""
        cSum = ""
        if cls = "agency":
            cAgency = "class='agency'"
        elif cls = "sum":
            cSum = "class='sum'"
        print(
            "<tr "+cSum+"><td "+cAgency+">"+row[2]+" "+str(row[1])+"""</td>
             <td>"""+str(row[3])+"</td><td>"+str(row[4])+"</td><td>"""+str(row[5])+"</td><td>"+
                str(row[6])+"</td><td>"+str(row[7])+"</td><td>"+str(row[8])+"""</td>
             <td style='background-color: black;'>&nbsp;</td>
             <td>"""+str(row[10])+"</td><td>"+str(row[11])+"</td><td>"""+str(row[12])+"</td><td>"+
                str(row[13])+"</td><td>"+str(row[14])+"</td><td>"+str(row[15])+"""</td>
             <td style='background-color: black;'>&nbsp;</td>
             <td>"""+str(row[17])+"</td><td>"+str(row[18])+"</td><td>"""+str(row[19])+"</td><td>"+
                str(row[20])+"</td><td>"+str(row[21])+"</td><td>"+str(row[22])+"</td></tr>"
        )

    myresult = sqlcmd("SELECT * from mpvSummary where btotal>0 order by btotal desc, bMaxYear desc") 
    sum = ["",0,"Total agencies<br/>",0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    prtRow = 0
    for row in myresult:
        if row[8] < 5 and prtRow != row[8]:
            prt("sum",sum)
            prtRow = row[8]
            sum = ["",0,"Total agencies<br/>",0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        sum[1] += 1
        prt("agency",row)
        cnt = 3
        while cnt<=22:
            sum[cnt] += row[cnt]
            cnt += 1
    prt("sum",sum)

def blacksKilledByAgency():

    def addYear(count):
        style = ""
        if count != "":
            if count > 4:
                style = "style='background-color: pink;'"
            elif count > 1:
                style = "style='background-color: yellow;'" 
        return("<td "+style+"> &nbsp; " + str(count) + " &nbsp; </td>")

    sql = (""" 
        SELECT concat(state, ' ', city), race, substr(date,1,4), count(distinct(name))
            FROM `mappingPoliceViolence_org`
            where date>=2015 and date<=2019 and (race='Black' or race='White')
            group by concat(state, ' ', city), race, substr(date,1,4) 
    """)
    print("<p class='hilite'>"+sql+"</p>\n")

    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    myresult.append(["bad record", "bad record", 'bad record', 'bad record'])

    print("<table><tr><th>City</th><th colspan='5'>Blacks</th><th> &nbsp; </th><th colspan='5'>White</th></tr> \
        <th></th> \
        <th>2015</th><th>2016</th><th>2017</th><th>2018</th><th>2019</th> \
        <th></th> \
        <th>2015</th><th>2016</th><th>2017</th><th>2018</th><th>2019</th>")
    data = {'city': ''}
    for row in myresult:
        if data['city'] != row[0]:
            if data['city'] != '' and (data['B2015'] != '' or data['B2016'] != '' or data['B2017'] != '' or data['B2018'] != '' or data['B2019'] != ''):
                print("<tr><td> &nbsp; " + data["city"] + " &nbsp; </td>" +
                    addYear(data['B2015']) +
                    addYear(data['B2016']) +
                    addYear(data['B2017']) +
                    addYear(data['B2018']) +
                    addYear(data['B2019']) +
                    "<td></td>" +
                    addYear(data['W2015']) +
                    addYear(data['W2016']) +
                    addYear(data['W2017']) +
                    addYear(data['W2018']) +
                    addYear(data['W2019']) +
                    "</tr>" )
            data = {'city': row[0], 
                'B2015': '', 'B2016': '', 'B2017': '', 'B2018': '', 'B2019': '',
                'W2015': '', 'W2016': '', 'W2017': '', 'W2018': '', 'W2019': ''}
        data[row[1][0:1]+row[2]] = row[3]
    print("</table>")

def blacksKilledByCity():

    def addYear(count):
        style = ""
        if count != "":
            if count > 4:
                style = "style='background-color: pink;'"
            elif count > 1:
                style = "style='background-color: yellow;'" 
        return("<td "+style+"> &nbsp; " + str(count) + " &nbsp; </td>")

    sql = (""" 
        SELECT concat(state, ' ', city), race, substr(date,1,4), count(distinct(name))
            FROM `mappingPoliceViolence_org`
            where date>=2015 and date<=2019 and (race='Black' or race='White')
            group by concat(state, ' ', city), race, substr(date,1,4) 
    """)
    print("<p class='hilite'>"+sql+"</p>\n")

    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    myresult.append(["bad record", "bad record", 'bad record', 'bad record'])

    print("<table><tr><th>City</th><th colspan='5'>Blacks</th><th> &nbsp; </th><th colspan='5'>White</th></tr> \
        <th></th> \
        <th>2015</th><th>2016</th><th>2017</th><th>2018</th><th>2019</th> \
        <th></th> \
        <th>2015</th><th>2016</th><th>2017</th><th>2018</th><th>2019</th>")
    data = {'city': ''}
    for row in myresult:
        if data['city'] != row[0]:
            if data['city'] != '' and (data['B2015'] != '' or data['B2016'] != '' or data['B2017'] != '' or data['B2018'] != '' or data['B2019'] != ''):
                print("<tr><td> &nbsp; " + data["city"] + " &nbsp; </td>" +
                    addYear(data['B2015']) +
                    addYear(data['B2016']) +
                    addYear(data['B2017']) +
                    addYear(data['B2018']) +
                    addYear(data['B2019']) +
                    "<td></td>" +
                    addYear(data['W2015']) +
                    addYear(data['W2016']) +
                    addYear(data['W2017']) +
                    addYear(data['W2018']) +
                    addYear(data['W2019']) +
                    "</tr>" )
            data = {'city': row[0], 
                'B2015': '', 'B2016': '', 'B2017': '', 'B2018': '', 'B2019': '',
                'W2015': '', 'W2016': '', 'W2017': '', 'W2018': '', 'W2019': ''}
        data[row[1][0:1]+row[2]] = row[3]
    print("</table>")

def policeKilledByState():

    def byPop(count, pop):
        if count[0] == 0:
            return("<td></td>")
        if pop == 0:
            pop = 1
        return("<td> &nbsp; "+str(count[0])+" &nbsp; ( "+str(round(count[1]/pop,1))+" ) &nbsp; </td>")

    sql = (""" 
        SELECT state, substr(date,1,4), race, count(distinct(name)),
                case
                   when race='Black' then round(any_value(b)*count(distinct(name)),1)
                   when race='White' then count(distinct(name))
                   when race='Hispanic' then round(any_value(h)*count(distinct(name)),1)
                   else round(any_value(o)*count(distinct(name)),1)
                end as population 
            FROM `mappingPoliceViolence_org`
            left join kff_org_population on state=state_code 
            where date>=2015 and date<=2019
            group by state, substr(date,1,4), race 
            limit 1000 
    """)
    print("<p class='hilite'>"+sql+"</p>\n")

    mycursor.execute(sql)
    myresult = mycursor.fetchall()
    myresult.append(["end of data","bad",0,0])

    data = {"state": "", "year": "", "Black": [0,0], "White": [0,0], "Hispanic": [0,0], "Other": [0,0]}
    print("<table><td>State</td><td>year</td><td>Black</td><td>White</td><td>Hispanic</td><td>Other</td></tr>")
    year = ""
    state = ""

    for row in myresult:
        if state != row[0] or year != row[1]:
            if state != "":
                print("<tr><td> &nbsp; " + data["state"] + " &nbsp; </td>" +
                    "<td> &nbsp; " + data["year"] + " &nbsp; </td>" +
                    byPop(data["Black"], data["White"][1]) +
                    byPop(data["White"], data["White"][1]) +
                    byPop(data["Hispanic"], data["White"][1]) +
                    byPop(data["Other"], data["White"][1]) +
                    "</tr>" 
                )
            data = {"state": row[0], "year": row[1], "Black": [0,0], "White": [0,0], "Hispanic": [0,0], "Other": [0,0]}
            if state == row[0]:
                data["state"] = ""
            state = row[0]
            year = row[1]

        if row[2] in data.keys():
            data[row[2]][0] += row[3]
            data[row[2]][1] += row[4]
        else:
            data["Other"][0] += row[3]                    
            data["Other"][1] += row[4]
                    
    print("</table>")

def FBIarrests():

    sql = ("select offence,total1,total2,black,white,hispanic from `fbi_arrests`")
    print("<p class='hilite'>"+sql+"</p>\n")

    mycursor.execute(sql)
    myresult = mycursor.fetchall()

    for row in myresult:
        work = int(row[1].replace(',',''))-int(row[2].replace(',',''))
        print(row[0], 
        int(row[1].replace(',',''))-int(row[2].replace(',','')),
        int(row[1].replace(',',''))-int(row[2].replace(',',''))+int(row[3].replace(',','')),
        row[3], row[4], row[5])

def allDeaths():
    displayAllDeaths("race", "1=1") 
    displayAllDeaths("'unarmed', race, 'men'", "gender='male' and (unarmed not like 'un%' or alleged_threat_level='attack')") 
    displayAllDeaths("'armed', race, 'men'", "gender='male' and unarmed like 'un%' and alleged_threat_level!='attack'") 

def displayAllDeaths(fields, where):

    sql = ("select '<div id=""', lower(race), '""> #', " + fields + 
        " ,'per million &nbsp; (actual', round(count(distinct(name))/5), ')</div>'" + 
        " from `mappingPoliceViolence_org` where date>=2015 and date<=2019 and (" +
        where + ") group by race;")
    print("<p class='hilite'>"+sql+"</p>\n")

    mycursor.execute(sql)
    myresult = mycursor.fetchall()

    for row in myresult:
        line = ""
        for column in row:
            line += " " + str(column)
        print(line)

def genericTable(myresult):

    tab = {}
    tabsum = {}
    race = 'xxxx'

    for x in myresult:

        if x[0] != race:
            race = x[0]
            race_text = race_table.get(race, "Other")
            if race_text not in tab:
                tab[race_text] = {}
        try:
            tab[race_text][x[1]] += x[2]
        except:
            tab[race_text][x[1]] = x[2]

        try:
            tabsum[x[1]] += x[2]
        except KeyError:
            tabsum[x[1]] = x[2]

    tabsum = sorted(tabsum.items())
    tab = sorted(tab.items())

    data = "<table><tr><td> </td>"
    for year in tabsum:
        data += "<td style='text-align: center;'>" + year[0] + "</td>"
    data += "<td>total</td></tr>\n"

    for race in tab:
        sum = 0
        data += "<tr><td> "+race[0]+" </td>"
        for year in tabsum: 
            occurance = race[1].get(year[0], 0)
            data += "<td> " + str(occurance) + " <br/> " + \
            str(round(occurance / year[1] * 100)) + "% </td>"
            sum += occurance
        data += "<td> " + str(sum) + " </tr>\n "

    sum = 0
    data += "<tr><td>Total</td>"
    for year in tabsum:
        data += "<td> " + str(year[1]) + " <br/> 100% </td>"
        sum += year[1]
    data += "<td> " + str(sum) + " </td></tr>\n</table>"

    print(data)

    return()

def fbi(myresult):

    for x in myresult:

        offense = x[0]
        other = int(x[3].replace(',','')) + int(x[4].replace(',','')) + int(x[5].replace(',',''))
        white = int(x[1].replace(',',''))
        black = int(x[2].replace(',',''))
        hispanic = int(x[6].replace(',',''))
        total = other + white + black + hispanic

        print( '<div class="arrests" offense="' + offense + '"', 
            'black="'+str(black)+'"', 
            'white="'+str(white)+'"', 
            'hispanic="'+str(hispanic)+'"', 
            'other="'+str(other)+'">',
            '</div>\n'
        ) 

    return()

main()
exit



"""ALTER TABLE `fatalencounters`
add uid varchar(100) , add name varchar(100) , add age varchar(100) , add gender varchar(100) , add race varchar(100) , add race_with_imputations varchar(100) , add imputation_probability varchar(100) , add URL_of_image_of_deceased varchar(255) , add date varchar(100) , add address varchar(255) , add city varchar(100) , add Full_Address varchar(255) , add zip varchar(100) , add county varchar(100) , add unnamed1 varchar(100) , add agency_responsible varchar(100) , add Cause varchar(100) , add brief_description varchar(5000) , add Dispositions_Exclusions varchar(1000) , add Link_documentation varchar(255) , add mental_illness varchar(100) , add Video varchar(255) , add Date_and_Description varchar(1000) , add Unique_ID_formula varchar(100) , add year varchar(100)

add year varchar(100) , add county varchar(100) , add race_or_ethnicity varchar(100) , add all_deaths varchar(100) , add arrest_related_deaths varchar(100) , add in_custody_deaths varchar(100) , add population varchar(100) , add all_deaths_per_100000 varchar(100) , add arrest_related_deaths_per_100000 varchar(100) , add in_custody_deaths_per_100000 varchar(100)

add county varchar(100) , add reporting_agency varchar(100) , add agency_full_name varchar(100) , add ncic_number_county varchar(100) , add ncic_number_city varchar(100) , add ncic_number_agency varchar(100) , add date_of_birth_mm varchar(100) , add date_of_birth_dd varchar(100) , add date_of_birth_yyyy varchar(100) , add race varchar(100) , add gender varchar(100) , add custody_status varchar(100) , add custody_offense varchar(100) , add date_of_death_yyyy varchar(100) , add date_of_death_mm varchar(100) , add date_of_death_dd varchar(100) , add custodial_responsibility_at_time_of_death varchar(100) , add location_where_cause_of_death_occurred varchar(100) , add facility_death_occured varchar(100) , add manner_of_death varchar(100) , add means_of_death varchar(100)

name varchar(100) , add age varchar(100) , add gender varchar(100) , add ace varchar(100) , add URL_image_victim varchar(100) , add Date varchar(100) , add Address_Incident varchar(100) , add City varchar(100) , add State varchar(100) , add Zip varchar(100) , add County varchar(100) , add Agency varchar(100) , add Cause varchar(100) , add description varchar(100) , add Official_disposition varchar(100) , add Criminal_Charges varchar(100) , add url_news_article_or_photo_of_official_document varchar(100) , add mental_illness varchar(100) , add Unarmed varchar(100) , add Alleged_Weapon varchar(100) , add Alleged_Threat_Level varchar(100) , add Fleeing varchar(100) , add Body_Camera varchar(100) , add WaPo_ID_If_in_WaPo_database varchar(100) , add Off_Duty_Killing varchar(100) , add Geography varchar(100) , add ID
"""