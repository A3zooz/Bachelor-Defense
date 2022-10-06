# from tkinter import SOLID
import random
from re import S
import data as dt
from tabulate import tabulate
import cost_function
import neighboring
from copy import deepcopy
import Inputcreation
import Outputcreation
import json

max_generations = 80000
num_runs = 1
input_file = Inputcreation.Create_input()
# output_file = 'classes/output2.json' #lesa
cost_function = cost_function.cost
def drawschedule(f):
    u=[""]*180
    for x in range(len(f[0])):
        u[f[0][x]['Time']] += "("+ (f[0][x]['Examiner'] +" , "+ f[0][x]['Supervisor']) +")  "
    x1=["Saturday",u[0],u[1],u[2],u[3],u[4],u[5],u[6],u[7],u[8],u[9],u[10],u[11],u[12],u[13],u[14]]
    x2=["Sunday",u[15],u[16],u[17],u[18],u[19],u[20],u[21],u[22],u[23],u[24],u[25],u[26],u[27],u[28],u[29]]
    x3=["Monday",u[30],u[31],u[32],u[33],u[34],u[35],u[36],u[37],u[38],u[39],u[40],u[41],u[42],u[43],u[44]]
    x4=["Tuesday",u[45],u[46],u[47],u[48],u[49],u[50],u[51],u[52],u[53],u[54],u[55],u[56],u[57],u[58],u[59]]
    x5=["Wednesday",u[60],u[61],u[62],u[63],u[64],u[65],u[66],u[67],u[68],u[69],u[70],u[71],u[72],u[73],u[74]]
    x6=["Thursday",u[75],u[76],u[77],u[78],u[79],u[80],u[81],u[82],u[83],u[84],u[85],u[86],u[87],u[88],u[89]]
    x7=["Saturday",u[90],u[91],u[92],u[93],u[94],u[95],u[96],u[97],u[98],u[99],u[100],u[101],u[102],u[103],u[104]]
    x8=["Sunday",u[105],u[106],u[107],u[108],u[109],u[110],u[111],u[112],u[113],u[114],u[115],u[116],u[117],u[118],u[119]]
    x9=["Monday",u[120],u[121],u[122],u[123],u[124],u[125],u[126],u[127],u[128],u[129],u[130],u[131],u[132],u[133],u[134]]
    x10=["Tuesday",u[135],u[136],u[137],u[138],u[139],u[140],u[141],u[142],u[143],u[144],u[145],u[146],u[147],u[148],u[149]]
    x11=["Wednesday",u[150],u[151],u[152],u[153],u[154],u[155],u[156],u[157],u[158],u[159],u[160],u[161],u[162],u[163],u[164]]
    x12=["Thursday",u[165],u[166],u[167],u[168],u[169],u[170],u[171],u[172],u[173],u[174],u[175],u[176],u[177],u[178],u[179]]

    with open('Solution.txt', 'w') as e: 
        e.write(tabulate([x1,x2,x3,x4,x5,x6,x7,x8,x9,x10,x11,x12], headers=['Slot 1', 'Slot 2','Slot 3', 'Slot 4','Slot 5', 'Slot 6','Slot 7', 'SLot 8','Slot 9', 'Slot 10','Slot 11', 'Slot 12','Slot 13','Slot 14', 'Slot 15'], tablefmt="grid"))



