def Save(data,name= "data"):
    if type(data) == str:
        with open("{}.txt".format(name),"w") as file:
            file.write(data)
    elif type(data) == list:
        with open("{}.txt".format(name),"w") as file:
            for i in data:
                file.write("{}\n".format(i))
    elif type(data) == dict:
        with open("{}.txt".format(name),"w") as file:
            for key, value in data.items(): 
               file.write('%s,%s\n' % (key, value))
    else:

        print("Plsease check the data type !!")


def SuperSaver(data,name="data.bineet"):
    import pickle
    with open(name,'wb') as f:
        pickle.dump(data,f)

def SuperRead(data):
    import pickle
    with open(data,'rb') as file:
        read_data = pickle.load(file)

    return read_data

def Read(data):
    with open(data,'r') as f:
        output = f.read()
    return output
