import tkinter
import tkinter.filedialog
import os
import re
import shutil
import subprocess

# input author name
authorName = input("작성자 이름: ").replace(" ", "")
# input problem name
problemName = input("문제 이름: ").replace(" ", "")
# input file path to submit
tkinter.Tk().withdraw()
absoluteFilePath = tkinter.filedialog.askopenfilename(title="제출할 파일을 선택해주세요.")
print("파일 경로: ", absoluteFilePath)
# input commit message
commitMessage = input("커밋메시지: ")

# get most recent directory
baseDirectory = "./dirs"
previousDirectories = os.listdir(baseDirectory)

directorySuffix = "주차"
directoryPatternString = "([\d]+)"+directorySuffix
directoryPattern = re.compile(directoryPatternString)

maxWeek = 1
for directory in previousDirectories:
    week = int(directoryPattern.match(directory).group(1))
    if week > maxWeek:
        maxWeek = week

# create new directory
newWeekString = "%s%s" % (maxWeek + 1, directorySuffix)
newDirectoryName = "%s/%s" % (baseDirectory, newWeekString)

check = input("폴더를 생성합니다. %s (y/n)" % (newDirectoryName))
if check != 'y':
    exit()

os.mkdir(newDirectoryName)
print("mkdir", newDirectoryName)

# create branch
newBranchName = "feature/%s(%s)-%s" % (authorName, newWeekString, problemName)

check = input("브랜치를 생성합니다. %s (y/n)" % (newBranchName))
if check != 'y':
    exit()

GIT_CHECKOUT_CMD = "git checkout -b %s" % (newBranchName)
subprocess.call(GIT_CHECKOUT_CMD.split(" "))

# move file to new directory
originalFileName = os.path.basename(absoluteFilePath)
newAbsoluteFilePath = "%s/%s" % (newDirectoryName, originalFileName)

check = input("파일을 복사합니다. %s (y/n)" % (originalFileName))
if check != 'y':
    exit()

shutil.copy(absoluteFilePath, newAbsoluteFilePath)
print("move file %s to %s" % (absoluteFilePath, newAbsoluteFilePath))

# add and commit
GIT_ADD_CMD = "git add %s" % (newAbsoluteFilePath)
subprocess.call(GIT_ADD_CMD.split(" "))

GIT_COMMIT_CMD = "git commit -m"
commitMessage = "'%s'" % (commitMessage)

GIT_COMMIT_CMD = GIT_COMMIT_CMD.split(" ")
GIT_COMMIT_CMD.append(commitMessage)

check = input("커밋메시지를 작성합니다. %s (y/n)" % (commitMessage))
if check != 'y':
    exit()

subprocess.call(GIT_COMMIT_CMD)

# push
GIT_PUSH_CMD = "git push origin %s" % (newBranchName)
subprocess.call(GIT_PUSH_CMD.split(" "))

# delete local branch
GIT_CHECKOUT_MASTER_CMD = "git checkout master"
subprocess.call(GIT_CHECKOUT_MASTER_CMD.split(" "))

GIT_DELETE_LOCAL_BRANCH_CMD = "git branch -d %s" % (newBranchName)
subprocess.call(GIT_DELETE_LOCAL_BRANCH_CMD.split(" "))