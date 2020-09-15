#! /usr/bin/python3

def getPercent():
    outfile.write('" ", "Black", "White", "Hispanic","Other"\n')
    for line in infile:

        work = line.split("Arrests: ")
        if len(work) > 1:
            work = work[1].split("<")
            newline = '"' + work[0] + '"'
            cnt = 1
        if (line.find('id="black"') != -1) or (line.find('id="white"') != -1) or (line.find('id="hispanic"') != -1) or (line.find('id="other"') != -1):
            work = line.split("ion &nbsp; ")
            work = work[1].split("%")
            newline += "," + work[0]
            cnt += 1
            if cnt == 5:
                newline += "\n"
                outfile.write(newline)

def fixData():
    for line in infile:
        if (line.find('id="black"') != -1) or (line.find('id="white"') != -1) or (line.find('id="hispanic"') != -1) or (line.find('id="other"') != -1):
            work = line.split(">",1)
            work2 = work[1].split("(",1)
            work3 = work2[1].split(")",1)
            work5 = work[0] + "> " + work3[0] +" (" +work2[0] +")"
            outfile.write(work[0] + "> " + work3[0] +" (" +work2[0] +"zz)"+work3[1])            
        else:
            outfile.write(line)

infile = open('black_lives_matter/blm_fbi_arrests_bkup1.html','r') 
outfile = open('black_lives_matter/blm_fbi_arrests.html.new','w')
getPercent()
infile.close()
outfile.close()