def evolutionary_algorithm():
    best_timetable = None
    data = dt.load_data(input_file)
    neighbor = neighboring.neighbor  # call the neighbor function from neighboring file

    for i in range(num_runs):
        solution = dt.generate_solution(data[0],data[1],data[4],data[5],data[2],data[3],data[6])  # generate a solution by creating the first timetable by random
        flag =False
        c=0
        for j in range(max_generations):
            # change the new solution by calling the neighbor from neighboring by getteing a deepcopy from the original chromosom

            new_solution = neighbor(deepcopy(solution),flag)


            # calculate the cost for the solution
            ft = cost_function(solution)
            fti=[]
            fti = ft[0] + ft[1] + ft[2]
            # if the cost for the solution == 0 -> optimal solution (no violate of hard and soft constraint)
            if fti == 0:
                break
            # calculate the cost for the solution
            ftn = cost_function(new_solution)
            ftni = []
            ftni = ftn[0]+ftn[1]+ftn[2]
            # ---- if the cost for the new_solution less than or equal the cost solution
            # change the value of solution to new_solution ----
            if(ftni >= fti):
                c+=1
            if(c >= 2000):
                flag=True
            if(ftni < fti):
                c=0
                flag=False                
            if (ftni <= fti):
                solution = new_solution

            # print the iteration number and the cost for the current solution
            if j % 200 == 0:
                print('Iteration', j, 'cost', cost_function(solution))
            if j % 5000 == 0:
                drawschedule(solution)

        print('Run', i + 1, 'cost', cost_function(solution), 'solution', solution)
        print(cost_function(solution))
        # Soft constraint not important yet
        # if best_timetable is None or cost_function2(solution) <= cost_function2(best_timetable):
        if best_timetable is None:
            best_timetable = deepcopy(solution)

    solution = best_timetable
    # print(solution[0])

    
    """
            Soft constraint not important yet
    """
    # for j in range(3 * max_generations):
    #     new_solution = neighbor2(deepcopy(solution))
    #     ft = cost_function2(solution)
    #     ftn = cost_function2(new_solution)
    #     if ftn <= ft:
    #         solution = new_solution
    #     if j % 200 == 0:
    #         print('Iteration', j, 'cost', cost_function2(solution))
    #
    # print('Run', 'cost', cost_function2(solution), 'solution', solution)

    #dt.write_data(solution[0], output_file)

    examiner_hard = True
    supervisor_hard = True
    room_hard = True
    continued = True

    # Check hard constraints
    # for single_class in solution[0]:
    #     if len(solution[1][solution[0][i]['Examiner']][solution[0][i]['Time']]) > 1:
    #         examiner_hard = False
    # for profesor in solution[1]:
    #     for i in range(len(solution[1][profesor])):
    #         if solution[1][profesor][i] > 1:
    #             professor_hard = False
    # for ucionica in solution[2]:
    #     for i in range(len(solution[2][ucionica])):
    #         if solution[2][ucionica][i] > 1:
    #             classroom_hard = False
    # for grupa in solution[3]:
    #     for i in range(len(solution[3][grupa])):
    #         if solution[3][grupa][i] > 1:
    #             group_hard = False
                
    for i in range(len(solution[0])):             

        
        if len(solution[1][solution[0][i]['Examiner']][solution[0][i]['Time']]) > 1:
            examiner_hard = False
            # print(solution[0][i])

        if solution[2][solution[0][i]['Supervisor']][solution[0][i]['Time']] > 1:
            supervisor_hard = False
            #print(solution[0][i])

    
        # if solution[3][solution[0][i]['Room']][solution[0][i]['Time']] > 1:
        #     room_hard = False
            #print(solution[0][i])

        if len(solution[1][solution[0][i]['Examiner']][solution[0][i]['Time']]) >= 1 and solution[4][solution[0][i]['Examiner']][solution[0][i]['Time']] == 1:
            examiner_hard = False
        
    
    for Examiner in solution[1]:
        for day in range(12):
            temp = 0
            flag1=False
            for slot in range(15):
                time = day * 15 + slot
                if (len(solution[1][Examiner][time]) >= 1):
                    if (time - temp - 1 >= 2 and flag1):
                            continued=False
                            # print("Continouty violated")
                    flag1=True
                    temp = time

        
    print('Are hard restrictions for Examiner satisfied:', examiner_hard)
    print('Are hard restrictions for Supervisor satisfied:', supervisor_hard)
    # print('Are hard restrictions for Room satisfied:', room_hard)
    print('Are hard restrictions for Continouity satisfied:', continued)
    for day in range(12):
        available_rooms = deepcopy(solution[7])
        found = False
        for Examiner in solution[1]:
            for slot in range(15):
                timing = day * 15 + slot
                if solution[1][Examiner][timing] == 1 and found == False :
                    chosen_room = random.choice(available_rooms)
                    available_rooms.remove(chosen_room)
                    found = True
                    for i in range(len(solution[0])):
                        if solution[0][i]['Time'] == timing and solution[0][i]['Examiner'] == Examiner:
                            solution[0][i]['Room'] = chosen_room
                elif solution[1][Examiner][timing] == 1:
                    for i in range(len(solution[0])):
                        if solution[0][i]['Time'] == timing and solution[0][i]['Examiner'] == Examiner:
                            solution[0][i]['Room'] = chosen_room





    return solution
    
    
    


