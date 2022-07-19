class Utilities:
	def __init__(self, name):
		self.name = name

	@classmethod
	def replaceInFile(cls, infile: str, outfile: str, toreplace: dict):
		fin = open(infile, "rt")
		#output file to write the result to
		fout = open(outfile, "wt")
		#for each line in the input file
		for line in fin:
			outstr = line
			for key in toreplace:
				outstr = outstr.replace(key, toreplace.get(key))
			fout.write(outstr)
		#close input and output files
		fin.close()
		fout.close()

