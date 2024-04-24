import os
import pathlib
files = [f for f in os.listdir('.') if os.path.isfile(f)]
for f in files:
    if pathlib.Path(f).suffix == ".log":
        print(f)
        with open(f, "r") as logfile:
            params = ""
            avgtime = ""
            for x in range(7):
                if x == 0:
                    params = logfile.readline()
                    params = params.split(',')[2].strip()
                elif x == 4:
                    avgtime = logfile.readline()
                    avgtime = avgtime.split("INFO:__main__:")[1]
                elif x == 5:
                    variance = logfile.readline()
                    variance = variance.split("INFO:__main__:")[1]
                   
                logfile.readline()
            
            print(params)
            print(avgtime)
            print(variance)
             
            logfile.close()