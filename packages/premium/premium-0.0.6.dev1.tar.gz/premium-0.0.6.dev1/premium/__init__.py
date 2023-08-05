import builtins

import codefast as cf

from premium.datasets import downloader, word2vec
from premium.measure import libra
from premium.preprocess import any_cn, jb_cut, pkl, once
from premium.postprocess import mop
from premium.models.clf import Classifier
from premium.demo import demo_object as demo
