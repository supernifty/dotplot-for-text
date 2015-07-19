#!/usr/bin/env python
# make a dot plot of incoming text

import argparse
import collections
import Image
import re
import sys

def dot(p, x, y, x_size, y_size, max_size):
  if x_size > max_size:
    x = x * max_size / x_size
  if y_size > max_size:
    y = y * max_size / y_size
  p[x, y] = (0, 0, 0)
  
def generate( candidate_fh, reference_fh=None, words=False, k=1, max_size=1024 ):
  print "building candidate k-mers..."
  cand_map = [] # pos -> kmers
  history = [''] * k # for k-mer
  ref_kmers = collections.defaultdict(set) # kmers -> pos
  cand_pos = 0
  for line in candidate_fh:
    line = line.strip().lower()
    if words:
      word_list = re.sub( "[^\w]", " ", line ).split()
      for word in word_list:
        history.insert( 0, word ) # insert at start
        history.pop() # takes off end
        identity = hash( ' '.join( history ) )
        cand_map.append( identity )
        if reference_fh is None:
          ref_kmers[identity].add( cand_pos )
        cand_pos += 1
    else:
      for word in line:
        history.insert( 0, word ) # insert at start
        history.pop() # takes off end
        identity = hash( ''.join( history ) )
        cand_map.append( identity )
        if reference_fh is None:
          ref_kmers[identity].add( cand_pos )
        cand_pos += 1
  print "building candidate k-mers: %i positions" % cand_pos

  if reference_fh is not None:
    print "building reference k-mers..."
    ref_pos = 0
    for line in reference_fh:
      line = line.strip().lower()
      if words:
        word_list = re.sub( "[^\w]", " ", line ).split()
        for word in word_list:
          history.insert( 0, word ) # insert at start
          history.pop() # takes off end
          identity = hash( ' '.join( history ) )
          ref_kmers[identity].add( ref_pos )
          ref_pos += 1
      else:
        for word in line:
          history.insert( 0, word ) # insert at start
          history.pop() # takes off end
          identity = hash( ''.join( history ) )
          cand_map.append( identity )
          ref_kmers[identity].add( ref_pos )
          ref_pos += 1
    print "building reference k-mers: %i positions" % ref_pos
  else:
    ref_pos = cand_pos
 
  print "creating image"
  image = Image.new( 'RGB', (min(cand_pos, max_size), min(ref_pos, max_size)), "white" )
  pixels = image.load()

  print "generating dot plot"
  for x in xrange(cand_pos):
    identity = cand_map[x]
    for y in ref_kmers[identity]:
        dot(pixels, x, y, cand_pos, ref_pos, max_size)

  print "showing image"
  image.show()

if __name__ == '__main__':
  parser = argparse.ArgumentParser(description='Generate dotplot from text')
  parser.add_argument('-k', dest='k', type=int, default=1, help='window size (default 1)')
  parser.add_argument('-w', dest='w', type=bool, default=False, help='word as unit (default char)')
  parser.add_argument('-m', dest='m', type=int, default=1024, help='max image size (default 1024)')
  parser.add_argument('-r', dest='reference', required=False, help='compare stdin to this file')
  args = parser.parse_args()
  print "Words is %s, %s k-mer size" % (args.w, args.k)
  if args.reference is None:
    generate( sys.stdin, reference_fh=None, words=args.w, k=args.k, max_size=args.m )
  else:
    generate( sys.stdin, reference_fh=open( args.reference, 'r' ), words=args.w, k=args.k, max_size=args.m )
