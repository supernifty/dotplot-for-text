
# make a dot plot of incoming text

import argparse
import collections
import Image
import re
import sys

def dot(p, x, y):
  p[x, y] = (0, 0, 0)
  
def generate( reference_fh, candidate_fh=None, words=False, k=1 ):
  print "building k-mers..."
  reference = collections.defaultdict(set)
  pos = 0
  for line in reference_fh:
    line = line.strip()
    if words:
      word_list = re.sub( "[^\w]", " ", line ).split()
      for word in word_list:
        reference[word].add( pos )
        pos += 1
    else:
      for c in line:
        reference[c].add( pos )
        pos += 1
  print "building k-mers: %i positions" % pos

  print "creating image"
  image = Image.new( 'RGB', (pos, pos), "white" )
  pixels = image.load()

  print "generating dot plot"
  for kmer in reference:
    for x in reference[kmer]:
      for y in reference[kmer]:
        dot(pixels, x, y)

  print "showing image"
  image.show()

if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='Generate dotplot from text')
  parser.add_argument('-k', dest='k', type=int, default=1, help='window size')
  parser.add_argument('-w', dest='w', type=bool, default=False, help='word as unit')
  #parser.add_argument('--reference', dest='reference', type=int, default=0, help='only consider alignments with at least this distance from the true location')
  args = parser.parse_args()
  print "Words is %s, %s k-mer size" % (args.w, args.k)
  generate( sys.stdin, candidate_fh=None, words=args.w, k=args.k )
