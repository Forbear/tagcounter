from tagcounter import TagCounter
from tagcounter import TagCounterApp
import sys


if len(sys.argv) > 1:
    c = TagCounter(sys.argv[1:])
    print(c.execute())
else:
    c_app = TagCounterApp()
    c_app.run()
