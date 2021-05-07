from tagcounter import TagCounter
import sys


c = TagCounter(sys.argv[1:])
c.execute()
