def info(item, z):
    size = {
        1: "small",
        2: "medium",
        3: "large",
        4: "large bottle"
    }
    
    item_deduct = {
        "small": -3,
        "medium": -6,
        "large": -8,
        "large bottle": -10
    }
    
    item_con = {
        "PB": "plastic bag",
        "J": "jar",
        "CB": "cardboard box",
        "CC": "cardboard carton",
        "LB": "large bottle"
        }
    
    item_info = {
        #Order is (item: container, size, if it's cold or not, how much to deduct) 
        "Bread": [item_con["PB"], size[2], False, item_deduct[size[2]]],
        "Glop": [item_con["J"], size[1], False, item_deduct[size[1]]],
        "Granola": [item_con["CB"], size[3], False, item_deduct[size[3]]],
        "Ice Cream":[item_con["CC"], size[2], False, item_deduct[size[2]]],
        "Potato Chips":[item_con["PB"], size[2], False, item_deduct[size[2]]],
        "Soda":[item_con["LB"], size[4], False, item_deduct[size[4]]]
    }
    if z == "info":
        return [item_deduct["small"], item_deduct["medium"], item_deduct["large"],
                item_deduct["large bottle"]]
    else:
        return item_info[item]
    
def check_out(items):
    print("Please enter the corresponding number for your order:")
    y = 1
    chosen_items=[]
    for x in range(0,len(items)):
        print("{}: {}".format(x, items[x]))
    while y != -1:
        y= int(input("Choose the number for your respective item (Enter -1 to finish): "))
        if y == -1:
            pass
        else:
            chosen_items.append(items[y])
    suggestions(chosen_items, items)
    return chosen_items

def suggestions(GL, items):
    if items[4] in GL:
        print("I see you have {}. Would you like to add {} to your purchases?"
              .format(items[4].lower(), items[5].lower()))
        x = input("Y for yes, N for no: ").lower()
        if x == 'y':
            GL.append(items[5])

def check_list(size, items, choice):
    if choice == "size":
        for x in items:
            temp = info(x, "")
            if temp[1] == "small":
                size[0] += 1
            elif temp[1] == "medium":
                size[1] += 1
            elif temp[1] == "large":
                size[2] += 1
            elif temp[1] == "large bottle":
                size[3] += 1
        return size
    else:
        temp1 = []
        for x in items:
            temp = info(x, "")
            temp1.append(temp[3])
        return temp1

def bagging(items):
    BAG_SIZE= 30
    bag_amount= []
    FROZEN_AMOUNT = 18
    #FSL = Frozen Slot Left
    FSL = FROZEN_AMOUNT
    frozen_bags= 0
    isAdded= False
    temp = []
    #This will be a list for what went in each bag
    bags = []
    #Permenate Size Deduction array
    PSD = []
    #This will corespond to how many small, medium, large, large bottles are in a list
    size= [0, 0, 0, 0]
    GL_deduct = []
    #while (len(items) != 0):
    PSD = info(items, "info")
    size = check_list(size, items, "size")
    GL_deduct = check_list(size, items, "")
    bag_amount = base_bags(items, GL_deduct, size, BAG_SIZE, PSD)
    while size[3] != 0 or size[2] != 0 or size[1] !=0 or size[0] !=0:
        if size[3] > 0:
            bag_amount.append(BAG_SIZE-abs(PSD[3]))
            q = items.index("Soda")
            items.pop(q)
            GL_deduct.pop(q)
            size[3] -= 1
        if items.count("Ice Cream") > 0:
            frozen_bags += 1
            while items.count("Ice Cream") > 0:
                FSL -= abs(PSD[1])
                size[1] -= 1
                q = items.index("Ice Cream")
                items.pop(q)
                GL_deduct.pop(q)
                if FSL == 0:
                    FSL = FROZEN_AMOUNT
                    frozen_bags += 1
        if size[2] > 0:
            a = False
            while a != True:
                if size[2] == 0:
                    a == True
                    break
                for x in bag_amount:
                    if x >= 8:
                        x -= Bag_Large_Items(x, items, GL_deduct, PSD)
                        size[2] -= 1
                        break
        if PSD[1] in GL_deduct and PSD[0] in GL_deduct:
            a = False
            isNewBag = True
            while a!= True:
                if size[0] == 0 or size[1] == 0:
                    a == True
                    break
                for x in bag_amount:
                    if x >= 10:
                        x = conflict_resolution(x, GL_deduct, size, PSD, items)
                        isNewBag = False
                        break
                if isNewBag == True:
                    bag_amount.append(BAG_SIZE)
                    bag_amount[-1] = conflict_resolution(bag_amount, GL_deduct, size, PSD, items)
        if size [1] > 0:
            a = False
            while a != True:
                if size[1] == 0:
                    a == True
                    break
                for x in bag_amount:
                    if x >= 6:
                        x -= Bag_Med_Items(x, items, GL_deduct, PSD)
                        size[1] -= 1
                        break
        if size [0] > 0:
            a = False
            while a != True:
                if size[0] == 0:
                    a == True
                    break
                for x in bag_amount:
                    if x >= 3:
                        x -= Bag_Small_Items(x, items, GL_deduct, PSD)
                        size[0] -= 1
                        break
    print(bag_amount)

