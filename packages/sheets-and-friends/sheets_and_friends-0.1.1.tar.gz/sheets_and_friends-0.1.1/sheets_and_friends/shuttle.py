import logging

from typing import List, Optional, Dict, Any

import click
import click_log

import pandas as pd

from linkml_runtime.linkml_model import (
    SchemaDefinition,
    ClassDefinition,
)

from linkml_runtime.utils.schemaview import SchemaView

from linkml_runtime.dumpers import yaml_dumper
import pprint

logger = logging.getLogger(__name__)
click_log.basic_config(logger)


@click.command()
@click_log.simple_verbosity_option(logger)
@click.option("--recipient_model", type=click.Path(exists=True), required=True)
@click.option("--config_tsv", type=click.Path(exists=True), required=True)
@click.option("--yaml_output", type=click.Path(), required=True)
def do_shuttle(recipient_model: str, config_tsv: str, yaml_output: str):
    """
    Gets slots, listed in config_tsv, from source_model and puts them in recipient_model
    :param recipient_model:
    :param config_tsv:
    :param yaml_output:
    :return:
    """

    shuttle = Shuttle()
    shuttle.tsv_file = config_tsv
    shuttle.recipient_model_fp = recipient_model
    shuttle.get_slots_from_tsv()
    shuttle.prepare_dest_schema()
    shuttle.get_unique_source_files()
    shuttle.prep_transactions_dict()
    shuttle.prep_views_dict()
    shuttle.extract_dest_class_names()
    shuttle.yaml_output = yaml_output
    shuttle.shuttle_slots()
    shuttle.write_schema()


if __name__ == '__main__':
    do_shuttle()


class Shuttle:
    def __init__(self):
        self.yaml_output: Optional[str] = None
        self.destination_class_names: Optional[List[str]] = None
        self.recipient_model_fp: Optional[str] = None
        self.destination_schema: Optional[SchemaDefinition] = None
        self.slots_frame: Optional[pd.DataFrame] = None
        self.slots_lod: Optional[List[Dict[str, Any]]] = None
        self.source_schema_files: Optional[List[str]] = None
        # todo MAM be more specific
        self.sources_first: Optional[Dict[str, Any]] = {}
        self.tsv_file: Optional[str] = None
        self.views_dict: Optional[Dict[str, Any]] = {}

    def get_slots_from_tsv(self):
        slots_frame = pd.read_csv(self.tsv_file, sep="\t")
        self.slots_lod = slots_frame.to_dict(orient='records')

    def prepare_dest_schema(self):
        current_view = SchemaView(self.recipient_model_fp)
        self.destination_schema = current_view.schema

    def get_unique_source_files(self):
        schema_files = [i['source file or URL'] for i in self.slots_lod]
        schema_files = list(set(schema_files))
        schema_files.sort()
        self.source_schema_files = schema_files

    def prep_transactions_dict(self):
        self.sources_first = {}
        for i in self.slots_lod:
            source_designator = i['source file or URL']
            if source_designator not in self.sources_first:
                self.sources_first[source_designator] = {}
                self.sources_first[source_designator]['transactions'] = []
            self.sources_first[source_designator]['transactions'].append(i)

    def prep_views_dict(self):
        self.views_dict = {}
        for k, v in self.sources_first.items():
            temp = SchemaView(k)
            self.views_dict[k] = temp

    def extract_dest_class_names(self):
        destination_classes = self.destination_schema.classes
        destination_class_names = list(destination_classes.keys())
        destination_class_names.sort()
        self.destination_class_names = destination_class_names

    def shuttle_slots(self):
        for k, v in self.sources_first.items():
            logger.info(k)
            current_view = self.views_dict[k]
            for i in v['transactions']:
                logger.info(i)
                current_slot = current_view.induced_slot(slot_name=i['slot'], class_name=i['source class'])
                # current_yaml = yaml_dumper.dumps(current_slot)
                # print(current_yaml)
                desired_class_name = i['destination class']
                if desired_class_name not in self.destination_class_names:
                    new_class = ClassDefinition(name=desired_class_name)
                    self.destination_schema.classes[desired_class_name] = new_class

                desired_slot_name = i['slot']

                class_shortcut = self.destination_schema.classes[desired_class_name]
                self.destination_schema.slots[desired_slot_name] = current_slot
                class_shortcut.slots.append(desired_slot_name)
                class_shortcut.slot_usage[desired_slot_name] = current_slot

    def write_schema(self):
        yaml_dumper.dump(self.destination_schema, to_file=self.yaml_output)
