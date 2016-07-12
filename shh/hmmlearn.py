'''
Created on Apr 9, 2016

@author: akhila
'''
from collections import OrderedDict
import json
import pickle
import sys

a_dir1=sys.argv[1]
lines = open(a_dir1,'r').read().splitlines()

word_tag={}
start_tags={}
all_tags={}
end_tags={}
prev_tag="akhila"
final_dict={}
for i in lines:
    #print i
    a=i.split() #splits each line by space and returns words with /
    temp=a[0].rindex("/")
    var=a[0][temp+1:] #contains the starting tag
    if var not in start_tags:
        start_tags[var]=1;
    else:
        start_tags[var]=start_tags[var]+1
    for j in a:  #each word with /
        b=j.rindex("/")
        var1=j[b+1:]
        if prev_tag=="akhila":
            prev_tag=var1
        else:
            if prev_tag not in final_dict:
                final_dict[prev_tag]={}
            if var1 not in final_dict[prev_tag]:
                final_dict[prev_tag][var1]=1
            else:
                final_dict[prev_tag][var1]=final_dict[prev_tag][var1]+1
                #adj_tags[var1]=adj_tags[var1].append(prev_tag)
        if j[0:b] not in word_tag:
            word_tag[j[0:b]]={}
            word_tag[j[0:b]][var1]=1
        else:
            if var1 not in word_tag[j[0:b]]:
                word_tag[j[0:b]][var1]=1
            else:
                word_tag[j[0:b]][var1]=word_tag[j[0:b]][var1]+1
            
        if var1 in all_tags:
            all_tags[var1]=all_tags[var1]+1
        else:
            all_tags[var1]=1   
            
            #print "***********"
        prev_tag=var1
    n=j.split("/")
    n1=n[1]
    if n1 not in end_tags:
        end_tags[n1]=1
    else:
        end_tags[n1]=end_tags[n1]+1
    prev_tag="akhila"
        
#print "word_tag",word_tag
#print "start_tags",start_tags
#print "all_tags",all_tags
#print "end_tags",end_tags
#print "final_dict",final_dict
sum1=0
for k in start_tags.values():
    #print k
    sum1=sum1+k
#print sum1 
#print len(all_tags)  
dump_dict={}
dump_dict['qo']={}
for p in final_dict:
    dump_dict[p]={}
    if p in start_tags:
        dump_dict['qo'][p]=(0.0+start_tags[p])/sum1 #is it sum i.e total number of sentences or this
    if p in end_tags:
        for q in final_dict[p]:
            dump_dict[p][q]=(0.0+final_dict[p][q])/(all_tags[p]-end_tags[p])
    else:
        for q in final_dict[p]:
            dump_dict[p][q]=(0.0+final_dict[p][q])/all_tags[p]
for q in all_tags:
    if q not in dump_dict['qo']:
        dump_dict['qo'][q]=(0.0+1)/(sum1+1)
    for w in all_tags:
        if w not in dump_dict[q]:
            if q not in end_tags:
                dump_dict[q][w]=1.0/(all_tags[q]+1)
            else:
                #print "in else",all_tags[q]-end_tags[q]
                dump_dict[q][w]=1.0/(all_tags[q]-end_tags[q]+1)
write_dict=[]
emission={}
#print "all_tags",all_tags
#print "word_tag",word_tag
for i in word_tag:
    emission[i]={}
    for j in word_tag[i]:
        emission[i][j]=(0.0+word_tag[i][j])/all_tags[j]
#write_dict[0]={}
#print emission
#write_dict[1]={}
#print "dump_dict",len(dump_dict)
#for i in dump_dict:
    #print i,"-----------",dump_dict[i]
#write_dict.append(word_tag)
#write_dict.append(all_tags)
write_dict.append(dump_dict)
#print "transiton",dump_dict
#print dump_dict['qo']
#write_dict.append(end_tags)
write_dict.append(emission)
write_dict.append(all_tags)
#with open('hmmmodel.txt','w+' ) as fp:
    #json.dump(write_dict,fp)
output=open("hmmmodel.pkl","wb")
pickle.dump(write_dict,output)

   
    