def Bag_Large_Items(BS, GL, deduct, PSD):
    remaining = 0
    if len(GL) == 1:
        x = 0
        if deduct[x] == PSD[0]:
           GL.pop(x)
           deduct.pop(x)
           remaining = BS-abs(PSD[0]) 
    else:
        for x in range(0, len(GL)-1):
            if deduct[x] == PSD[2]:
                GL.pop(x)
                deduct.pop(x)
                remaining = BS-abs(PSD[2])
                break
    return remaining

def Bag_Med_Items(BS, GL, deduct, PSD):
    remaining = 0
    if len(GL) == 1:
        x = 0
        if deduct[x] == PSD[1]:
           GL.pop(x)
           deduct.pop(x)
           remaining = BS-abs(PSD[1]) 
    else:
        for x in range(0, len(GL)-1):
            if deduct[x] == PSD[1]:
                GL.pop(x)
                deduct.pop(x)
                remaining = BS-abs(PSD[1])
                break
    return remaining

def Bag_Small_Items(BS, GL, deduct, PSD):
    remaining = 0
    if len(GL) == 1:
        x = 0
        if deduct[x] == PSD[0]:
           GL.pop(x)
           deduct.pop(x)
           remaining = BS-abs(PSD[0]) 
    else:
        for x in range(0, len(GL)-1):
            if deduct[x] == PSD[0]:
                GL.pop(x)
                deduct.pop(x)
                remaining = BS-abs(PSD[0])
                break
    return remaining

def conflict_resolution(BS, item_size, size, PSD, GL):
    a = item_size.index(PSD[0])
    b = item_size.index(PSD[1])
    GL.pop(a)
    GL.pop(b)
    item_size.pop(a)
    item_size.pop(b)
    BS -= abs(PSD[0])
    BS -= abs(PSD[1])
    size[1] -= 1
    size[0] -= 1
    return BS

def base_bags(GL, deduct, size, BS, PSD):
    baseBags = []
    if size[3] >= 2:
        size[3] -= 2
        BS -= abs(PSD[3]*2)
        GL.remove("Soda")
        GL.remove("Soda")
        deduct.remove(PSD[3])
        deduct.remove(PSD[3])
        baseBags.append(BS)
    return baseBags

#This the start of the packing robot
#This is the list of items that are able to be bought
items = ["Bread", "Glop", "Granola", "Ice Cream", "Potato Chips", "Soda"]
#This is the list of the shoper
#print(checkout.count("Soda"))
checkout = check_out(items)
bagging(checkout)