import subprocess
import argparse
import Input
import Output
import Noise
parser = argparse.ArgumentParser()
parser.add_argument("-t", "--test", help="test mode", default = False, type = bool)
parser.add_argument("-i", "--input", help="input file", default = None)
parser.add_argument("-l", "--length", help="dna segment length", default = 128, type=int)
args = parser.parse_args()

if args.test == True:
    # syn_error_list = [0.0001, 0.001, 0.01]
    # seq_error_list = [0.002, 0.005, 0.01]
    error_list = [0.0001, 0.001, 0.01]
    copies_list = [50, 100, 200]
    file_list = ["./120.data", "./203.data", "./521.data"]
    alpha_list = [0.01, 0.005, 0, -0.005, -0.01]
    length_list = [128, 256]
    # syn_error_list = [0.001, 0.002]
    # seq_error_list = [0.001]
    # error_list = [0.001]
    # copies_list = [100]
    # file_list = ["./120.data", "./203.data"]
    # alpha_list = [0.03, -0.5, 0.02]
    # length_list = [128]
    error_list = [0.01]
    copies_list = [50, 100, 200]
    file_list = ["./120.data", "./203.data", "./521.data"]
    alpha_list = [-0.1, -0.125, -0.15]
    length_list = [128]
    tot = len(error_list) * len(copies_list) * len(file_list) * len(length_list) * len(alpha_list)
    cnt = 0
    with open("testdata.out", "w") as f:
        for error in error_list:
            for copies in copies_list:
                for file in file_list:
                    
                    for length in length_list:            
                        for alpha in alpha_list:
                            cnt += 1
                            print("round: " + str(cnt) + '/' + str(tot))
                            f.write(str(error) + ' ' + str(copies) + ' ' + str(file) + ' ' + str(length) + ' ' + str(alpha) + ' ')
                            # if not tg:
                            #     continue
                            print("Encoding begin:")
                            # result = subprocess.run([\
                            #     'python', 'Input.py', '-i', file, '-l', str(length), '-se', str(syn_error), '-qe', str(seq_error), '-cp', str(copies), \
                            #     '-a', str(alpha)])
                            syn_error = seq_error = error
                            l, density = Input.main(input = file, length = length, syn_error = syn_error, seq_error = seq_error, copies = copies, alpha = alpha)
        
                            print("Encoding end.")
                            print("Noises adding begin:")
                            Noise.main(syn_error = syn_error, seq_error = seq_error, copies = copies)
                            # subprocess.run(['python', 'Noise.py', '-se', str(syn_error), '-qe', str(seq_error), '-cp', str(copies)])
                            print("Noises adding end.")
                            print("Decoding begin:")
                            # res = subprocess.run(['python', 'Output.py', '-l', str(l)]).returncode
                            recovery = Output.main(length = l)
                            print(recovery)
                            print("Decoding end.")
                            f.write(str(density) + ' ' + str(recovery) + '\n')

    exit(0)

if args.input is None:
    raise Exception("Input file cannot be None!")
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
