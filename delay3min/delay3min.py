#-------------------------------------------------------------------------------
# Name:        CSV Import From Zonar
# Author:      Rich Buford & Jeff King
# Created:     01/03/2017
# Copyright:   (c) richbuford 2017
#-------------------------------------------------------------------------------

import csv
import time
import datetime
import urllib
import os
import shutil
import sys
import xml.etree.ElementTree as ET

#The function that is looped by the program.
#This is given one thread each cycle, while the gui also gets one thread each cycle

#To recompile this file, navigate to C:\atlas_shared\AVL\ZonarHistoricalCSV in windows command prompt
#Ensure that you stop the Zonar service in windows services

pathTo = "C:\\atlas_shared\\AVL\\ZonarHistoricalCSV\\delay3min\\"

def looper():
    try:
        global pathTo
        runlog = open(pathTo + "runtime.log", "w+")
        timeDelay = 60*3
        timeWindow = 10
        prev_time_file = pathTo + "prev_time.log"
        try:
            lookupxml = pathTo + "lookupxml.xml"
            xml_url = "https://col2225.zonarsystems.net/interface.php?action=showopen&operation=showassets&username=gisadmins&password=admin1234&format=xml"
            urllib.urlretrieve(xml_url, lookupxml)
            tree = ET.parse(lookupxml)
            root = tree.getroot()
            lookuploc = {}
            lookupstype = {}
            for member in root.findall('asset'):
                fleet = member.find('fleet').text
                location = member.find('location').text
                subtype = member.find('subtype').text
                lookuploc[fleet] = location
                lookupstype[fleet] = subtype
        except Exception as e:
            writeError("Failed creating lookup table at {1}: {0}\n".format(str(e), str(time.time())))

        endtime = int(time.time() - timeDelay)
        try:
            prev_time = open(prev_time_file, "r+")
            liner = prev_time.readline()
            if(liner == "" or liner == "\n"):
                starttime = endtime - timeWindow
            else:
                starttime = int(liner)
            prev_time.close()
        except:
            starttime = endtime - timeWindow

        tstarttime = str(starttime)
        tendtime = str(endtime)

        try:
            next_time = open(prev_time_file, "w+")
            next_time.write(str(endtime+1))
            next_time.close()
        except Exception as e:
            writeError("Failed opening prev_time log at {1}: {0}\n".format(str(e), str(time.time())))

        start = int(time.time())

        req_list = {"action": "showposition",
        "logvers": "3.6",
        "username": "gisadmins",
        "password": "admin1234",
        "operation": "path",
        "format": "csv",
        "version": "2",
        "starttime": tstarttime,
        "endtime": tendtime}

        #WaterLight
        try:
            wlname = "ZonarWaterLight" + tendtime
            wlout1 = pathTo + "WaterLight\\Temp\\" + wlname + "_1" + ".csv"
            wlout2 = pathTo + "WaterLight\\Temp\\" + wlname + "_2" + ".csv"
            wlout3 = pathTo + "WaterLight\\Temp\\" + wlname + "_3" + ".csv"
            wlout4 = pathTo + "WaterLight\\Temp\\" + wlname + "_4" + ".csv"
            wlout5 = pathTo + "WaterLight\\Temp\\" + wlname + ".csv"
            wlout = pathTo + "WaterLight\\" + wlname + "" + ".csv"

            req_list["location"] = "Electric Distribution"
            req_params = urllib.urlencode(req_list)
            wlurl1 = "http://col2225.zonarsystems.net/interface.php?%s" % req_params

            req_list["location"] = "Electric Utility Services"
            req_params = urllib.urlencode(req_list)
            wlurl2 = "http://col2225.zonarsystems.net/interface.php?%s" % req_params

            req_list["location"] = "Water Distribution"
            req_params = urllib.urlencode(req_list)
            wlurl3 = "http://col2225.zonarsystems.net/interface.php?%s" % req_params

            req_list["location"] = "Water Light Engineering"
            req_params = urllib.urlencode(req_list)
            wlurl4 = "http://col2225.zonarsystems.net/interface.php?%s" % req_params

            urllib.urlretrieve(wlurl1, wlout1)
            urllib.urlretrieve(wlurl2, wlout2)
            urllib.urlretrieve(wlurl3, wlout3)
            urllib.urlretrieve(wlurl4, wlout4)

            f = wlout1
            csvinputs = [wlout3, wlout2, wlout4]
            appendCsvs(f, csvinputs, wlout5)
            writeToOutput(wlout5, wlout, lookuploc, lookupstype)
            os.remove(wlout1)
            os.remove(wlout3)
            os.remove(wlout2)
            os.remove(wlout4)
            os.remove(wlout5)
            runlog.write("WaterLight Imported\n")
        except Exception as e:
            writeError("Failed Waterlight at {1}: {0}\n".format(str(e), str(time.time())))
        #End WaterLight

        #Sewer
        try:
            sewername = "ZonarSewer" + tendtime
            sewerout1 = pathTo + "Sewer\\Temp\\" + sewername + "" + ".csv"
            sewerout = pathTo + "Sewer\\" + sewername + "" + ".csv"

            req_list["location"] = "Sewer and Stormwater - WWTP"
            req_params = urllib.urlencode(req_list)
            sewerurl = "http://col2225.zonarsystems.net/interface.php?%s" % req_params

            urllib.urlretrieve(sewerurl, sewerout1)
            writeToOutput(sewerout1, sewerout, lookuploc, lookupstype)
            runlog.write("Sewer Imported\n")
            os.remove(sewerout1)
        except Exception as e:
            writeError("Failed Sewer at {1}: {0}\n".format(str(e), str(time.time())))
        #End Sewer

        #Street
        try:
            streetname = "ZonarStreet" + tendtime
            streetout1 = pathTo + "Street\\Temp\\" + streetname + "_1" + ".csv"
            streetout2 = pathTo + "Street\\Temp\\" + streetname + "_2" + ".csv"
            streetout3 = pathTo + "Street\\Temp\\" + streetname + "_5" + ".csv"
            streetout4 = pathTo + "Street\\" + streetname + "" + ".csv"

            req_list["location"] = "Street - Grissum"
            req_params = urllib.urlencode(req_list)
            streeturl1 = "http://col2225.zonarsystems.net/interface.php?%s" % req_params

            req_list["location"] = "Street Sweepers - Grissum"
            req_params = urllib.urlencode(req_list)
            streeturl2 = "http://col2225.zonarsystems.net/interface.php?%s" % req_params

            urllib.urlretrieve(streeturl1, streetout1)
            urllib.urlretrieve(streeturl2, streetout2)

            fstreets = streetout1
            streetinputs = [streetout2]
            appendCsvs(fstreets, streetinputs, streetout3)
            writeToOutput(streetout3, streetout4, lookuploc, lookupstype)
            os.remove(streetout1)
            os.remove(streetout2)
            os.remove(streetout3)
            runlog.write("Streets Imported\n")
        except Exception as e:
            writeError("Failed Street at {1}: {0}\n".format(str(e), str(time.time())))
        #End Street

        #Solid Waste
        try:
            solidwastename = "ZonarSolidWaste" + tendtime
            solidout1 = pathTo + "SolidWaste\\Temp\\" + solidwastename + "" + ".csv"
            solidout = pathTo + "SolidWaste\\" + solidwastename + "" + ".csv"

            req_list["location"] = "Solid Waste - Grissum"
            req_params = urllib.urlencode(req_list)
            solidurl = "http://col2225.zonarsystems.net/interface.php?%s" % req_params

            urllib.urlretrieve(solidurl, solidout1)
            writeToOutput(solidout1, solidout, lookuploc, lookupstype)
            os.remove(solidout1)
            runlog.write("Solid Imported\n")
        except Exception as e:
            writeError("Failed Solid Waste at {1}: {0}\n".format(str(e), str(time.time())))
        #End Solid Waste

        endtime2 = int(time.time())
        print tendtime
        print tstarttime
        timedif = endtime2-start
        print timedif

        runlog.write('It took {0} seconds.\n'.format(endtime2-start))
        runlog.close()
    except Exception as e:
        writeError("Failed main loop at {1}: {0}\n".format(str(e), str(time.time())))

