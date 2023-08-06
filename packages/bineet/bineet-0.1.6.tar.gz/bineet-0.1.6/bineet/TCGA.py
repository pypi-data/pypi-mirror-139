def OrganizeData(folder_path,output_path='',name='OrganizedFile'):
    import os
    import pickle
    import re
    if output_path == '':
        output_path = folder_path
    else:
        pass
    os.chdir(folder_path)
    dirs = os.listdir()
    print(dirs)
    def extract_all(folder_path,dir):
        newfolder_path = folder_path+'/'+dir
        files = os.listdir(newfolder_path)
        os.chdir(newfolder_path)
        for file in files:
            if file.endswith('counts.gz'):
                os.system('gunzip {}'.format(file))

    def dict_maker(dict_name,folder_path,dir):
        new_folder_path = folder_path+'/'+ dir
        files = os.listdir(new_folder_path)
        os.chdir(new_folder_path)
        for file in files:
            if file.endswith('counts'):
                with open(file,'r') as f:
                    data = f.read()
                    lines = data.split("\n")
                    for line in lines:
                        if line.startswith("ENSG"):
                            parts = re.split('\s+',line)
                            if parts[0] in dict_name.keys():
                                dict_name[parts[0]].append(eval(parts[1]))
                            else:
                                new_key = {parts[0]:[eval(parts[1])]}
                                dict_name.update(new_key)

    end_dict = {}

    for dir in dirs:
        if dir.startswith("MANIFEST") or dir.endswith("tar.gz"):
            pass
        else:
            extract_all(folder_path,dir)
            dict_maker(end_dict,folder_path,dir)

    print(end_dict)

    with open('{}/{}.cbb'.format(output_path,name),'wb') as result:
        pickle.dump(end_dict,result)


def CreateDataFrame(OrganizedFilePath,outputpath='',name='DataFrame'):
    import pickle
    import os
    import pandas as pd
    if outputpath == '':
        outputpath = os.getcwd()
    else:
        pass
    with open(OrganizedFilePath,'rb') as file:
        data = pickle.load(file)

    dataframe = pd.DataFrame.from_dict(data)

    with open("{}/{}.cbb".format(outputpath,name),'wb') as file:
        pickle.dump(dataframe,file)