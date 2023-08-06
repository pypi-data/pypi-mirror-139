from __future__ import annotations

import logging
import re
from typing import Any, Dict, List

import pandas as pd
from linkml_runtime.utils.schemaview import SchemaView

import pprint

logger = logging.getLogger(__name__)


class ValidationConverter:
    """
    structure for looking up DH datatypes and regular expressions
    based on MIxS string serializations and ranges
    """

    def __init__(self) -> None:
        # parameterize these
        selected_cols = ["from_val", "from_type", "to_type", "to_val"]

        # todo no hard-coding paths!
        raw = pd.read_csv(".cogs/tracked/validation_converter.tsv", sep="\t")

        sc_frame = raw[selected_cols]
        vc_lod = sc_frame.to_dict(orient="records")
        self.vc_dod = {i["from_val"]: i for i in vc_lod}


vc_inst = ValidationConverter()


class LinkML2DataHarmonizer:
    """Class interface that has methods for conversion
    from LinkML to DataHarmonizer interface."""

    def __init__(self, linkml_model_path: str) -> None:
        self.model_sv = SchemaView(linkml_model_path)
        self.range_tally = []
        self.string_ser_tally = []

    def classes(self) -> Any:
        return self.model_sv.all_classes()

    def enums(self) -> Any:
        return self.model_sv.all_enums()

    def table_columns(self) -> List[str]:
        return [
            "Ontology ID",
            "label",
            "parent class",
            "description",
            "guidance",
            "datatype",
            "pattern",
            "requirement",
            "examples",
            "source",
            "capitalize",
            "data status",
            "max value",
            "min value",
            "EXPORT_soil_emsl_jgi_mg",
        ]

    def log_tally(self, tally: List[str], message: str) -> None:
        logger.info(message)
        logger.info(pd.Series(tally).value_counts())
        logger.info("\n")

    def _req_rec_from_slot_usage(self) -> Dict[str, List[str]]:
        """Get Dictionary of required and recommended properties from slot usage."""
        reqs_from_usage = []

        classes = self.classes()
        class_names = list(classes.keys())
        class_names.sort()

        for cc in class_names:
            current_class = classes[cc]
            ccsu = current_class.slot_usage
            ccsu_names = list(ccsu.keys())
            ccsu_names.sort()
            for current_usage in ccsu_names:
                current_row_dict = {
                    "class": cc,
                    "slot": current_usage,
                    "required": ccsu[current_usage].required,
                    "recommended": ccsu[current_usage].recommended,
                }
                reqs_from_usage.append(current_row_dict)

        reqs_from_usage_frame = pd.DataFrame(reqs_from_usage)
        reqs_from_usage_frame["required"] = reqs_from_usage_frame["required"].fillna(
            False
        )
        reqs_from_usage_frame["recommended"] = reqs_from_usage_frame[
            "recommended"
        ].fillna(False)
        req_from_usage = list(
            reqs_from_usage_frame.loc[reqs_from_usage_frame.required, "slot"]
        )
        rec_from_usage = list(
            reqs_from_usage_frame.loc[reqs_from_usage_frame.recommended, "slot"]
        )

        return {"required": req_from_usage, "recommended": rec_from_usage}

    def _get_is_a_struct(
            self, selected_class: str, default_section: str, as_a: str = "dictionary"
    ):
        relevant_slots = self.model_sv.class_induced_slots(selected_class)
        isa_dict = {}
        isa_set = set()

        for i in relevant_slots:
            # block that adds appropriate section names to the data.tsv
            ia_jsonobj = i.annotations
            ijd = ia_jsonobj.__dict__
            if i.annotations and "dh:section_name" in ijd:
                relevant_isa = i.annotations._get("dh:section_name").value
            elif i.is_a:
                relevant_isa = i.is_a
            else:
                relevant_isa = "undef_sect"

            isa_dict[i.name] = relevant_isa
            isa_set.add(relevant_isa)

        if as_a == "set":
            return isa_set

        return isa_dict

    def _get_section_list(self, selected_class: str, default_section: str):
        blank_row = {i: "" for i in self.table_columns()}

        isa_set = self._get_is_a_struct(selected_class, default_section, as_a="set")

        isa_list = list(isa_set)
        isa_list = [i for i in isa_list if i]
        isa_list.sort()
        section_list = []
        for i in isa_list:
            current_row = blank_row.copy()
            current_row["label"] = i
            section_list.append(current_row)

        return section_list

    def _get_term_pv_list(
            self,
            selected_class: str,
            default_section: str,
            default_source: str,
            default_capitalize: str,
            default_data_status: str,
    ):
        blank_row = {i: "" for i in self.table_columns()}

        isa_dict = self._get_is_a_struct(selected_class, default_section)

        term_names = list(isa_dict.keys())
        term_names.sort()
        term_list = []
        pv_list = []

        relevant_slots = self.model_sv.class_induced_slots(selected_class)
        rs_names = [i.name for i in relevant_slots]
        rs_dict = dict(zip(rs_names, relevant_slots))

        model_enum_names = list(self.enums().keys())
        model_enum_names.sort()

        for i in term_names:
            logger.info(f"processing {i}")
            current_row = blank_row.copy()
            current_sd = rs_dict[i]

            current_row["Ontology ID"] = current_sd.slot_uri
            if current_sd.title is not None and len(current_sd.title) > 0:
                current_row["label"] = current_sd.title
            else:
                current_row["label"] = current_sd.name

            # useless parent classes:  attribute, <default>,
            current_row["parent class"] = isa_dict[i]

            # description: quote and or bracket wrappers, TODO, empty
            if current_sd.description is None:
                pass
            else:
                # these are of type linkml_runtime.utils.yamlutils.extended_str
                # even though GOLD sample identifiers ['identifiers for corresponding sample in GOLD'] looks like a list
                # current_row["description"] = current_sd.description[0]
                temp = current_sd.description
                temp = re.sub(r"^[\['\"]*", "", temp)
                temp = re.sub(r"['\]\"]*$", "", temp)
                current_row["description"] = temp

            # block that adds column information to the data.tsv
            # the int() is necessary to convert the column number from str type to int so
            # pandas can sort
            try:
                current_row["column_number"] = int(
                    current_sd.annotations._get("dh:column_number").value
                )
            except AttributeError:
                logger.info(f"No annotations associated with slot {current_sd.name}")
                pass

            # guidance: I have moved slot used in...  out of the MIxS comments
            #  Occurrence is still in there
            #   ~ half of the MixS soil/NMDC biosample fields lack comments for "guidance"
            #   Montana provides her own, to be concatenated on
            #   Damion's latest LinkML -> JS approach lays the comments and examples out nicer
            current_row["guidance"] = " | ".join(current_sd.comments)

            # todo refactor
            current_row["datatype"] = "xs:token"

            if current_sd.pattern is not None and current_sd.pattern != "":
                if (
                        current_row["guidance"] is not None
                        and current_row["guidance"] != ""
                ):
                    current_row["guidance"] = (
                            current_row["guidance"]
                            + " | pattern as regular expression: "
                            + current_sd.pattern
                    )
                else:
                    current_row["guidance"] = (
                            "pattern as regular expression: " + current_sd.pattern
                    )

            if (
                    current_sd.string_serialization is not None
                    and current_sd.string_serialization != ""
            ):
                if (
                        current_row["guidance"] is not None
                        and current_row["guidance"] != ""
                ):
                    current_row["guidance"] = (
                            current_row["guidance"]
                            + " | Pattern hint: "
                            + current_sd.string_serialization
                    )
                else:
                    current_row["guidance"] = (
                            "Pattern hint: " + current_sd.string_serialization
                    )
                # if current_sd.string_serialization == '{float}':
                #     current_row["datatype"] = "xs:decimal"
            # todo map types
            # don't forget selects and multis
            # map selects to terms and indent
            self.range_tally.append(current_sd.range)

            if (
                    current_sd.string_serialization is not None
                    and current_sd.string_serialization != ""
            ):
                self.string_ser_tally.append(current_sd.string_serialization[0:99])
            else:
                self.string_ser_tally.append("<none>")

            current_row["pattern"] = current_sd.pattern

            # if (current_sd.pattern is None or current_sd.pattern == "") and current_sd.range == "quantity value":
            #     current_row["pattern"] = q_val_pattern
            # todo check for numeric but don't force float when int will do?
            if current_sd.minimum_value is not None and current_sd.minimum_value != "":
                current_row["min value"] = current_sd.minimum_value

            if current_sd.maximum_value is not None and current_sd.maximum_value != "":
                current_row["max value"] = current_sd.maximum_value

            if current_sd.range in vc_inst.vc_dod:
                temp = vc_inst.vc_dod[current_sd.range]['to_val']
                if vc_inst.vc_dod[current_sd.range]['to_type'] == 'DH datatype':
                    current_row["datatype"] = temp
                if vc_inst.vc_dod[current_sd.range]['to_type'] == 'DH pattern regex':
                    current_row["pattern"] = temp

            if current_sd.string_serialization in vc_inst.vc_dod:
                temp = vc_inst.vc_dod[current_sd.string_serialization]['to_val']
                if vc_inst.vc_dod[current_sd.string_serialization]['to_type'] == 'DH datatype':
                    current_row["datatype"] = temp
                if vc_inst.vc_dod[current_sd.string_serialization]['to_type'] == 'DH pattern regex':
                    current_row["pattern"] = temp

            if current_sd.range in model_enum_names:
                # anything else to clear?
                current_row["pattern"] = ""
                # update this once the enums are built
                if current_sd.multivalued:
                    current_row["datatype"] = "multiple"
                    logger.info(f"    {i} is multi-valued")
                else:
                    current_row["datatype"] = "select"

                model_enums = self.enums()
                pvs_obj = model_enums[current_sd.range].permissible_values
                pv_keys = list(pvs_obj.keys())
                pv_keys.sort()
                for pvk in pv_keys:
                    pv_row = blank_row.copy()
                    pv_row["label"] = pvk
                    if current_sd.title:
                        pv_row["parent class"] = current_sd.title
                    else:
                        pv_row["parent class"] = current_sd.name
                    # use term meaning as ontology ID if possible
                    pv_row["Ontology ID"] = pvs_obj[pvk].meaning
                    pv_list.append(pv_row)

            req_rec_dict = self._req_rec_from_slot_usage()

            if current_sd.recommended or current_sd.name in req_rec_dict["recommended"]:
                current_row["requirement"] = "recommended"
            elif current_sd.required or current_sd.name in req_rec_dict["required"]:
                current_row["requirement"] = "required"

            example_list = []
            for exmpl in current_sd.examples:
                # ignoring description which always seems to be None
                if exmpl.value is not None and len(exmpl.value) > 0:
                    example_list.append(exmpl.value)
                    example_cat = "|".join(example_list)
                    current_row["examples"] = example_cat

            current_row["source"] = default_source  # for reuse of enums?
            current_row["capitalize"] = default_capitalize
            current_row["data status"] = default_data_status
            # any other ways to infer min or max, as a supplement to the datatypes?
            current_row["max value"] = current_sd.maximum_value
            current_row["min value"] = current_sd.minimum_value
            # old issue... export menu saves a file but not with the briefer LinkML names (as opposed to titles)
            current_row["EXPORT_soil_emsl_jgi_mg"] = current_sd.name

            if current_sd.identifier:
                current_row["datatype"] = "xs:unique"
                current_row["requirement"] = "required"

            term_list.append(current_row)
        logger.info("\n")

        return {"term": term_list, "pv": pv_list}

    def _combined_list(
            self,
            section_list: List[str],
            term_list: List[str],
            pv_list: List[str],
            selected_class: str,
            default_section: str,
    ):
        # column ordering
        tl_temp_frame = pd.DataFrame(term_list)
        tltf_sorted = tl_temp_frame.groupby("parent class").apply(
            pd.DataFrame.sort_values, "column_number"
        )

        term_list = tltf_sorted.to_dict(orient='records')

        sl_temp_frame = pd.DataFrame(section_list)

        section_record_list = []
        dh_section_name = self.model_sv.class_children('nmdc_dh_section')
        for current_dhs in dh_section_name:
            current_dhs_obj = self.model_sv.get_class(current_dhs)
            sect_ord_anno = current_dhs_obj.annotations['dh_sect_ord'].value
            section_record_list.append({'section': current_dhs, 'order': sect_ord_anno, "title": current_dhs})
        section_frame = pd.DataFrame(section_record_list)

        sections_with_orders = sl_temp_frame.merge(right=section_frame, how="left", left_on="label", right_on="section")

        sections_with_orders['order'] = sections_with_orders['order'].fillna(999)
        sections_with_orders['order'] = sections_with_orders['order'].astype(int)
        sections_with_orders.sort_values('order', inplace=True)
        section_list = sections_with_orders.to_dict(orient='records')

        final_list = section_list + term_list + pv_list
        final_frame = pd.DataFrame(final_list)

        final_frame.drop(['section', 'order', 'title', 'column_number'], axis=1, inplace=True)

        self.log_tally(
            self.range_tally,
            "TABULATION OF SLOT RANGES, for prioritizing range->regex conversion",
        )
        self.log_tally(
            self.string_ser_tally,
            "TABULATION OF STRING SERIALIZATIONS, for prioritizing serialization->regex conversion",
        )

        return final_frame
