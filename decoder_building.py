from main import H_x, H_z, recovery, logical_x
import numpy as np
import math

def generating_errors_w1(error):
    error_list = []

    for symb_ind in range(len(error)):
        if error[symb_ind] == 'I':
            error[symb_ind] = 'Z'
            error_list.append("".join(error))
            error[symb_ind] = 'I'

    return error_list

def generate_all_errors(n):
    identity = 'I'*n
    all_errors = [identity]
    error_list = [identity]

    for i in range(n):
        weight_errors = set()

        for error in error_list:
            weight_errors.update(generating_errors_w1(error=list(error)))


        all_errors.extend(weight_errors)
        error_list = weight_errors

    return all_errors

def error_to_vector(error):
    return np.array([int(sym == "Z") for sym in error])

def compute_syndrome(H_x, error):
    e = [1 if sym == 'Z' else 0 for sym in error]

    return tuple(((H_x @ e) % 2).tolist())

def error_to_syndrome(H_x):
    decoder_dict = {}

    for error in generate_all_errors(H_x.shape[1]):
        decoder_dict[error] = compute_syndrome(H_x, error)

    return decoder_dict

def evaluate_decoder(H_x, H_z, logical_x, decoder_table):
    results = {}

    for error in generate_all_errors(H_x.shape[1]):
        weight = error.count("Z")

        # reveal the syndrome and retrieve its correction
        syndrome = compute_syndrome(H_x, error)

        # retrieve its correction
        correction = error_to_vector(decoder_table[syndrome])

        # convert error string to vector
        err_vector = error_to_vector(error)

        # calculate the residual
        residual = (err_vector + correction) % 2

        # create counters when this weight first appears
        if weight not in results:
            results[weight] = {"success": 0, "failure": 0}

        # check recovery and count successes/failures by weight
        if recovery(H_z, residual, logical_x, H_x):
            results[weight]["success"] += 1
        else:
            results[weight]["failure"] += 1

    return results


def logical_failure_probability(results, p):
    summation = 0

    for weight in results.keys():
        prob_product = math.pow(p, weight) * math.pow(1-p, H_x.shape[1]-weight)
        summation += results[weight]["failure"] * prob_product

    return summation

def logical_success_probability(results, p):
    summation = 0

    for weight in results.keys():
        prob_product = math.pow(p, weight) * math.pow(1-p, H_x.shape[1]-weight)
        summation += results[weight]["success"] * prob_product

    return summation

decoder_table = {}

for error, syndrome in error_to_syndrome(H_x).items():
    decoder_table.setdefault(syndrome, error)


# print(compute_syndrome(H_x, error='ZZIIIIIII'))
# print(decoder_table[compute_syndrome(H_x, error='ZZIIIIIII')])

# c = error_to_vector(decoder_table[compute_syndrome(H_x, error='ZZIIIIIII')])
# e = error_to_vector('ZZIIIIIII')

# r = (e + c) % 2
# print(recovery(H_z, r, logical_x, H_x))

print(evaluate_decoder(H_x, H_z, logical_x, decoder_table))
print("logical failure probability: ", logical_failure_probability(evaluate_decoder(H_x, H_z, logical_x, decoder_table), 0.01))
print("logical success probability: ", logical_success_probability(evaluate_decoder(H_x, H_z, logical_x, decoder_table), 0.01))