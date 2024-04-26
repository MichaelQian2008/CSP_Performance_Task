import pandas as pd
import random
import argparse
import warnings


parser = argparse.ArgumentParser(description='mem words')
parser.add_argument('-start', dest='start', default=-1, type=int, help='begin')
parser.add_argument('-end', dest='end', default=-1, type=int, help='end')
parser.add_argument('-wordDB', dest='file', default='GRE_2_revised.json', type=str, help='word file')
args = parser.parse_args()
data = pd.read_json(args.file)
unknownWords = []
allWords = []
choices = []
def insertChoice():
    count = 0
    choices.clear()
    while count < 3:
        randChoice = random.choice(allWords)
        if (randChoice not in choices) and randChoice != randWord:
            choices.append(randChoice)
            count += 1

    choices.insert(random.randint(0, 4), data.content.iloc[random.randint(0, 19)]["word"]["wordHead"])
    choices.insert(random.randint(0, 5), data.content.iloc[random.randint(0, 19)]["word"]["wordHead"])

    insertIndex = random.randint(0, 6)
    choices.insert(insertIndex, randWord)

    return insertIndex



if (args.start == -1 or args.end == -1) or (args.start > args.end):
    warnings.warn("Please specify the start and end correctly using: -start and -end")
else:
    for i in range(args.start, args.end):
        allWords.append(data.content.iloc[i]["word"]["wordHead"])
        print(i + 1, data.content.iloc[i]["word"]["wordHead"])
        isKnownWord = input("y/n: ")
        if isKnownWord == "n":
            unknownWords.append(
                data.content.iloc[i]["word"]["wordHead"])
            print("added to unknown words")
        print("===============================================================================")
        print(data.content.iloc[i]["word"]["wordHead"], end=" ")
        try:
            print("[" + data.content.iloc[i]["word"]["content"]["phone"] + "]")
        except:
            print("[" + data.content.iloc[i]["word"]["content"]["ukphone"] + "]")
        print("Meaning: " + data.content.iloc[i]["word"]["content"]["trans"][0][
            "tranOther"])
        try:
            print("Sample Sentence: " + data.content.iloc[i]["word"]["content"]["sentence"]["sentences"][0][
                "sContent"])
        except:
            print(
                "Sample Sentence: Failed: This entry does not have a sample sentence.")
        print("===============================================================================")
        print()
    if len(unknownWords) != 0:
        print("You have " + str(len(unknownWords)) + " unknown words. Let's do a test!")


while len(unknownWords) > 0:
    randWord = random.choice(unknownWords)
    for i in range(args.start, args.end):
        if data.content.iloc[i]["word"]["wordHead"] == randWord:
            print("===============================================================================")
            print(data.content.iloc[i]["word"]["content"]["trans"][0]["tranOther"])

            insertIndex = insertChoice()

            for j in range(len(choices)):
                print(str(j + 1), choices[j])
            print("===============================================================================")
            userChoice = int(input("Which word the meaning of the sentence [1-6]: "))
            if userChoice == insertIndex + 1:
                print("correct")
                unknownWords.remove(randWord)
            else:
                print("wrong")
            break
