import json
import yaml
import sys
import boto3

SSM = boto3.client('ssm')


def make_parameter_file(env):
    # from SSM
    function_args = {
        'Path': f'/{env}/lambda',
        'Recursive': True,
        'WithDecryption': True,
        'MaxResults': 10,
    }

    response = SSM.get_parameters_by_path(**function_args)
    current_batch, next_token = extract_result(response)

    result = current_batch

    while next_token is not None:
        function_args['NextToken'] = next_token
        response = SSM.get_parameters_by_path(**function_args)
        current_batch, next_token = extract_result(response)
        result += current_batch

    cfn_parameters_from_ssm = \
        {extract_parameter_name(parameter): convert_to_ssm_cfn_parameters(parameter) for parameter in result}

    # from fixed value
    with open(f'environments/{env}-fixed-variables.json', 'r') as file:
        fixed_values = json.load(file)
        cfn_parameters_from_fixed = \
            {parameter['Name']: convert_to_fixed_cfn_parameters(parameter) for parameter in fixed_values}

    cfn_parameters_yaml = {
        'Parameters': {**cfn_parameters_from_ssm, **cfn_parameters_from_fixed}
    }
    dumped = yaml.dump(cfn_parameters_yaml, default_flow_style=False, allow_unicode=True)
    with open(f'templates/{env}_lambda_common_parameters.yaml', 'w') as file:
        file.write(dumped)
    print(dumped)


def extract_result(parameter_store_response):
    parameters = parameter_store_response['Parameters']
    next_token = parameter_store_response.get('NextToken', None)
    return parameters, next_token


def extract_parameter_name(ssm_parameter_name):
    return ssm_parameter_name['Name'].split('/')[-1]


def convert_to_ssm_cfn_parameters(ssm_parameter):
    return {
        'Type': 'AWS::SSM::Parameter::Value<String>',
        'Default': ssm_parameter['Name']
    }


def convert_to_fixed_cfn_parameters(fixed_parameter):
    return {
        'Type': 'String',
        'Default': fixed_parameter['Value']
    }


if __name__ == '__main__':
    make_parameter_file(sys.argv[1])
