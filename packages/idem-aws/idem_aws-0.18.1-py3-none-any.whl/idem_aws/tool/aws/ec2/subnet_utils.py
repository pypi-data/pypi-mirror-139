from collections import OrderedDict
from typing import Any
from typing import Dict


def convert_raw_subnet_to_present(
    hub, raw_resource: Dict[str, Any], idem_resource_name: str = None
) -> Dict[str, Any]:
    resource_id = raw_resource.get("SubnetId")
    resource_parameters = OrderedDict(
        {
            "VpcId": "vpc_id",
            "CidrBlock": "cidr_block",
            "AvailabilityZone": "availability_zone",
            "OutpostArn": "outpost_arn",
            "Tags": "tags",
        }
    )
    resource_translated = {"name": idem_resource_name, "resource_id": resource_id}
    for parameter_raw, parameter_present in resource_parameters.items():
        if parameter_raw in raw_resource:
            resource_translated[parameter_present] = raw_resource.get(parameter_raw)
    if (not raw_resource.get("AvailabilityZone")) and raw_resource.get(
        "AvailabilityZoneId"
    ):
        # Only populate availability_zone_id field when availability_zone doesn't exist
        resource_translated["availability_zone_id"] = raw_resource.get(
            "AvailabilityZoneId"
        )
    if raw_resource.get("Ipv6CidrBlockAssociationSet"):
        ipv6_cidr_block_association_set = (
            hub.tool.aws.network_utils.get_associated_ipv6_cidr_blocks(
                raw_resource.get("Ipv6CidrBlockAssociationSet")
            )
        )
        # We should only output the associated ipv6 cidr block, and theoretically there should only be one,
        # since AWS only supports one ipv6 cidr block association on a subnet
        if ipv6_cidr_block_association_set:
            resource_translated["ipv6_cidr_block"] = ipv6_cidr_block_association_set[
                0
            ].get("Ipv6CidrBlock")
    return resource_translated
