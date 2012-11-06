from crn import *

start = findDate("05/01/2010 00:00")
end = findDate("09/01/2010 00:00")
stations = findStation("Monahans")
station_name = "Monahans"
#stations = findStations("Sioux Falls","Elgin")
#stations = findStations("Elgin","Tucson","Paul","Alsworth")
#stations = findStations("Elgin","Tucson","Yuma","Williams","Mercury","Sioux Falls","Socorro","Muleshoe","Oakley","Des Moines","Bowling Green","Coshocton","Durham")
#stations = getAllStations()  #Get all stations
els_5min = findElements("Geonor precip for 5 minutes")
OnsetPrecip_els = findElements("Geonor precip for 5 minutes","Geonor wire 1 depth","Geonor wire 2 depth","Geonor wire 3 depth","wetness sensor channel 1")
#els_1hr = findElements("precip","TB/d/d")


current_date = start
subhourly_minutes = ["05","10","15","20","25","30","35","40","45","50","55","60"]    #A list of subhourly 5 minute intervals (used to pull subhourly wire depths based on elementId)
precip_within_2hrs = 0            #Indicating the start of precipitation (zero when no precip has been calculated over the last two hours)
no_precip_counter = 0            #Counts the number of five minute periods with no rainfall
size_of_5min_Smoothing = 5

#Loop over the entire preiod
while current_date.getDatetimeId() < end.getDatetimeId():
    #Processing analysis period in two hourly subperiods (required because pulling all subhourly data at once from database exceeds it's querying limitations)
    subperiod_st = current_date                        #Start of subperiod to analyze
    subperiod_ed = current_date.add(1)                    #End of subperiod to analyze
    print"Processing hours ",subperiod_st.toString()," and ",subperiod_ed.toString()
    
    #Get data from database and process
    five_min_data = getData(stations,(subperiod_st,subperiod_ed),els_5min)    #Pull subhourly data for the subperiod
    current_subperiod_hour = subperiod_st    #Identifer for subperiod's hour being processed

    #Loop over the two hours
    for k in range (2):
        if no_precip_counter >= 23 and precip_within_2hrs == 1:
            precip_within_2hrs = 0
        subhourly_loop_counter = 1
        #print "Processing current subperiod hour: ",current_subperiod_hour.toString()
        for i in subhourly_minutes:    #Loop over the subhourly intervals
            #print "Processing minute: ",i
            #print "5 min periods with no precipitation: ",no_precip_counter
            if sum(five_min_data.forElement("P5_" + str(subhourly_loop_counter)).forDatetime(current_subperiod_hour.getDatetimeId())) > 0 :    #If precipitation was calaculated
                #print "5-min precipitation was calculated at ",i,"th minute for ",current_date.getDatetime0_23()
                print "Precipitation was observed: ",sum(five_min_data.forElement("P5_" + str(subhourly_loop_counter)).forDatetime(current_subperiod_hour.getDatetimeId()))
                #print "None Precip counter and precip flag were: ",no_precip_counter," ",precip_within_2hrs
                
                #Check to see if it had already precipitated within the last two-hours
                if precip_within_2hrs == 0: 
                    print "*****************************START OF PRECIPITATION EVENT****************************"
                    #Pull wire data, precip, and wetness values during the three-hours prior and 1 hour after the onset of precipitation
                    Onset_precip_date = current_subperiod_hour.add(1)        #Add an additional hour after the onset of precipitation
                    twoHrprior_Onset_precip_date = Onset_precip_date.previous()    #Pull wire data three hours before the onset of precipitation (-1)
                    twoHrprior_Onset_precip_date = twoHrprior_Onset_precip_date.previous()    #Roll back second hour (-2)
                    twoHrprior_Onset_precip_date = twoHrprior_Onset_precip_date.previous()    #Roll back third hour to esure the entire dry 2 hour period is captured (-3)
                    onset_precip_data = getData(stations,(twoHrprior_Onset_precip_date,Onset_precip_date),OnsetPrecip_els)
                    current_onsetPrecip_date = twoHrprior_Onset_precip_date        #Current processing hour
                    counter = 1
                    Onset_values_list = []
                    Onset_values_list.append("AAAStation,Date,minute,Depth1,Depth2,Depth3,Wetness,CalcPrcip")
                    while current_onsetPrecip_date.getDatetimeId() <= Onset_precip_date.getDatetimeId():    #Loop through all hours during this period ~three hours
                        counter = 1        #Reset counter for each hour
                        for j in subhourly_minutes:    #Loop through the subhourly intervals
                            #Pull subhourly values individually
                            cur_D1 = sum(onset_precip_data.forElement("D1"+j).forDatetime(current_onsetPrecip_date.getDatetimeId()))
                            cur_D2 = sum(onset_precip_data.forElement("D2"+j).forDatetime(current_onsetPrecip_date.getDatetimeId()))
                            cur_D3 = sum(onset_precip_data.forElement("D3"+j).forDatetime(current_onsetPrecip_date.getDatetimeId()))
                            cur_wet = sum(onset_precip_data.forElement("WET1"+j).forDatetime(current_onsetPrecip_date.getDatetimeId()))
                            cur_precip = sum(onset_precip_data.forElement("P5_"+str(counter)).forDatetime(current_onsetPrecip_date.getDatetimeId()))
                            counter = counter + 1
                            #Store subhouly values in list and output to textfile
                            subhourly_valuestring = str(stations.name) + "," + str(current_onsetPrecip_date.toString()) + "," + str(j)+"min,"
                            subhourly_valuestring = subhourly_valuestring + str(cur_D1) + "," + str(cur_D2) + "," + str(cur_D3) + "," + str(cur_wet) + "," + str(cur_precip)
                            Onset_values_list.append(subhourly_valuestring)
                        #End of for loop
                        current_onsetPrecip_date = current_onsetPrecip_date.add(1)    #Increment to the next hour
                    #End of while loop
                    printfile(station_name+"_"+str(current_onsetPrecip_date.getMonth())+"_"+str(current_onsetPrecip_date.getDay())+"_"+str(current_onsetPrecip_date.getYear())+".txt",Onset_values_list)
                no_precip_counter = 0
                precip_within_2hrs = 1
            else:
                #print"No precipitation was calculated at ",i," for date ",current_subperiod_hour.getDatetime0_23()
                no_precip_counter = no_precip_counter + 1
            subhourly_loop_counter = subhourly_loop_counter + 1    #Increment the subhourly loop counter
        current_subperiod_hour = current_subperiod_hour.add(1)
    current_date = current_date.add(2)
