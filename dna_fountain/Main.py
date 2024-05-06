import subprocess
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-i", "--input", help="input file", required=True)
parser.add_argument("-l", "--length", help="dna segment length", default = 140, type=int)
args = parser.parse_args()
print("Encoding begin:")
result = subprocess.run(['python', 'Input.py', '-i', args.input, '-l', str(args.length)])
l = result.returncode
print(l)
print("Encoding end.")
print("Noises adding begin:")
subprocess.run(['python', 'Noise.py'])
print("Noises adding end.")
print("Decoding begin:")
subprocess.run(['python', 'Output.py', '-l', str(l)])
print("Decoding end.")
exit(0)
