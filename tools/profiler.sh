#/usr/bin/sh

echo "AES Profiling"

# usage: ./profiler.sh [-ep | -dp | -es | -ds] [infile] 

if [ $1 == "-ep" ]; then
    echo "______Encryption_____"
    python3 -m cProfile aestest.py -e -p $2 dummyoutfile.txt
elif [ $1 == "-es" ]; then
    echo "______Encryption_____"
    python3 -m cProfile aestest.py -e $2 dummyoutfile.txt
elif [ $1 == "-dp" ]; then
    echo "______Decryption_____"
    python3 -m cProfile aestest.py -d  -p $2 dummyoutfile.txt
elif [ $1 == "-ds" ]; then
    echo "______Decryption_____"
    python3 -m cProfile aestest.py -d $2 dummyoutfile.txt
else
    echo "Unrecognized argument to profiler"
fi

#truncate -s 4000 [file you redirected this output to]
