"""Sample code to get all OUs in AWS Organizations"""
import boto3
from botocore.exceptions import ClientError


def get_org_root_id() -> str:
    """Get AWS Organizations root id"""
    orgs_client = boto3.client("organizations")
    try:
        response_roots = orgs_client.list_roots()
        org_root_id = response_roots["Roots"][0]["Id"]
    except ClientError as error:
        print(error)
    return org_root_id


def get_child_ous(root_or_ou_id: str) -> list:
    """Get child ous for parent ou recursively"""
    child_ous = []
    orgs_client = boto3.client("organizations")
    try:
        response = orgs_client.list_organizational_units_for_parent(
            ParentId=root_or_ou_id
        )
        child_ous.extend(response["OrganizationalUnits"])
        while "NextToken" in response:
            response = orgs_client.list_organizational_units_for_parent(
                ParentId=root_or_ou_id, NextToken=response["NextToken"]
            )
            child_ous.extend(response["OrganizationalUnits"])
        for child_ou in child_ous:
            print(f"child_ou name is {child_ou['Name']}")
            child_ous.extend(get_child_ous(child_ou["Id"]))
    except ClientError as error:
        print(error)
    return child_ous


if __name__ == "__main__":
    root_id = get_org_root_id()
    all_ous = get_child_ous(root_id)
    print(f"There are {len(all_ous)} in Organzations")
    for ou in all_ous:
        print(ou["Name"])
