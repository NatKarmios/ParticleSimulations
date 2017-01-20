from pythia_lib.pythia8 import Pythia

p = Pythia("", True)
p.readFile("cfg.txt")
p.init()
p.next()
