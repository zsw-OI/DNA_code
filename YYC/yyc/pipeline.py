"""
Name: Entry function

Coder: HaoLing ZHANG (BGI-Research)[V1]

Current Version: 1

Function(s): After initializing the encoding or decoding method,
             the conversion between DNA sequence set and binary files is completed
             by the entry function.
"""
import sys
from yyc.utils import log, data_handle, index_operator, model_saver
from reedsolo import RSCodec

def symbol_to_binary(symbol, bits_per_symbol):
    return [int(x) for x in format(symbol, f'0{bits_per_symbol}b')]

# noinspection PyProtectedMember
def encode(method, input_path, output_path,
           model_path=None, verify=None, need_index=True, segment_length=120, need_log=False):
    """
    introduction: Use the selected method, convert the binary file to DNA sequence
                  set and output the DNA sequence set.

    :param method: Method under folder "methods/".
                    Type: Object.

    :param input_path: The path of binary file you need to convert.
                        Type: String.

    :param output_path: The path of DNA sequence set you need to use to .
                         Type: String.

    :param model_path: The path of model file if you want to save
                        Type: String

    :param verify: Error correction method under "methods/verifies/"
                    Type: Object.

    :param need_index: Declare whether the binary sequence indexes are required
                       in the DNA sequences.
                        Type: bool.

    :param segment_length: The cut length of DNA sequence.
                      Considering current DNA synthesis factors, we usually
                      set 120 bases as a sequence.

    :param need_log: Show the log.
    """

    if input_path is None or len(input_path) == 0:
        log.output(log.ERROR, str(__name__), str(sys._getframe().f_code.co_name),
                   "The input file path is invalid!")

    if output_path is None or len(input_path) == 0:
        log.output(log.ERROR, str(__name__), str(sys._getframe().f_code.co_name),
                   "The output file path is invalid!")

    input_matrix, size = data_handle.read_binary_from_all(input_path, segment_length, need_log)

    if need_index:
        input_matrix = index_operator.connect_all(input_matrix, need_log)

    length = len(input_matrix[0])
    print(f'length = {length}')
    # Example parameters
    bits_per_symbol = 8  # This depends on the maximum symbol value, e.g., 255 requires 8 bits

    # Assuming `input_matrix` is already filled with your input binary data
    rs = RSCodec(2)  # This would still use Reed-Solomon with non-binary symbols
    encoded_matrix = [rs.encode(item) for item in input_matrix]

    # Convert each symbol in the encoded matrix to a binary format
    binary_encoded_matrix = []
    for encoded_row in encoded_matrix:
        binary_row = []
        cnt = 0
        for symbol in encoded_row:
            cnt += 1
            if cnt >= length:
                binary_row.extend(symbol_to_binary(symbol, bits_per_symbol))
            else:
                binary_row.append(symbol)
        binary_encoded_matrix.append(binary_row)

    if verify is not None:
        input_matrix = verify.add_for_matrix(input_matrix, need_log)

    print(binary_encoded_matrix[0])
    dna_sequences = method.encode(binary_encoded_matrix, size, need_log)

    if model_path is not None:
        model_saver.save_model(model_path, {"method": method, "verify": verify, "length": length})

    data_handle.write_dna_file(output_path, dna_sequences, need_log)


# noinspection PyProtectedMember
def decode(method=None, model_path=None, input_path=None, output_path=None,
           verify=None, has_index=True, need_log=False, length = 133):
    """
    introduction: Use the selected method, convert DNA sequence set to the binary
                  file and output the binary file.

    :param method: Method under folder "methods/".
                    If you have model file, you can use this function with out
                    method.
                    Type: Object.

    :param input_path: The path of DNA sequence set you need to convert.
                       Type: String.

    :param output_path: The path of binary file consistent with previous
                        documents.
                         Type: String.

    :param model_path: The path of model file if you want to save
                        Type: String

    :param verify: Error correction method under "methods/verifies/"
                    Type: Object.

    :param has_index: Declare whether the DNA sequences contain binary sequence
                      indexes.
                       Type: bool.

    :param need_log: Show the log.
    """

    if method is None and model_path is None:
        log.output(log.ERROR, str(__name__), str(sys._getframe().f_code.co_name),
                   "The method you select does not exist!")
    else:
        if input_path is None or len(input_path) == 0:
            log.output(log.ERROR, str(__name__), str(sys._getframe().f_code.co_name),
                       "The input file path is not valid!")

        if output_path is None or len(output_path) == 0:
            log.output(log.ERROR, str(__name__), str(sys._getframe().f_code.co_name),
                       "The output file path is not valid!")

        if model_path is not None:
            model = model_saver.load_model(model_path)
            method = model.get("method")
            verify = model.get("verify")
            length = model.get("length")

        dna_sequences = data_handle.read_dna_file(input_path, need_log)

        output_matrix, size = method.decode(dna_sequences, need_log)

        # decode_matrix = []
        # for item in output_matrix:
        #     cur = []
        #     for i in range(len(item)):
        #         if i < length:
        #             cur.append(item[i])
        #         else:
        #             val = 0
        #             for j in range(8):
        #                 if i + j >= len(item):
        #                     break
        #                 val += item[i+j] * (2 ** (7-j))
        #             print(val)
        #             cur.append(val)
        #             i += 7
        #     decode_matrix.append(cur) 
        # if verify is not None:
        #     output_matrix = verify.verify_for_matrix(output_matrix, need_log)

        # if has_index:
        #     indexes, data_set = index_operator.divide_all(decode_matrix, need_log)
        #     output_matrix = index_operator.sort_order(indexes, data_set, need_log)

        # print(output_matrix[0])
        data_handle.write_all_from_binary(output_path, output_matrix, size, need_log)
