"""Internal module for running tests from cibuildwheel"""

import sys
import jimplejson.tests

if __name__ == '__main__':
    jimplejson.tests.main(project_dir=sys.argv[1])
