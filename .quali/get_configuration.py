import json
import sys

from cloudshell.api.cloudshell_api import UpdateTopologyGlobalInputsRequest, UpdateTopologyRequirementsInputsRequest

from common import get_session

def main():
    session = get_session()
    res_id = sys.argv[1]

    reservation_details = session.GetReservationDetails(res_id).ReservationDescription
    resources_in_reservation = reservation_details.Resources

    config = {}

    for resource in resources_in_reservation:
        if resource.ResourceModelName == 'Ap':
            section = 'access_point'
        elif resource.ResourceModelName == 'Trafficgenerator':
            section = 'traffic_generator'
        else:
            continue

        config[section] = {}
        details = session.GetResourceDetails(resource.Name)

        for attribute in details.ResourceAttributes:
            key = attribute.Name.replace(f"{resource.ResourceModelName}.", '')
            if attribute.Type == 'Boolean':
                value = True if attribute.Value == 'True' else False
            elif attribute.Type == 'Numeric':
                value = int(attribute.Value)
            else:
                value = attribute.Value

            config[section][key] = value

    print(json.dumps(config))

if __name__ == '__main__':
    main()
