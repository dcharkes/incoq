import pickle
import matplotlib.pyplot as plt


# 04/12/14

# 256KB L2
#xs = [250, 500, 750, 1000, 1250, 1500, 1750, 2000, 2250, 2500, 2750, 3000, 3250, 3500, 3750, 4000, 4250, 4500, 4750, 5000, 6000, 7000, 8000, 9000, 10000, 11000, 12000, 13000, 14000, 15000, 16000, 17000, 18000, 19000, 20000]
#data = [(36839495, 28933393, 0.6), (38906203, 29640431, 0.6), (39950488, 30810175, 0.7), (39225314, 31930240, 0.7), (40211296, 32850667, 0.7), (39714824, 33588059, 0.7), (40415099, 34185759, 0.7), (40449147, 34671359, 0.7), (40634531, 35112104, 0.7), (40611617, 35431350, 0.7), (40206321, 35702280, 0.8), (40686005, 35962530, 0.8), (40781916, 36166864, 0.8), (40193143, 36399198, 0.8), (42377080, 36536521, 0.8), (40220595, 36672977, 0.8), (40810453, 36839293, 0.8), (40821886, 36954327, 0.8), (40957729, 37039489, 0.8), (40245405, 37137110, 0.8), (40383981, 37458883, 0.8), (41040566, 37681682, 0.8), (40350945, 37857735, 0.8), (40513672, 38000122, 0.8), (40964753, 38128214, 0.8), (40454544, 38204339, 0.8), (40391346, 38286903, 0.8), (41027105, 38365262, 0.8), (40502316, 38410943, 0.8), (40486473, 38464964, 0.8), (41012594, 38510648, 0.8), (40605507, 38535189, 0.8), (41642119, 38575523, 0.8), (41121534, 38602970, 0.8), (40542056, 38640512, 0.8)]

# 3MB L3
#xs = [1000, 2001, 3002, 4003, 5004, 6005, 7006, 8007, 9008, 10009, 11010, 12011, 13012, 14013, 15014, 16015, 17016, 18017, 19018]
#data = [(39099639, 28259361, 0.6), (40493051, 28261871, 0.6), (40591083, 28303905, 0.6), (40213833, 28459105, 0.6), (40254940, 28710953, 0.6), (40257082, 28996520, 0.6), (40897821, 29375580, 0.6), (40195539, 29814871, 0.6), (40273197, 30196089, 0.6), (40282054, 30527506, 0.6), (40379378, 30916869, 0.7), (40269986, 31309598, 0.7), (40906064, 31630122, 0.7), (40435589, 31907858, 0.7), (40869009, 32209858, 0.7), (40459292, 32459144, 0.7), (40920110, 32738073, 0.7), (40395318, 32944972, 0.7), (40325112, 33111124, 0.7)]

# 04/13/14

# 256KB L2
xs = [250, 500, 750, 1000, 1250, 1500, 1750, 2000, 2250, 2500, 2750, 3000, 3250, 3500, 3750, 4000, 4250, 4500, 4750, 5000, 6000, 7000, 8000, 9000, 10000, 11000, 12000, 13000, 14000, 15000, 16000, 17000, 18000, 19000, 20000]
data = [(5148163862, 168702325, 3.2, 169536629, 139457266, 0.8), (5148454547, 178335406, 3.4, 179171929, 142792815, 0.8), (5165475273, 182006968, 3.5, 182846669, 148605480, 0.8), (5148288965, 183968638, 3.5, 184805677, 153969717, 0.9), (5179234274, 185064107, 3.5, 185900077, 158629540, 0.9), (5165636858, 185942848, 3.5, 186780734, 162400413, 0.9), (5155897656, 186427379, 3.6, 187264816, 165244567, 0.9), (5148408090, 187386332, 3.6, 188219109, 167658624, 0.9), (5189185307, 187155141, 3.6, 187993337, 169768637, 0.9), (5179529217, 187464759, 3.6, 188304389, 171450562, 0.9), (5172289787, 187670805, 3.6, 188508041, 172744479, 1.0), (5165535756, 188113077, 3.6, 189549787, 173849321, 1.0), (5160003804, 187923412, 3.6, 188759724, 175082026, 1.0), (5155127267, 188038749, 3.6, 188873461, 175860340, 1.0), (5151761335, 188182606, 3.6, 189018339, 176843486, 1.0), (5148226447, 188440382, 3.6, 189275971, 177586281, 1.0), (5194275499, 188434932, 3.6, 189272028, 178176996, 1.0), (5208043640, 188582271, 3.6, 190322508, 178728423, 1.0), (5184297063, 188641636, 3.6, 189478604, 179288558, 1.0), (5178983902, 188831750, 3.6, 189669840, 179810689, 1.0), (5165573772, 189081851, 3.6, 190516327, 181203328, 1.0), (5155518225, 188965223, 3.6, 189800874, 182365581, 1.0), (5147787256, 189658369, 3.6, 190492115, 183215419, 1.0), (5189250321, 189217636, 3.6, 190654859, 183814930, 1.0), (5179392497, 189263611, 3.6, 190098710, 184469244, 1.0), (5172131002, 189526978, 3.6, 190961379, 184920567, 1.0), (5165666531, 189337687, 3.6, 190773051, 185175840, 1.0), (5160222828, 189393641, 3.6, 190227754, 185593950, 1.0), (5155515327, 189566387, 3.6, 190402766, 185713223, 1.0), (5151545895, 190051910, 3.6, 190886444, 186092973, 1.0), (5148399094, 189586573, 3.6, 191022343, 186329237, 1.0), (5194420724, 189655166, 3.6, 190492098, 186390004, 1.0), (5189068399, 190167073, 3.6, 191005401, 186655224, 1.0), (5184155948, 189547024, 3.6, 190383787, 186740154, 1.0), (5179838651, 189578928, 3.6, 190416887, 186912329, 1.0)]



#with open('cachetest_out.pickle', 'rb') as f:
#    xs = pickle.load(f)
#    data = pickle.load(f)


print(xs)
print(data)

drefs, d1misses, d1missrate, llrefs, llmisses, llmissrate = zip(*data)
ymax = None

xs = [x / 1e3 for x in xs]
drefs = [y / 1e6 for y in drefs]
d1misses = [y / 1e6 for y in d1misses]
llrefs = [y / 1e6 for y in llrefs]
llmisses = [y / 1e6 for y in llmisses]


#plt.plot(xs, drefs, '-s', label='D refs')
#ymax = 6000

plt.plot(xs, d1misses, '-s', label='D1 misses')
#plt.plot(xs, llrefs, '-o', label='L2 refs')
#plt.plot(xs, llmisses, '-o', label='L2 misses')

plt.ylabel('Millions')


#plt.plot(xs, d1missrate, '-o', label='D1 miss rate')
#plt.plot(xs, llmissrate, '-o', label='L2 miss rate')
#plt.ylabel('Percent')

plt.xlabel('Number of unique objects (in thousands)')
plt.legend(loc='lower right')
plt.gca().set_ylim(bottom=0, top=ymax)
plt.show()