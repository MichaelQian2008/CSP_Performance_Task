import pandas as pd
import random
import json
import argparse
import warnings

parser = argparse.ArgumentParser(description='mem words')
parser.add_argument('-mode', dest='mode', default="mem", type=str, help='mem: memorize words, review: review the wrong '
                                                                        'words')
parser.add_argument('-start', dest='start', default=-1, type=int, help='begin')
parser.add_argument('-end', dest='end', default=-1, type=int, help='end')
parser.add_argument('-wordDB', dest='file', default='GRE_2_revised.json', type=str, help='word file')
parser.add_argument('-userData', dest='userData', default='userData.json', type=str, help='user data file destination')
args = parser.parse_args()

# with open("GRE_2.json", "r") as f:  # 打开文件
#     data = f.readlines()  # 读取文件
#
# dictList = []
# for i in data:
#     strip = json.loads(i)
#     dictList.append(strip)
#
# with open('GRE_2_revised.json', mode='w', encoding='utf-8') as f:
#     json.dump(dictList, f)

data = pd.read_json(args.file)
unknownWords = []
allWords = []
choices = []
if args.mode == "mem":
    if (args.start == -1 or args.end == -1) or (args.start > args.end):
        warnings.warn("Please specify the start and end correctly using: -start and -end")
    else:
        for i in range(args.start, args.end):
            allWords.append(data.content.iloc[i]["word"]["wordHead"])
            print(i + 1, data.content.iloc[i]["word"]["wordHead"])
            isKnownWord = input("[y]/n: ")
            if isKnownWord == "n":
                unknownWords.append(data.content.iloc[i]["word"]["wordHead"])
                print("===============================================================================")
                print(data.content.iloc[i]["word"]["wordHead"], end=" ")
                try:
                    print("[" + data.content.iloc[i]["word"]["content"]["phone"] + "]")
                except:
                    print("[" + data.content.iloc[i]["word"]["content"]["ukphone"] + "]")
                print("Meaning: " + data.content.iloc[i]["word"]["content"]["trans"][0]["tranOther"])
                try:
                    print("Sample Sentence: " + data.content.iloc[i]["word"]["content"]["sentence"]["sentences"][0][
                        "sContent"])
                except:
                    print("Sample Sentence: Failed: This entry does not have a sample sentence.")
                print("===============================================================================")
                print("added to unknown words")
                print()

        print("You have " + str(len(unknownWords)) + " unknown words. Let's do a test!")

while len(unknownWords) > 0:
    randWord = random.choice(unknownWords)
    for i in range(args.start, args.end):
        if data.content.iloc[i]["word"]["wordHead"] == randWord:
            print("===============================================================================")
            print(data.content.iloc[i]["word"]["content"]["trans"][0]["tranOther"])
            count = 0
            choices.clear()
            while count < 3:
                randChoice = random.choice(allWords)
                if (randChoice not in choices) and randChoice != randWord:
                    choices.append(randChoice)
                    count += 1

            choices.insert(random.randint(0,4), data.content.iloc[random.randint(0,4000)]["word"]["wordHead"])
            choices.insert(random.randint(0,5), data.content.iloc[random.randint(0,4000)]["word"]["wordHead"])

            insertIndex = random.randint(0,6)
            choices.insert(insertIndex, randWord)

            for j in range(len(choices)):
                print(str(j+1), choices[j])
            print("===============================================================================")
            userChoice = int(input("Which word the meaning of the sentence: "))
            if userChoice == insertIndex+1:
                print("correct")
                unknownWords.remove(randWord)
            break
