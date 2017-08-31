import os
import sys


def CleanCsv(a,b,c):
    cmd=""
    path="/Users/MIGUEL/Documents/Sublime/python/FIFA/testScrapy/testScrapy/spiders/"
    script="CleanCsv.py"
    try:
        print("Inicia limpieza de csv :"+a+b+c)
        cmd+="python "+path
        cmd+=script
        cmd+=" "+a
        cmd+=" "+b
        cmd+=" "+c
        os.system(cmd)
        return True
    except ValueError:
        "algo va mal loco1"
        return False

def Spider(a,b,c):
    cmd=""
    try:
        cmd+="scrapy crawl jobs -a pais="+a
        cmd+=" -a temporada="+b
        cmd+=" -o "+a+"ligaMx_"+c+".csv"
        #cmd+=" > "+a+"ligaMx_"+c+".log"
        print("Inicia ejecucion de spider")
        print(cmd)
        os.system(""+cmd)        
        return True
    except:
        "Algo va mal loco2 no se puede ejecutar script"
        return False


if __name__ == "__main__":
    print ("This is the name of the script: "+ str(sys.argv[0]))
    print ("Number of arguments: "+ str(len(sys.argv)))
    print ("The arguments are: " + str(sys.argv))
    a = str(sys.argv[1])
    b = str(sys.argv[2]) 
    c=str(b[2:-5])+str(b[7:])
    Spider(a,b,c)
    #CleanCsv(a,b,c)

