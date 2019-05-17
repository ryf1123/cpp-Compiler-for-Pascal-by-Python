
f = open("./requirement","r")
data = f.read()
f.close()

# print(data)
data_lines = data.split('\n')
currentLine = []
data_frames = []
for one_line in data_lines:
    # print(one_line)
    # print()
    if one_line == "":
        continue
    if ":" in one_line:
        # print(11)
        if currentLine != []:
            data_frames.append(currentLine)
        currentLine = []
    currentLine.append(one_line)

for one_frame in data_frames:
    # print(data_frames[0])
    print("def p_%s(p):"%one_frame[0].split(" ")[0])
    
    if len(one_frame) == 1:
        print("        '''%s'''"%one_frame[0])
    else:
        print("        '''",end='')
        for index in range(len(one_frame)):
            if index == 0:
                # print("\t\t",end="")
                print(one_frame[index])
            elif index == len(one_frame)-1:
                print("        ",end="")
                print(one_frame[index],end="")
            else:
                print("        ",end="")
                print(one_frame[index])
        # print("\t\t",end="")
        print("'''")

    # 下面试图自动给出分析树的生成代码
    # 先对只有一行的简单情况进行讨论，对终结符和非终结符的判断通过s.isupper() 完成
    if len(one_frame) == 1:
        
        one_frame_split = one_frame[0].split(" ")
        one_frame_split = [i for i in one_frame_split if i != "" and i != ":"]
        
        isLowList = [i.islower() for i in one_frame_split] 

        print("        p[0] = Node(\"%s\")"%(one_frame_split[0]), end="")
        print("([", end="")
        for index in range(len(one_frame_split)):
            if index == 0:
                continue
            else:
                if isLowList[index] == True:
                    # 如果是最后一个，或者倒数第二个（如果最后一个是终结符的话）
                    if index == len(one_frame_split)-1 or (index == len(one_frame_split)-2 and isLowList[index+1] == False):
                        print("p[%d]"%index, end="")
                    else:
                        print("p[%d], "%index, end="")
        
        print("])", end="")        

    # 如果是多行的，就同样生成，但是给if后面的表达式空出来，最后手动填写
    else:
        name_this_frame =  one_frame[0].split(" ")[0]
        for split_index in range(len(one_frame)):
            if split_index == 0: # the first ine
                print("        if p[] == '':")
                print("    ", end="")
                one_frame_split = one_frame[split_index].split(" ")
                one_frame_split = [i for i in one_frame_split if i != "" and i != ":"]
                # print(one_frame_split)
                isLowList = [i.islower() for i in one_frame_split] 

                print("        p[0] = Node(\"%s-%s\")"%(name_this_frame, one_frame_split[0]), end="")
                print("([", end="")
                for index in range(len(one_frame_split)):
                    if index == 0:
                        continue
                    else:
                        if isLowList[index] == True:
                            # 如果是最后一个，或者倒数第二个（如果最后一个是终结符的话）
                            if index == len(one_frame_split)-1 or (index == len(one_frame_split)-2 and isLowList[index+1] == False):
                                print("p[%d]"%(index), end="")
                            else:
                                print("p[%d], "%(index), end="")
                
                print("])", end="")    
                print()
            else:
                print("        elif p[] == '':")
                print("    ", end="")
                one_frame_split = one_frame[split_index].split(" ")
                one_frame_split = [i for i in one_frame_split if i != "" and i != "|"]
                # print(one_frame_split)
                isLowList = [i.islower() for i in one_frame_split] 

                print("        p[0] = Node(\"%s-%s\")"%(name_this_frame, one_frame_split[0]), end="")
                print("([", end="")
                for index in range(len(one_frame_split)):
                    if isLowList[index] == True:
                        # 如果是最后一个，或者倒数第二个（如果最后一个是终结符的话）
                        if index == len(one_frame_split)-1 or (index == len(one_frame_split)-2 and isLowList[index+1] == False):
                            print("p[%d]"%(index+1), end="")
                        else:
                            print("p[%d], "%(index+1), end="")
                

                print("])", end="")    
                print()

    print("\n\n")
