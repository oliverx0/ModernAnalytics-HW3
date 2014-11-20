import parse_movies_example as h

movies = h.load_all_movies('../plot.list.gz')

print len(movies)