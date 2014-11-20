import parse_movies_example as h
import math
import matplotlib.pyplot as plt

movies = h.load_all_movies('../plot.list.gz', False)
total_movies = len(movies)
y = []
x = [1930, 1940, 1950, 1960, 1970, 1980, 1990, 2000, 2010]

# print len(movies)
decade_counts = {"1930":0, "1940":0, "1950":0, "1960":0, "1970":0, "1980":0, "1990":0, "2000":0, "2010":0}

## dictionary of decades and their respective movie_counts
for m in movies:
    # year = decade_counts.get('year') ##print "Value : %s" %  
    decade = math.trunc(float(m['year'])/10)*10
    decade_counts[str(decade)] += 1

for d in decade_counts:
    print decade_counts[d]
    decade_counts[d] = float(decade_counts[d])/float(total_movies)
  
for i in x:
    y.append(decade_counts[str(i)])

print decade_counts
print y 

plt.bar(x,y, width = 10)
plt.show()



