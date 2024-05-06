import subprocess
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", help="input file", required=True)
parser.add_argument("-l", "--length", help="dna segment length", default = 128, type=int)
args = parser.parse_args()

syn_error = 0.001
seq_error = 0.01
copies = 100

print("Encoding begin:")
result = subprocess.run([\
    'python', 'Input.py', '-i', args.input, '-l', str(args.length), '-se', str(syn_error), '-qe', str(seq_error), '-cp', str(copies)\
    ])
l = result.returncode
print("Encoding end.")
print("Noises adding begin:")
subprocess.run(['python', 'Noise.py', '-se', str(syn_error), '-qe', str(seq_error), '-cp', str(copies)])
print("Noises adding end.")
print("Decoding begin:")
subprocess.run(['python', 'Output.py', '-l', str(l)])
print("Decoding end.")
exit(0)
