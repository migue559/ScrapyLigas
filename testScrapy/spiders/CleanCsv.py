import os
import sys
import csv


def CleanCsv(a,b,c):
    path="/Users/MIGUEL/Documents/Sublime/python/FIFA/testScrapy/"
    pais=a
    liga="ligaMx_"
    temp=c
    print("SIIII")
    print(path+a+liga+c+".csv")
    try:
        file_object = open(path+a+liga+c+".csv","r")
        lines = csv.reader(file_object, delimiter=',')
        flag = 0
        data=[]
        for line in lines:
            if line == []:
                flag =1 # etiqueta las lineas vacias del csv                 
                continue
            else:
                data.append(line)
        file_object.close()
        if flag ==1: #if blank line is present in file
            file_object = open(path+a+liga+c+".csv", 'w')
            for line in data:
                str1 = ','.join(line)
                
                
                file_object.write(str1+"\n")
            file_object.close() 
        print("Se ha realizado la limpieza de lineas vacias")
    except (Exception,e):
        print ("Error")    

if __name__ == "__main__":
    a = str(sys.argv[1])
    b = str(sys.argv[2])
    c = str(sys.argv[3])
    print("Este es el contenido de clean csv __a:"+a +"__b:"+b +"__c:"+c)
    CleanCsv(a,b,c)
   

