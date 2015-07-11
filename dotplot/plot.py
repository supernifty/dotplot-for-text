
# make a dot plot of incoming text

import argparse
import collections
import Image
import re
import sys

MAX_SIZE=4096

def dot(p, x, y, size, max_size):
  if size > max_size:
    x = x * max_size / size
    y = y * max_size / size
  p[x, y] = (0, 0, 0)
  
def generate( reference_fh, candidate_fh=None, words=False, k=1 ):
  print "building k-mers..."
  reference = [] # pos -> kmers
  history = [''] * k # for k-mer
  candidate = collections.defaultdict(set) # kmers -> pos
  pos = 0
  for line in reference_fh:
    line = line.strip().lower()
    if words:
      word_list = re.sub( "[^\w]", " ", line ).split()
      for word in word_list:
        history.insert( 0, word ) # insert at start
        history.pop() # takes off end
        identity = hash( ' '.join( history ) )
        reference.append( identity )
        candidate[identity].add( pos )
        pos += 1
    else:
      for word in line:
        history.insert( 0, word ) # insert at start
        history.pop() # takes off end
        identity = hash( ''.join( history ) )
        reference.append( identity )
        candidate[identity].add( pos )
        pos += 1
  print "building k-mers: %i positions" % pos

  print "creating image"
  image = Image.new( 'RGB', (min(pos, MAX_SIZE), min(pos, MAX_SIZE)), "white" )
  pixels = image.load()

  print "generating dot plot"
  for x in xrange(pos):
    identity = reference[x]
    for y in candidate[identity]:
        dot(pixels, x, y, pos, MAX_SIZE)

  print "showing image"
  image.show()

if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='Generate dotplot from text')
  parser.add_argument('-k', dest='k', type=int, default=1, help='window size')
  parser.add_argument('-w', dest='w', type=bool, default=False, help='word as unit (default char)')
  #parser.add_argument('--reference', dest='reference', type=int, default=0, help='only consider alignments with at least this distance from the true location')
  args = parser.parse_args()
  print "Words is %s, %s k-mer size" % (args.w, args.k)
  generate( sys.stdin, candidate_fh=None, words=args.w, k=args.k )
