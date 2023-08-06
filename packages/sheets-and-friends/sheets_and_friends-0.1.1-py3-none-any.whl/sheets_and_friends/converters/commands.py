import logging

import click
import click_log
import pandas as pd

from linkml_runtime.utils.schemaview import SchemaView

from sheets_and_friends.converters.linkml2dataharmonizer import (
    LinkML2DataHarmonizer,
    # ValidationConverter,
)
from sheets_and_friends.converters.sheet2linkml import Sheet2LinkML
import pprint

logger = logging.getLogger(__name__)
click_log.basic_config(logger)


@click.command()
@click_log.simple_verbosity_option(logger)
@click.option("--model_file", type=click.Path(exists=True), required=True)
@click.option("--selected_class", required=True)
@click.option("--default_section", default="default", show_default=True)
@click.option("--default_source", default="", show_default=True)
@click.option("--default_capitalize", default="", show_default=True)
@click.option("--default_data_status", default="", show_default=True)
@click.option(
    "--output_file", type=click.Path(), default="target/data.tsv", show_default=True
)
def linkml2dataharmonizer(
        model_file,
        selected_class,
        default_section,
        default_source,
        default_capitalize,
        default_data_status,
        output_file,
):
    lml_dh = LinkML2DataHarmonizer(linkml_model_path=model_file)

    section_list = lml_dh._get_section_list(selected_class, default_section)
    term_pv_dict = lml_dh._get_term_pv_list(
        selected_class,
        default_section,
        default_source,
        default_capitalize,
        default_data_status,
    )

    term_list = term_pv_dict["term"]
    pv_list = term_pv_dict["pv"]

    consolidated_list = lml_dh._combined_list(
        section_list, term_list, pv_list, selected_class, default_section
    )

    if output_file:
        consolidated_list.to_csv(output_file, sep="\t", index=False)
    else:
        click.echo(consolidated_list)


@click.command()
@click_log.simple_verbosity_option(logger)
@click.option("--model_file", type=click.Path(exists=True), required=True)
@click.option("--output_file", type=click.Path(), required=True)
def mixs_package_map(model_file, output_file):
    mixs_view = SchemaView(model_file)
    # should be "MIxS"
    # logger.info(mixs_view.schema.name)

    mixs_classes = mixs_view.all_classes()
    mixs_class_names = list(mixs_classes.keys())
    mixs_class_names.sort()
    blank_class_row = {
        "class_name": None,
        "is_a_parent": None,
        "is_mixin": False,
        "mixins_used": None,
    }
    class_row_list = []

    for current_class_name in mixs_class_names:
        # logger.info(current_class_name)
        current_cd = mixs_view.get_class(current_class_name)
        # current_is_a = current_cd.is_a
        current_mixin_flag = current_cd.mixin
        mixins_used = current_cd.mixins
        # logger.info(f"{i}\t{current_is_a}\t{current_mixin_flag}\t{mixins_used}")
        current_row = blank_class_row.copy()
        current_row["class_name"] = current_class_name

        if current_cd.is_a is not None:
            current_row["is_a_parent"] = str(current_cd.is_a)

        if current_mixin_flag:
            current_row["is_mixin"] = True
        # current_row['mixins_used'] = str(mixins_used)
        current_row["mixins_used"] = "|".join(mixins_used)
        class_row_list.append(current_row)

    mixs_class_frame = pd.DataFrame(class_row_list)
    # logger.info(mixs_class_frame)
    # for now, it looks like all is_a parents of any other class are the packages

    package_classes = list(mixs_class_frame["is_a_parent"].drop_duplicates())
    package_classes = [
        current_class for current_class in package_classes if current_class is not None
    ]
    package_classes.sort()
    # logger.info(package_classes)

    # env_package_pvs = mixs_view.get_enum('env_package_enum').permissible_values
    # ep_pvs_names = list(env_package_pvs.keys())
    # ep_pvs_names.sort()
    # logger.info(ep_pvs_names)

    mims_package_classes = mixs_class_frame["class_name"].loc[
        mixs_class_frame["mixins_used"].eq("MIMS")
        & mixs_class_frame["is_a_parent"].isin(package_classes)
        ]
    mims_package_classes = list(mims_package_classes)
    mims_package_classes.sort()

    selected_classes = [
        "built environment",
        "microbial mat_biofilm",
        "miscellaneous natural or artificial environment",
        "plant-associated",
        "sediment",
        "soil",
        "wastewater_sludge",
        "water",
    ]

    blank_slot_row = {"class_name": None, "slot_name": None, "disposition": None}
    slot_row_list = []
    for current_pc_name in selected_classes:
        # logger.info(current_pc_name)
        induceds = mixs_view.class_induced_slots(current_pc_name)
        induceds_names = [ci.name for ci in induceds]
        induceds_names.sort()

        for current_induced in induceds_names:
            # logger.info(f"{current_pc_name} {current_induced}")
            current_slot_row = blank_slot_row.copy()
            current_slot_row["class_name"] = current_pc_name
            current_slot_row["slot_name"] = current_induced
            slot_row_list.append(current_slot_row)

    slot_frame = pd.DataFrame(slot_row_list)
    # logger.info(slot_frame)
    slot_frame.to_csv(output_file, sep="\t", index=False)


