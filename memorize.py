import pandas as pd
import random
import json
import argparse
import warnings

# Get all the arguments needed for the program to run
parser = argparse.ArgumentParser(description='mem words')
parser.add_argument('-start', dest='start', default=-1, type=int, help='begin')
parser.add_argument('-end', dest='end', default=-1, type=int, help='end')

# arguments need to be determined
parser.add_argument('-wordDB', dest='file', default='GRE_2_revised.json', type=str, help='word file')
args = parser.parse_args()

# import word database
data = pd.read_json(args.file)

# list for test
unknownWords = []
allWords = []
choices = []


def insertChoice():
    count = 0
    choices.clear()
    while count < 3:  # make sure that the choices don't reoccur
        randChoice = random.choice(allWords)
        if (randChoice not in choices) and randChoice != randWord:  # if the choices repeat
            choices.append(randChoice)
            count += 1

    # insert 2 random words from the whole database
    choices.insert(random.randint(0, 4), data.content.iloc[random.randint(0, 4000)]["word"]["wordHead"])
    choices.insert(random.randint(0, 5), data.content.iloc[random.randint(0, 4000)]["word"]["wordHead"])

    insertIndex = random.randint(0, 6)  # random the index of answer
    choices.insert(insertIndex, randWord)  # insert the answer using the index above

    return insertIndex


# missing start or end argument
if (args.start == -1 or args.end == -1) or (args.start > args.end):
    warnings.warn("Please specify the start and end correctly using: -start and -end")
else:  # if there is argument
    # iterate through the words using pandas iloc by the interval user parsed
    for i in range(args.start, args.end):
        allWords.append(data.content.iloc[i]["word"]["wordHead"])
        print(i + 1, data.content.iloc[i]["word"]["wordHead"])  # print the word
        isKnownWord = input("y/n: ")
        if isKnownWord == "n":
            unknownWords.append(
                data.content.iloc[i]["word"]["wordHead"])  # append to unknownWords list, for use in the while loop
            print("added to unknown words")
        print("===============================================================================")
        print(data.content.iloc[i]["word"]["wordHead"], end=" ")  # print the word
        try:
            print("[" + data.content.iloc[i]["word"]["content"]["phone"] + "]")  # print the phonetics
        except:
            print("[" + data.content.iloc[i]["word"]["content"]["ukphone"] + "]")  # print the phonetics
        print("Meaning: " + data.content.iloc[i]["word"]["content"]["trans"][0][
            "tranOther"])  # print the meaning in english
        try:
            print("Sample Sentence: " + data.content.iloc[i]["word"]["content"]["sentence"]["sentences"][0][
                "sContent"])  # print the sample sentence
        except:
            print(
                "Sample Sentence: Failed: This entry does not have a sample sentence.")  # print if no sample sentence
        print("===============================================================================")
        print()
    if len(unknownWords) != 0:
        print("You have " + str(len(unknownWords)) + " unknown words. Let's do a test!")


while len(unknownWords) > 0:
    randWord = random.choice(unknownWords)  # choose a word from the list
    for i in range(args.start, args.end):
        if data.content.iloc[i]["word"]["wordHead"] == randWord:  # find the word in the database
            print("===============================================================================")
            print(data.content.iloc[i]["word"]["content"]["trans"][0]["tranOther"])

            insertIndex = insertChoice()

            for j in range(len(choices)):  # print all the choices
                print(str(j + 1), choices[j])
            print("===============================================================================")
            userChoice = int(input("Which word the meaning of the sentence [1-6]: "))
            if userChoice == insertIndex + 1:
                print("correct")
                unknownWords.remove(randWord)  # if correct, remove from list
            else:
                print("wrong")
            break  # step out of the for loop
