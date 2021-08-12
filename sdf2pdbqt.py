#!/usr/bin/python3
# Written by Rohit Shukla (Jaypee University of Information Technology, Waknaghat, Solan).
# 12 August 2021
# Please write your suggetions for improvement at shuklarohit815@gmail.com

import os
import argparse

# Defining the variables for command line argument. Here four parameters are defined: two are required and two are optional.
if __name__ == "__main__":
    print("\n            ########################################################################## \n\
            ##                      pySDF2PDBQT convertor                           ## \n\
            ##           convert sdf to pdbqt for virtual screening                 ## \n\
            ##                      @Rohit Shukla, August, 2021                     ##  \n\
            ##             https://github.com/shuklarohit815/pySDF2PDBQT            ## \n\
            ########################################################################## \n")
    parser = argparse.ArgumentParser(description=" \
    This script will convert the sdf to pdbqt for four databases (PUBCHEM, DRUGBANK, ZINC, CHEMBL) and keep the result in the same direcory \
    in seperate SDF \n and PDBQT folder. \
    Please give sdf structure in 3D format otherwise geometry of the structure will be compromized by openbabel.")

    parser.add_argument("-l","--ligand", metavar="", required=True, help="Enter ligands file in sdf file format") 
    parser.add_argument("-d","--database", metavar="", required=True, help="Please enter Database name in Capital as it is written below. \
        The script supports four types of database currently (PUBCHEM, DRUGBANK, ZINC, CHEMBL) ")
    

    group = parser.add_mutually_exclusive_group()
    group.add_argument("-q", "--quiet", action = "store_true", help="print_quiet")
    group.add_argument("-v", "--verbose", action = "store_true", help="print_verbose")

    print("Examples:")
    print("")
    print("python sdf2pdbqt.py --ligand ligand_file.sdf --database PUBCHEM")
    print("")
    print("python sdf2pdbqt.py -l ligand_file.sdf -d PUBCHEM")
    print("")

args = parser.parse_args() # the args has all the command line variable

#Taking the value of variables in a new string variable for furthur operation
ligand_file = args.ligand
database_name =args.database

# opening the file will command for all. It will open the file and prepare the file for furthur operation
file_1 = open(f"{ligand_file}")
file_lig = file_1.readlines()
temp_count = 0
list_lig_name = []
print_current_directory = os.getcwd()
pdbqt_folder_name = ""
sdf_folder_name = ""
sdf_folder_name = (database_name+"_SDF_Ligands")

# Printing and massage to user total compounds and its list. Meanwhile preparing the folder also.
def folder():
    print(f"The directory has {len(list_lig_name)} ligands. The script will convert one by one. Please keep patience and read some research article")        
    print("")
    os.mkdir(database_name+"_SDF_Ligands")
    sdf_folder_name = (database_name+"_SDF_Ligands")
    print(sdf_folder_name)
    os.chdir(sdf_folder_name)

#This loop will create the files for each ligand and write the content in the file according to the specific string and count version.
def sdf_files():
    num = 0
    temp_count = 0
    for count1, item1 in enumerate(file_lig , 0):
        if "$$$$\n" == item1:
            one_lig_name = list_lig_name[num]
            if database_name == "PUBCHEM":
                c = open (f"CID{one_lig_name}.sdf", "w+") # It will make the file
            else:
                c = open (f"{one_lig_name}.sdf", "w+") # It will make the file
            c.writelines(file_lig[temp_count:count1]) # It will write the lines on the basis of temp_count and count from the list
            temp_count = count1+1
            num = num+1

    #It will come to home directory on the basis of variable
def pdbqt_files(list_lig_name):
    os.chdir(print_current_directory)
    # converting the ligand using openbabel
    os.mkdir(database_name + "_pdbqt_ligands") # please take the input from user
    pdbqt_folder_name = (database_name +"_pdbqt_ligands")
    print(pdbqt_folder_name)
    for  count, temp_lig_name in enumerate(list_lig_name, 1):
        if database_name == "PUBCHEM":
            print (f"The CID{temp_lig_name} with number {count} is converting using ObenBabel. Please cite OpenBable with this script.")
            os.system(f"obabel -isdf {sdf_folder_name}/CID{temp_lig_name}.sdf -opdbqt -O {pdbqt_folder_name}/CID{temp_lig_name}.pdbqt")
        else:
            print (f"The {temp_lig_name} with number {count} is converting using ObenBabel. Please cite OpenBable with this script.")
            os.system(f"obabel -isdf {sdf_folder_name}/{temp_lig_name}.sdf -opdbqt -O {pdbqt_folder_name}/{temp_lig_name}.pdbqt")

# For PUBCHEM database
if database_name == "PUBCHEM":
    #This loop will store all the IDs of compounds in the list_lig_name.
    for count, item in enumerate(file_lig , 0):
        if  "> <PUBCHEM_COMPOUND_CID>\n" == item:
            file_name = (file_lig[count+1]) # it will copy the below row by using count value.
            file_name = file_name.split("\n")[0] # It will copy only ID and remove space
            list_lig_name.append(file_name)

    # Calling the folder function to create the sdf file folder.
    folder()

    # Calling the SDF_file function to create the SDF files.
    sdf_files()
    
    # Calling the pdbqt_file function to create the pdbqt files.
    pdbqt_files(list_lig_name)

# For DRUGBANK database
elif database_name == "DRUGBANK": #Last ligand is not coverting

    #This loop will store all the IDs of compounds in the list_lig_name.
    for count, item in enumerate(file_lig , 0):
        if  "> <DRUGBANK_ID>\n" == item:
            file_name = (file_lig[count+1]) # it will copy the below row by using count value.
            file_name = file_name.split("\n")[0] # It will copy only ID and remove space
            list_lig_name.append(file_name)

    # Calling the folder function to create the sdf file folder.
    folder()

    # Calling the SDF_file function to create the SDF files.
    sdf_files()
    
    # Calling the pdbqt_file function to create the pdbqt files.
    pdbqt_files(list_lig_name)

# For ZINC database
elif database_name == "ZINC":

    #This loop will store all the IDs of compounds in the list_lig_name.
    for count, item in enumerate(file_lig , 0):
        if  "ZINC" in item:
            file_name = (file_lig[count]) # it will copy the below row by using count value.
            file_name = file_name.split("\n")[0] # It will copy only ID and remove space
            list_lig_name.append(file_name)
    
    # Calling the folder function to create the sdf file folder.
    folder()
    
    # Calling the SDF_file function to create the SDF files.
    sdf_files()
    
    # Calling the pdbqt_file function to create the pdbqt files.
    pdbqt_files(list_lig_name)


# For CHEMBL database
elif database_name == "CHEMBL":

    #This loop will store all the IDs of compounds in the list_lig_name.
    for count, item in enumerate(file_lig , 0):
        if  "CHEMBL" in item:
            file_name = (file_lig[count]) # it will copy the below row by using count value.
            file_name = file_name.split("\n")[0] # It will copy only ID and remove space
            list_lig_name.append(file_name)
            
    # Calling the folder function to create the sdf file folder.
    folder()

    # Calling the SDF_file function to create the SDF files.
    sdf_files()
    
    # Calling the pdbqt_file function to create the pdbqt files.
    pdbqt_files(list_lig_name)

else:
    print("DATABASE name is not correct. Please enter the database name in capital letters like PUBCHEM, DRUGBANK, ZINC, CHEMBL")
