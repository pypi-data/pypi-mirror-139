import logging

# from typing import List, Optional, Dict, Any

import click
import click_log
import pandas as pd

import yaml

from glom import glom, assign
import glom.core as gc

from linkml_runtime.utils.schemaview import SchemaView

import pprint

logger = logging.getLogger(__name__)
click_log.basic_config(logger)


@click.command()
@click_log.simple_verbosity_option(logger)
@click.option("--yaml_input", type=click.Path(exists=True), required=True)
@click.option("--config_tsv", type=click.Path(exists=True), required=True)
@click.option("--yaml_output", type=click.Path(), required=True)
def mod_by_path(yaml_input: str, config_tsv: str, yaml_output: str):
    """
    :param yaml_input:
    :param config_tsv:
    :param yaml_output:
    :return:
    """

    # todo be defensive
    # parameterize?

    meta_view = SchemaView("https://w3id.org/linkml/meta")

    with open(yaml_input, 'r') as stream:
        try:
            schema_dict = yaml.safe_load(stream)
        except yaml.YAMLError as e:
            logger.warning(e)

    mod_rule_frame = pd.read_csv(config_tsv, sep="\t")
    mod_rule_lod = mod_rule_frame.to_dict(orient='records')

    # todo break out overwrites first
    for i in mod_rule_lod:
        base_path = f"classes.{i['class']}.slot_usage.{i['slot']}"
        try:
            logger.info(f"{i['slot']} {i['action']} {i['target']} {i['value']}")
            slot_usage_extract = glom(schema_dict, base_path)
            # update_path = None
            if i['action'] == "replace_attribute" and i['target'] != "" and i['target'] is not None:
                update_path = i['target']
                fiddled_value = i['value']
                from_meta = meta_view.get_slot(i['target'])
                fm_range = from_meta.range
                # update_path in ["identifier", "required", "recommended"]:
                if fm_range == "boolean":
                    fiddled_value = bool(i['value'])
                assign(obj=slot_usage_extract, path=update_path, val=fiddled_value)
            elif i['action'] == "replace_annotation" and i['target'] != "" and i['target'] is not None:
                if "annotations" in slot_usage_extract:
                    update_path = f"annotations.{i['target']}"
                    assign(obj=slot_usage_extract, path=update_path, val=i['value'])
                else:
                    update_path = f"annotations"
                    assign(obj=slot_usage_extract, path=update_path, val={i['target']: i['value']})
            # todo refactor
            elif i['action'] == "add_example" and i['target'] == "examples":
                cv_path = i['target']
                try:
                    current_value = glom(slot_usage_extract, cv_path)
                    current_type = type(current_value)
                    if current_type != list:
                        current_value = list(current_value)
                    current_value.append({'value': i['value']})
                    logger.info(current_value)
                except gc.PathAccessError as e:
                    logger.info(e)
                    current_value = [{'value': i['value']}]
                assign(obj=slot_usage_extract, path=i['target'], val=current_value)
            elif i['action'] == "overwrite_examples" and i['target'] == "examples":
                assign(obj=slot_usage_extract, path=i['target'], val=[{'value': i['value']}])
            elif i['action'] == "add_attribute" and i['target'] != "" and i['target'] is not None:
                cv_path = i['target']
                try:
                    current_value = glom(slot_usage_extract, cv_path)
                    current_type = type(current_value)
                    if current_type != list:
                        current_value = list(current_value)
                    current_value.append(i['value'])
                except gc.PathAccessError as e:
                    logger.debug(e)
                    current_value = [i['value']]
                # logger.info(pprint.pformat(current_value))
                assign(obj=slot_usage_extract, path=cv_path, val=current_value)
            # if update_path:
            #     assign(obj=schema_dict, path=base_path, val=slot_usage_extract)
        except gc.PathAccessError as e:
            logger.warning(e)

    with open(yaml_output, 'w') as outfile:
        yaml.dump(schema_dict, outfile, default_flow_style=False, sort_keys=False)


if __name__ == '__main__':
    mod_by_path()
