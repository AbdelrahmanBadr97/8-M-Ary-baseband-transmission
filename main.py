import random
import math
import numpy
# for plot graph
from  matplotlib import pyplot


#for mapper and demapper this is a symbol dictionary
mydict = {"010" : 7 ,
"011" : 5 ,
"001" : 3 ,
"000" : 1 ,
"100" : -1 ,
"101" : -3 ,
"111" : -5 ,
"110" : -7 }


num_of_symbols =1000

Eb = 1
root_E0 = math.sqrt (Eb/7)


BRE = list()
th_BRE= list()
Eb_over_N0 = range (-4 , 18 , 2)

#make required simuliation Eb/N0 form -4 to 16 and step 2
for E_N in Eb_over_N0:
    # number of wrong bits
    num_bits_err = 0
    #calculate the value of Theoretical BER
    th_BRE.append((7/24) * math.erfc(math.sqrt((1/7)* (10**(0.1*E_N)))))
    
    for i in range(num_of_symbols):
        bits=[]
        #generate random symbols each symbol is 3 bits
        for j in range(3) :
            bits.append(random.randint( 1 , 100000000 )%2)
        bits_str=''.join([str(elem) for elem in bits])
        #generat Si(t)
        st = mydict[bits_str] * root_E0

        #add noise
        N0 = 1/(10**(0.1*E_N))
        #normal function take the standard deviation
        st_noise= st + numpy.random.normal(0 , math.sqrt(N0/2) , 1)


        #demapper
        demaped = None
        if st_noise >= 6*root_E0  :
            demaped = "010"
        elif  st_noise > 4*root_E0 :
            demaped ="011"
        elif st_noise > 2*root_E0 :
            demaped = "001"
        elif st_noise > 0 :
            demaped="000"
        elif st_noise > -2 *root_E0 :
            demaped = "100"
        elif st_noise > -4 *root_E0 :
            demaped = "101"
        elif st_noise > -6*root_E0 :
            demaped = "111"
        else :
            demaped = "110"

        #check if noise change more than 1 bit ( it is rare to happen but I handle it )
        if demaped[0] != bits_str [0] :
            num_bits_err+=1
        if demaped[1] != bits_str [1] :
            num_bits_err+=1
        if demaped[2] != bits_str [2] :
            num_bits_err+=1

    #calculate Simulated BER
    BRE.append(err/(num_of_symbols*3))

#print the values
print(th_BRE )
print(BRE)
#draw the required Fig
pyplot.semilogy(Eb_over_N0 ,BRE  , linewidth = 2 , label = 'Simulated BER')
pyplot.semilogy(Eb_over_N0 ,th_BRE ,'--',linewidth = 2 ,  label = 'Theoretical BER')
pyplot.title('The simulated BER and the theoretical BER versus Eb/N0')
pyplot.xlabel('Eb/N0')
pyplot.ylabel('BER')
pyplot.legend()
pyplot.show()
