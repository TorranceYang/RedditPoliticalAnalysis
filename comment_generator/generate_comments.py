import markovify
import argparse

parser = argparse.ArgumentParser(description='Generate the comments')
parser.add_argument("--file", "-f", 
					help="Input the file you want to generate from",
					required=True)
parser.add_argument("--num", "-n", 
					help="Number of comments you want to generate",
					default=10)
parser.add_argument("--length", "-l", 
					help="Number of characters per comment to generate",)

args = parser.parse_args()

with open(args.file) as text_file:
	text = text_file.read()

text_model = markovify.Text(text)

for i in range(int(args.num)):
	if args.length is None:	
		print(text_model.make_sentence())
	else:
		print(text_model.make_short_sentence(int(args.length)))