f = evolutionary_algorithm()


flagc=True
c=0

# more than 2 per slot for examiner
for Examiner in f[1]:
    flagc=True
    c=0            
    for i in range(180):
        if len(f[1][Examiner][i]) > 1:
            while(flagc):
                if(f[0][c]["Examiner"]==Examiner and f[0][c]["Time"]==i):
                    f[0][c]["Color"]="Red"
                    flagc=False
                c+=1
flagc=True
c=0 

# more than 2 per slot for supervisor           
for Supervisor in f[2]:
    flagc=True
    c=0
    for i in range(180):
        if f[2][Supervisor][i] > 1:
            while(flagc):
                if(f[0][c]["Supervisor"]==Supervisor and f[0][c]["Time"]==i):
                    f[0][c]["Color"]="Red"
                    flagc=False
                c+=1
flagc=True
c=0  
# more slots than room
for slot in range(180):
    x=0
    flagc=True
    c=0            
    for i in range(len(f[0])):
        if(f[0][i]['Time']==slot):
            x+=1
        if(x>len(f[3])):
            c=0
            while(flagc):
                if(f[0][c]["Time"]==slot):
                    f[0][c]["Color"]="Red"
                    flagc=False
                c+=1            
flagc=True
c=0 
# slot of examiner in external constraint
for Examiner in f[1]:
    l = []
    for g in f[4][Examiner]:
        if(f[4][Examiner][g]==1):
            l.append(g)
    for i in range(len(l)):
        flagc=True
        c=0  
        if len(f[1][Examiner][l[i]]) >= 1:
            while(flagc):
                if(f[0][c]["Examiner"]==Examiner and f[0][c]["Time"]==l[i]):
                    f[0][c]["Color"]="Red"
                    flagc=False
                c+=1
flagc=True
c=0 

                
#the slots of the least working day for the examiner
for Examiner in f[1]:
    working_days = 0
    min = 13
    lwday = 0
    for day in range(12):
        temp = 0        
        for slot in range(15):
            time = day*15 + slot
            if len(f[1][Examiner][time]) >= 1:
                temp +=1
            if(temp<min and temp>0):
                lwday=day
                min=temp
        if(temp>=1):
            working_days += 1
    if working_days > 2:
        u=lwday*15
        ue=lwday*15 + 15
        for k in range(len(f[0])):
            if(f[0][k]["Examiner"]==Examiner and f[0][k]["Time"]>=u and f[0][k]["Time"]<ue ):
                f[0][k]["Color"]="Red"    
                    
                    
final = json.dumps(f[0], indent=3)
jsonFile = open("Solution.json", "w")
jsonFile.write(final)
jsonFile.close()
Outputcreation.Create_output()




# for Examiner in f[1]:
#     working_days = 0
#     for day in range(12):
#         flagc=True
#         c=0            
#         for slot in range(15):
#             time = day*15 + slot
#             if len(f[1][Examiner][time]) >= 1:
#                 working_days += 1
#                 break
#         if working_days > 2:
#             while(flagc):
#                 if(f[0][c]["Examiner"]==Examiner):
#                     f[0][c]["Color"]="Red"
#                     flagc=False
#                 c+=1
