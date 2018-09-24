import sys

def build_ind_sin(seq,key):
	dic=dict()
	for (index,d) in enumerate(seq):
		if(dic.get(d[key])==None):
			dic[d[key]]=[]
		dic[d[key]].append(dict(d,index=index))
	return dic


def build_ind_comb(seq,key1,key2):
	return dict((d[key1]+"_"+d[key2], dict(d,index=index)) for (index,d) in enumerate(seq))

def loadRelations(filename):
	collection=[]
	with open(filename) as bgp_relations:
	        for relation in bgp_relations:
        	        relation_arr=relation.split('|')
                	if(relation_arr[2]=='0'):
                        	new_relation={
                                	"as1":relation_arr[0],
	                                "as2":relation_arr[1],
        	                        "rel":'s'
                	        }
                        	collection.append(new_relation)
	                        new_relation={
        	                        "as1":relation_arr[1],
                	                "as2":relation_arr[0],
                        	        "rel":'s'
	                        }
        	                collection.append(new_relation)
                	else:
                        	# 2|3|-1|bpg 2 is the provider and 3 is the customer
	                        new_relation={
        	                        "as1":relation_arr[0],
                	                "as2":relation_arr[1],
                        	        "rel":'p'
	                        }
        	                collection.append(new_relation)
                	        new_relation={
                        	        "as1":relation_arr[1],
                                	"as2":relation_arr[0],
	                                "rel":'c'
        	                }
                	        collection.append(new_relation)
	return collection


def relation(a,b):
	rel=Rel_as1_as2_ind.get(a + '_' + b)
	if(rel==None):
		return str('n')
	else:
		return str(rel['rel'])


def check_valley(path_array):
	temp_object = {
		'trip':'111',
		'rel':'nv'
	}
	for p,q,r in zip(path_array[:-2],path_array[1:-1], path_array[2:]):
		rel1=relation(p,q)
		rel2=relation(q,r)
		if(rel1=='p' and rel2=='c'):
			temp_object['trip']=p+'|'+q+'|'+r
			temp_object['rel']='pc'
			return temp_object
		elif(rel1=='p' and rel2=='s'):
			temp_object['trip']=p+'|'+q+'|'+r
                        temp_object['rel']='ps'
			return temp_object
		elif(rel1=='s' and rel2=='c'):
			temp_object['trip']=p+'|'+q+'|'+r
                        temp_object['rel']='sc'
			return temp_object
		elif(rel1=='s' and rel2=='s'):
			temp_object['trip']=p+'|'+q+'|'+r
                        temp_object['rel']='ss'
			return temp_object
	return temp_object



if(len(sys.argv)<3):
	print("Error: Command like python valley_in_file.py <relationship-file> <file-for-valley-check>")
	sys.exit(0)

Rel_as1_as2_ind=build_ind_comb(loadRelations(sys.argv[1]),"as1","as2")

with open(sys.argv[2]) as bgpRelations:
	for line in bgpRelations:
		line_array=line.split()
		ip_prefix=line_array[0]
		path_array=line_array[1:]
		path_array.reverse()
		if(len(path_array)>2):
			path_property=check_valley(path_array)
			if(path_property['rel']!='nv'):
				print '|'.join(path_array),
				print path_property['trip'],
				print path_property['rel']



'''
for prefix_data in data:
	paths=prefix_data['paths']
	for pn,p in paths.iteritems():
		p=p.rstrip('|')
		path_array=p.split('|')
		if(len(path_array)>2):
			path_property=check_valley(path_array)	
			if(path_property['rel']!='nv'):
				print p,
				print path_property['trip'],
				print path_property['rel']

'''
