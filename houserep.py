#reference https://www.geeksforgeeks.org/reading-rows-from-a-csv-file-in-python/
#House of Representatives Twitter Handles found at https://pressgallery.house.gov/member-data/members-official-twitter-handles


#this file prints a list of all members of the house of representatives 
#allows user to choose which representatives they want to gather tweets on 

import csv

#creates an array of all the house of representatives twitter handles 
def getArrTwitterHandles(): 
    names_handles = [] 

    #opens file
    with open('house_of_rep.csv') as file_obj:
        reader_obj = csv.reader(file_obj)

        #adds each row to the array 
        for row in reader_obj: 
            names_handles.append(row)
    
    return names_handles

#allows user to choose which politicians they want to see 
def choosePeople(): 

    rep_twitter_handles = getArrTwitterHandles()
    count = 1
    for elem in rep_twitter_handles: 
        print(count, " ", elem[0], " ", elem[1], ": ", elem[2])
        count += 1
    print("Please enter the numbers of the senators you want to view seperated by spaces: ")
    chosenReps = input()

    arrChosen = chosenReps.split(" ")
    #print(arrChosen)

    handlesOfChosen = []
    #gets the twitter handles for which representatives the user chose 
    for e in arrChosen: 
        if e != '': 
            wantedRepIndex = int(e) - 1
            wantedRep = rep_twitter_handles[wantedRepIndex]
            handlesOfChosen.append(wantedRep)

    #print(handlesOfChosen)
    return handlesOfChosen