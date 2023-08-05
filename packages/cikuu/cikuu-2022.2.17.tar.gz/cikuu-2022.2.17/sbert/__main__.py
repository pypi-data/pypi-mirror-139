#pip install -U sentence-transformers
import fire 
from sentence_transformers import SentenceTransformer
model = SentenceTransformer('all-MiniLM-L6-v2')

def readline(infile, sepa=None):
	with open(infile, 'r') as fp:
		while True:
			line = fp.readline()
			if not line: break
			yield line.strip().split(sepa) if sepa else line.strip()

class util(object):
	def __init__(self): pass 

	def vec(self, infile, outfile=None): 
		''' gzjc.snt -> gzjc.snt.vec  '''
		if not outfile : outfile = infile + ".vec"
		print ("started:", infile, flush=True)
		with open(oufile, 'w') as fw: 
			for line in readline(infile): 
				vec = model.encode(line.strip())
				fw.write(f"{line.strip()}\t{json.dumps(vec.tolist())}\n")
		print ("finished:", infile)


if __name__ == '__main__':
	fire.Fire(util)