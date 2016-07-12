'''
Created on Apr 11, 2016

@author: akhila
'''
import json
import operator
import pickle
import sys

final_ans=""
#with open('hmmmodel.txt','r') as fpk:
    #final_dict=json.load(fpk)
a_dir1=sys.argv[1]
inputfile=open("hmmmodel.pkl","rb")

#anslist=[]
fp=open('hmmoutput.txt', 'w')   
final_dict=pickle.load(inputfile)
emission={}
emission=final_dict[1]
all_tags={}
all_tags=final_dict[2]
transition={}
transition=final_dict[0]
#end_tags={}
#end_tags=final_dict[3]
#print "emission",emission
#print "all_tags",all_tags
#print "transition",transition

#print "transition",transition


write_to_file=""
lines = open(a_dir1,'r').read().splitlines()
prob_matrix={}
back_point={}
for i in lines:
    a=i.split()
    prob_matrix.clear()
    back_point.clear()
    prev_state=""
    flag=False
    counter=0
    for j in a:
        counter=counter+1
        if j in emission:#checking if its a known or unknown word
            #print j
            if(flag==False):
                #m=j
                prob_matrix[counter]={}
                back_point[counter]={}
                #[counter]={}
                for m in emission[j]:
                    
                
                    prob_matrix[counter][m]=emission[j][m]*transition['qo'][m]
                   
                    back_point[counter][m]='q0'
                #prev_state=j
                flag=True
                
                    
                    #myarray[counter
            else:
                prob_matrix[counter]={}
                back_point[counter]={}
                for n in emission[j]:
                    
                    maxi=-1
                    p1=""
                    for p in prob_matrix[counter-1]:
                        t=prob_matrix[counter-1][p]*transition[p][n]*emission[j][n]
                            #t1=prob_matrix[prev_state][p]*transition[p][n]*emi_prob[j][n]
                        
                            #print "in else"
                            #t1=0
                        #print p,n,t
                        if maxi<=t:
                            maxi=t
                            p1=p
                    prob_matrix[counter][n]=maxi
                    back_point[counter][n]=p1   
                     
            #prev_state=j
        else:
            if(flag==False):
                #m=j
                prob_matrix[counter]={}
                back_point[counter]={}
                for m in all_tags:
                    #print "my m",m
                    prob_matrix[counter][m]=transition['qo'][m]
                    back_point[counter][m]='q0'
                #prev_state=j
                flag=True
                
                
            else:
                prob_matrix[counter]={}
                back_point[counter]={}
                for n in all_tags:#emission[j]:
                    maxi=-1
                    p1=""
                    for p in prob_matrix[counter-1]:
                        t=prob_matrix[counter-1][p]*transition[p][n]
                        #t1=prob_matrix[prev_state][p]*transition[p][n]*emi_prob[j][n]
                        #print "in else"
                        #t1=0
                        #print p,n,t
                        if maxi<=t:
                            maxi=t
                            p1=p
                    prob_matrix[counter][p]=maxi
                    back_point[counter][p]=p1
                   
            #prev_state=j
    #print "prob_matrix",prob_matrix     
    #print "back point",back_point  
    final_max=-1 # this is using backpointers
    final_tag=""
    curr_tag=""
    #length=len(prob_matrix)
    """for mm in prob_matrix[j]:
        if final_max<prob_matrix[j][mm]:
            final_max=prob_matrix[j][mm]
            final_tag=mm"""
    final_tag=max(prob_matrix[counter].iteritems(), key=operator.itemgetter(1))[0]
    #print "final tag is",final_tag
    """ v=list(prob_matrix[j].values())
    k=list(prob_matrix[j].keys())
    final_tag= k[v.index(max(v))]"""
    write_to_file=""
    write_to_file=write_to_file+j+"/"+final_tag+" "
    #print "writes here",write_to_file
    curr_tag=final_tag
    #print a
    #anslist=[]
    b=a[::-1]
    #print b
    c=j
    #anslist.append(final_tag)
    #anslist.append(c)
    #print c,mm
    b=b[1:]
    #print b
    
    #print "before going into for loop",write_to_file
    for tt in b:
        #print "here",tt,back_point[c][curr_tag]
        
        write_to_file=tt+"/"+back_point[counter][curr_tag]+" "+write_to_file
        
        #print "inside for",write_to_file
        #print "at other",write_to_file
        #anslist.append(back_point[c][curr_tag])
        #anslist.append(tt)
        
        curr_tag=back_point[counter][curr_tag]
        counter=counter-1
        c=tt
    #print anslist[::-1]  
    #print emptyi   
    final_ans=final_ans+write_to_file+"\n"
    #print "here",write_to_file
    #fp.write(write_to_file+"\n")
#print final_ans 
fp.write(final_ans)                  



  
#print "emi_prob",emi_prob  
#print emission
#print "prob_matrix",prob_matrix
#print "back_point",back_point 
#print prev_states