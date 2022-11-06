#!/usr/bin/env python3
import sys
import os

import JackCompiler

from .JackTokenizer import *

path = sys.argv[1]
isFile = os.path.isfile(path)
