import logging

import pprint
import re
from typing import Optional, Dict, List, Any

import click
import click_log

# from linkml_runtime.linkml_model import SchemaDefinition  # ClassDefinition
from linkml_runtime.utils.schemaview import SchemaView

import yaml

logger = logging.getLogger(__name__)
click_log.basic_config(logger)


@click.command()
@click_log.simple_verbosity_option(logger)
@click.option("--left_model", type=click.Path(exists=True), required=True)
@click.option("--right_model", type=click.Path(exists=True), required=True)
@click.option("--yaml_output", type=click.Path(), required=True)
def compare_enums(left_model: str, right_model: str, yaml_output: str):
    """
    Gets slots, listed in config_tsv, from source_model and puts them in recipient_model
    :param left_model:
    :param right_model:
    :param yaml_output:
    :return:
    """

    # todo help for each option
    # todo docstring

    comparison = [left_model, right_model]

    enum_comparison = EnumComparison()
    for i in comparison:
        basename = get_schema_basename(i)
        enum_comparison.add_view(basename, i)
        enum_comparison.get_enum_names(basename)
        enum_comparison.add_comparee(basename)

    enum_comparison.compare_enums()

    final = enum_comparison.ecres

    with open(yaml_output, "w") as outfile:
        yaml.safe_dump(final, outfile, default_flow_style=False)


if __name__ == "__main__":
    compare_enums()


def get_schema_basename(schema_path):
    schema_basename = re.sub(r"^.*/", "", schema_path)
    schema_basename = re.sub(r"\.yaml$", "", schema_basename)
    return schema_basename


def compare_lists(
        left: List, right: List, sort=True, left_name="left", right_name="right"
) -> Dict[str, List[str]]:
    ls = set(left)
    rs = set(right)
    intersection = list(ls.intersection(rs))
    lo = list(ls - rs)
    ro = list(rs - ls)
    if sort:
        intersection.sort()
        lo.sort()
        ro.sort()
    lo_name = onlyify(left_name)
    ro_name = onlyify(right_name)
    return {lo_name: lo, ro_name: ro, "intersection": intersection}


def onlyify(base_string: str) -> str:
    return base_string + "_only"


class EnumComparison:
    def __init__(self):
        self.ecres = Dict[str, Any]
        self.comparison_list: List[str] = []
        self.view_dict: Optional[Dict[str, SchemaView]] = {}
        self.enum_names_dict: Optional[Dict[str, List[str]]] = {}

    def add_comparee(self, comparee):
        self.comparison_list.append(comparee)

    def add_view(self, position, schema_file):
        self.view_dict[position] = SchemaView(schema_file)

    def get_enum_names(self, position):
        positions_enums = self.view_dict[position].all_enums()
        pe_names = [v.name for k, v in positions_enums.items()]
        pe_names.sort()
        self.enum_names_dict[position] = pe_names

    def compare_enums(self):
        left_source_name = self.comparison_list[0]
        lsno = onlyify(left_source_name)
        right_source_name = self.comparison_list[1]
        rsno = onlyify(right_source_name)
        left_enum_names = self.enum_names_dict[left_source_name]
        right_enum_names = self.enum_names_dict[right_source_name]
        comparison_result = compare_lists(
            left_enum_names,
            right_enum_names,
            sort=True,
            left_name=left_source_name,
            right_name=right_source_name,
        )

        self.ecres = {}
        self.ecres["disjoint_enums"] = {}

        self.ecres["disjoint_enums"][lsno] = comparison_result[lsno]
        self.ecres["disjoint_enums"][rsno] = comparison_result[rsno]

        self.ecres["shared_enums"] = {}
        for i in comparison_result["intersection"]:
            left_pvs = list(
                self.view_dict[left_source_name].get_enum(i).permissible_values.keys()
            )
            right_pvs = list(
                self.view_dict[right_source_name].get_enum(i).permissible_values.keys()
            )
            pv_comparison = compare_lists(
                left_pvs,
                right_pvs,
                sort=True,
                left_name=left_source_name,
                right_name=right_source_name,
            )
            self.ecres["shared_enums"][i] = pv_comparison
