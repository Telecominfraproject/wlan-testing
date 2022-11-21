
def standardize_json_results(results):
    '''
    standardize_json_results takes a dict of information retrieved from json_get and standardizes it to use the plural version of
    the data requested. 
    The data is returned starting with the "endpoints"

    TODO: Add functionality to handle other plural vs singular data representations
    '''
    if 'endpoints' not in results: 
        tmp_results = {}
        print(results)
        results = results['endpoint']
        name = results['name']
        tmp_results['endpoints'] = []
        tmp_results['endpoints'].append({results['name']: results})
        results = tmp_results

    return results['endpoints']