#function called by looper to writeoutput for each vehicle to csvs
def writeToOutput(out, write, lookuploc, lookupstype):
    with open(out, 'rb') as fileIn:
        with open(write, 'wb') as fileOut:
            reader = csv.reader(fileIn)
            writer = csv.writer(fileOut)
            rowWriter = []
            row = reader.next()
            row.append('Location')
            row.append('Subtype')
            for x in range(0,12):
                del row[17]
            rowWriter.append(row)
            for row in reader:
                if(len(row) == 29):
                    row.append(lookuploc[row[1]])
                    row.append(lookupstype[row[1]])
                    ept = int(row[3])
                    convt = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(ept))
                    row[2] = convt
                    for x in range(0,12):
                        del row[17]
                    rowWriter.append(row)
            writer.writerows(rowWriter)
    return

def writeError(string):
    try:
        global pathTo
        errlog = open(pathTo + "errors.log", "a+")
        errlog.write(string)
        errlog.close()
        exit(1)
    except:
        exit(1)

#function called before writeToOutput in the case that there are more than one
#csv inputs that must be appended together
def appendCsvs(f, csvinputs, out):
    op = open(out, 'wb')
    output = csv.writer(op, delimiter =',')
    csvfiles = []
    op1 = open(f, 'rb')
    rd = csv.reader(op1, delimiter = ',')
    for row in rd:
        csvfiles.append(row)
    for files in csvinputs:
        op2 = open(files, 'rb')
        rd2 = csv.reader(op2, delimiter = ',')
        rd2.next()
        for row2 in rd2:
            csvfiles.append(row2)
        op2.close()
    output.writerows(csvfiles)
    op.close()
    op1.close()
    return

def main():
    global pathTo
    try:
        shutil.rmtree(pathTo + "WaterLight")
        shutil.rmtree(pathTo + "Sewer")
        shutil.rmtree(pathTo + "Street")
        shutil.rmtree(pathTo + "SolidWaste")
        os.makedirs(pathTo + "WaterLight")
        os.makedirs(pathTo + "Sewer")
        os.makedirs(pathTo + "Street")
        os.makedirs(pathTo + "SolidWaste")
        os.makedirs(pathTo + "WaterLight//Temp")
        os.makedirs(pathTo + "Sewer//Temp")
        os.makedirs(pathTo + "Street//Temp")
        os.makedirs(pathTo + "SolidWaste//Temp")
    except:
        writeError("Failed replacing directories at {1}: {0}\n".format(str(e), str(time.time())))
        exit(3)

    for x in range(1000):
        looper()
        time.sleep(5)

if __name__ == '__main__':
    main()




