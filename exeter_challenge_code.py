#!/usr/bin/env python
# coding: utf-8

# In[59]:


import sys
import time
import re
import pandas as pd
from itertools import compress


# In[60]:


words_data = pd.read_csv(r"C:\Users\K G VINEETH\Desktop\french_dictionary.csv", header=None)
words_data.index = words_data[0]
words_data.drop(labels=[0], axis=1, inplace=True)
words_data.index.name = "english"
words_data.columns = ["french"]


# In[61]:


find_words = []
file = open(r"C:\Users\K G VINEETH\Desktop\find_words.txt")
find_words = ["".join(lines.split()) for lines in file.readlines()]
file.close()


# In[62]:


replace = []
file = open(r"C:\Users\K G VINEETH\Desktop\t8.shakespeare.txt")
replace = ["".join(lines.replace("\n", "")) for lines in file.readlines()]
file.close()


# In[63]:


words_count_before = {word:0 for word in find_words}
freq_replace = {word:0 for word in find_words}


# In[64]:


for i in range(len(replace)):
    splitted_words = replace[i].split()
    status = [True if (i.lower() in find_words) else False for i in splitted_words]
    idx = list(compress(range(len(status)), status))
    if len(idx) > 0:
        for j in idx:
            words_count_before[splitted_words[j].lower()] = words_count_before.get(splitted_words[j].lower()) + 1
    else:
        pass


# In[65]:


start_time = time.time()

for i in range(len(replace)):
    splitted_words = replace[i].split()
    status = [True if (i.lower() in find_words) else False for i in splitted_words]
    idx = list(compress(range(len(status)), status))
    if len(idx) > 0:
        for j in idx:
            freq_replace[splitted_words[j].lower()] = freq_replace.get(splitted_words[j].lower()) + 1
            splitted_words[j] = words_data.loc[splitted_words[j].lower()].values[0]
        replace[i] = " ".join(splitted_words)
    else:
        pass

end_time = time.time()
print("Time Taken to Translate : ", round((end_time - start_time),0), "seconds.")


# In[66]:


total_size = (sys.getsizeof(find_words) / 1e+6) + (sys.getsizeof(words_data) / 1e+6) + (sys.getsizeof(replace) / 1e+6)
print("Total Memory Size Required : ", total_size, "MB")


# In[67]:


final = [replace[i] + "\n" for i in range(len(replace))]


# In[68]:


file = open(r"C:\Users\K G VINEETH\Desktop\translated_output.txt", 'w')
file.writelines(final)
file.close()


# In[12]:


status = []
for i, j in zip(words_count_before.items(), freq_replace.items()):
    if (i[1] - j[1]) != 0:
        print(i[0], "wasn't replaced completely.")
    else:
        status.append(True)


# In[69]:


final_res = pd.DataFrame(data=[freq_replace.keys()]).T
final_res.columns = ["English"]


# In[70]:


final_df = pd.concat([final_res, words_data["french"]], axis=1)


# In[71]:


french_words = words_data["french"]
french_words.index = range(1000)


# In[72]:


final_df = pd.concat([final_res, words_data["french"]], axis=1)


# In[73]:


final_df = pd.concat([final_df, pd.Series(freq_replace.values(), index=range(1000))], axis=1)
final_df.columns = ["English", "French", "Frequency Replaced"]


# In[74]:


final_df.to_csv(r"C:\Users\K G VINEETH\Desktop\replaced_frequency.csv", index=None)


# In[77]:


n=total_size
f = open(r"C:\Users\K G VINEETH\Desktop\performance.txt", 'w')
f.write("Time to process: "+ str(round((end_time - start_time),0))+" seconds\n")
f.write("Memory used: "+str(n)+ " MB")
f.close()


# In[ ]:




