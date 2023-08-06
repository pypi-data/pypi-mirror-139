from re import fullmatch

from click import BadParameter

def regex_valid(regex, error_message = 'Invalid Input'):
    def regex_fullmatch(ctx, param, value):
        if fullmatch(regex, value):
            return value
        raise BadParameter(error_message, ctx, param)
    return regex_fullmatch


def data_validations(original_df, weights, impacts):
    if original_df.shape[1] < 3:
        raise Exception('Atleast 3 Columns Required.')

    if original_df.shape[1] - 1 == len(weights) == len(impacts):
        pass

    else:
        raise Exception('Weights, Impacts and Comparison Columns must be of same length.')
