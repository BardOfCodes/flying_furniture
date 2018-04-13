#The global variables for saving files etc.
import csv
import os
import sys
csv.field_size_limit(sys.maxsize)
import pickle
obj_class = {'basket':['02801938','basket',['basket'],[]],
           'bunk_bed':['02818832','bed',['bunk bed'],[]],
           'normal_bed':['02818832','bed',['cot','platform bed','headless beds','king size beds'],[]],
           'flat_bench':['02828884','bench',['flat bench'],[]],
           'normal_bench':['02828884','bench',['park bench'],[]],
           'birdhouse':['02843684','birdhouse',['birdhouse'],[]],
           'bookshelf':['02871439','bookshelf',['bookshelf'],[]],
           'dresser_cabinet':['02933112','cabinet',['dresser'],[]],
           'twodoor_cabinet':['02933112','cabinet',['two-door cabinet'],[]],
           'desk_cabinet':['02933112','cabinet',['desk cabinet'],[]],
           'zigzag_chair':['03001627','chair',['zigzag chair'],[]],
           'swivel_chair':['03001627','chair',['swivel chair'],[]],
           'straight_chair':['03001627','chair',['straight chair'],[]],
           'clock':['03046257','clock',['pendulum clock','longcase clock','grandfather clock'],[]],
           'lamp':['03636649','lamp',['table lamp','floor lamp','lamp'],[]],
           'letter_box':['03710193','mailbox',['letter box','mailbox'],[]],
           'lshaped_sofa':['04256520','sofa',['L-shaped couch'],[]],
           'normal_sofa':['04256520','sofa',['sofa bed','double couch'],[]],
           'coffee_table':['04379243','table',['coffee table'],[]],
           'pool_table':['04379243','table',['pool table'],[]],
          }

image_size = (128,128)
##### For class Disbalance:
images_per_class = [3222, ]*len(obj_class.keys())
images_per_class[10] = 1002 
images_per_class[5] = 1002

test_im_per_class = [545, ]*len(obj_class.keys())
test_im_per_class[10] = 405 
test_im_per_class[5] = 405
for iter,name in enumerate(obj_class.keys()):
    obj_class[name].append(images_per_class[iter])
    obj_class[name].append(test_im_per_class[iter])
# At last the label
for iter,name in enumerate(obj_class.keys()):
    obj_class[name].append(iter)
    
# we need to add the color 12 way classification
# from pascal
colors = [(192.0, 128.0, 0.0), (128.0, 64.0, 0.0), (0.0, 64.0, 128.0), (0.0, 128.0, 0.0), (192.0, 128.0, 128.0), (64.0, 0.0, 128.0), (0.0, 64.0, 0.0),  (128.0, 0.0, 0.0), (128.0, 128.0, 128.0), (192.0, 0.0, 128.0), (64.0, 128.0, 128.0), (128.0, 192.0, 0.0)]
class_name = list(set([obj_class[i][1] for i in obj_class.keys()]))
color_map = {}
for i in range(12):
    color_map[class_name[i]] = colors[i]
   
for iter,name in enumerate(obj_class.keys()):
    obj_class[name].append(color_map[obj_class[name][1]])


# Now a list of objects in each class?
for name,obj in obj_class.iteritems():
    csv_file = os.path.join('meta_files',obj[1]+'.txt')
    with open(csv_file, 'rb') as csvfile:
        spamreader = csv.reader(csvfile)
        count = 0
        tot_types = []
        for row in spamreader:
            if len(row)>=3:
                types = row[2].split(',')
                tot_types.extend(types)
                tot_types = list(set(tot_types))
                if any(a in types for a in obj[2]):
                    count+=1
                    obj[3].append(row[0].split('.')[1])
                    #print('================')
        print('count for ',name,obj[1],count)
        print(len(obj[3]))
        #print('TOt Types',tot_types)

## The benches have to be set manually :(
## Bad partitioning provided
name = 'flat_bench'
obj = obj_class[name]
csv_file = os.path.join('meta_files',obj[1]+'.txt')
with open(csv_file, 'rb') as csvfile:
    spamreader = csv.reader(csvfile)
    count = 0
    tot_types = []
    for row in spamreader:
        if len(row)>=3:
            name_types = row[-2].split(' ')
            if 'Flat' in name_types:
                obj[3].append(row[0].split('.')[1])
                #print('================')
    obj[3] = list(set(obj[3]))
    print('Updated count for ',name,obj[1],len(set(obj[3])))
# Now remove any intersection with normal benches
name = 'normal_bench'
obj_normal = obj_class[name]
obj_normal[3] = [x for x in obj_normal[3] if x not in obj[3]]
print('Updated count for ',name,obj_normal[1],len(set(obj_normal[3])))
 
# Max variety     
for name,obj in obj_class.iteritems():
    obj[3] = obj[3][:100]

# Now save the info
pickle.dump(obj_class,open('info.npy','w'))