@click.command()
@click_log.simple_verbosity_option(logger)
@click.option("--model_file", type=click.Path(exists=True), required=True)
@click.option("--selected_class", required=True)
@click.option(
    "--output_file", type=click.Path(), default="target/data.tsv", show_default=True
)
def range_str_ser(model_file, selected_class, output_file):
    # model_file = "target/soil_biosample_modular_annotated.yaml"
    # selected_class = "soil_biosample"
    # soil_biosample_regex_insight.tsv

    row_list = []

    sb_view = SchemaView(model_file)
    sb_class = sb_view.get_class(selected_class)
    sb_slots = sb_class.slots
    sb_slots.sort()
    sb_enums = sb_view.all_enums()
    sb_enum_names = list(sb_enums.keys())

    for i in sb_slots:
        i_struct = sb_view.get_slot(i)
        elements = ["name", "title", "string_serialization", "range"]
        row_dict = {}
        for j in elements:
            row_dict[j] = i_struct[j]
        row_dict["enum_range"] = False
        row_dict["enum_string_ser"] = False
        row_dict["enum_discrepancy"] = False
        # row_dict['enum_conflict'] = False
        if i_struct.range in sb_enum_names:
            row_dict["enum_range"] = True
        if row_dict["string_serialization"] == "enumeration":
            row_dict["enum_string_ser"] = True
        row_dict["enum_discrepancy"] = (
                row_dict["enum_range"] != row_dict["enum_string_ser"]
        )
        row_list.append(row_dict)

    row_frame = pd.DataFrame(row_list)
    row_frame.to_csv(output_file, sep="\t", index=False)


@click.command()
@click_log.simple_verbosity_option(logger)
@click.option(
    "--client_secret",
    default="local/client_secret_fresh-sheet2linkml.apps.googleusercontent.com.json",
    type=click.Path(exists=True),
    help="path your google sheet authentication file",
    show_default=True,
)
@click.option(
    "--sheet_id",
    default="1WErXj8sM5uJi51VVLNQZDilDF7wMiyBC2T4zELp7Axc",
    help="ID of the google sheet that will provide the curated enums",
    show_default=True,
)
@click.option(
    "--tab_title",
    default="Subset_EnvO_Broad_Local_Medium_terms_062221",
    help="which tab in the google sheet will provide the curated enums?",
    show_default=True,
)
@click.option(
    "--curated_tsv_out",
    default="target/tidy_triad_curations.tsv",
    type=click.Path(),
    help="destination for modified data.tsv",
    show_default=True,
)
@click.option(
    "--env_package",
    default="soil",
    help="""for which environmental packages (as expressed in the google sheet) 
              do you want do extract curated enums??""",
)
def tidy_triad_curations(
        client_secret, sheet_id, tab_title, curated_tsv_out, env_package
):
    raw = Sheet2LinkML.get_gsheet_frame(client_secret, sheet_id, tab_title)

    # raw.columns = ["enum", "raw_id", "permissible_value", "definition", "env_package"]
    #
    # raw["partial"] = raw["raw_id"].str.replace(
    #     "<http://purl.obolibrary.org/obo/ENVO_", "ENVO:", regex=True
    # )
    #
    # raw["term_id"] = raw["partial"].str.replace(">", "", regex=True)
    #
    # raw = raw[["env_package", "enum", "permissible_value", "term_id"]]
    #
    # raw["env_package"] = raw["env_package"].str.split("|", expand=False)

    raw["env_package"] = raw["packages_consensus"].str.split("|", expand=False)

    df_explode = raw.explode("env_package")

    df_explode = df_explode.loc[df_explode["env_package"].eq(env_package)]

    # logger.info(df_explode)

    # df_explode["env_package"] = df_explode["env_package"].str.lower()

    df_explode.to_csv(curated_tsv_out, sep="\t", index=False)


@click.command()
@click_log.simple_verbosity_option(logger)
@click.option(
    "--data_tsv_in",
    default="target/data.tsv",
    type=click.Path(exists=True),
    help="path to DataHarmonizer data.tsv input",
    show_default=True,
)
@click.option(
    "--data_tsv_out",
    default="target/data_promoted.tsv",
    type=click.Path(),
    help="destination for modified data.tsv",
    show_default=True,
)
@click.option(
    "--promote", multiple=True, help="which columns should be promoted to select type?"
)
@click.option(
    "--extra_row_files",
    multiple=True,
    type=click.Path(exists=True),
    help="path to files defining the new select/enum column(s) etc.",
    show_default=True,
)
def promote_to_select(data_tsv_in, data_tsv_out, promote, extra_row_files):
    data_in = pd.read_csv(data_tsv_in, sep="\t")
    for i in promote:
        logger.info(i)
        data_in.loc[data_in["label"].eq(i), "datatype"] = "select"
        data_in.loc[data_in["label"].eq(i), "pattern"] = ""
    to_concat = [data_in]
    for i in extra_row_files:
        logger.info(i)
        temp = pd.read_csv(i, sep="\t")
        to_concat.append(temp)
    catted = pd.concat(to_concat)
    catted.to_csv(data_tsv_out, sep="\t", index=False)
