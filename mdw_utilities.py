# Heiko Maerz MetadataWorks
# heiko@metadataworks.co.uk
# stuff used over and Over AND OVER again

# load packages
import copy
import datetime
import os
import pandas as pd
import requests
import json

# global variables
__version__ = '20201030_1751'


# timestamp
def write_timestamp(out_text=''):
    now = datetime.datetime.now().strftime("%Y/%m/%d %-H:%M:%S")
    print(f"{now} {out_text}")
    return


def get_json(json_uri):
    if isinstance(json_uri, dict):
        return json_uri
    elif os.path.isfile(json_uri):
        with open(json_uri, 'r') as json_file:
            return json.load(json_file)
    elif json_uri.startswith('http'):
        return requests.get(json_uri).json()
    else:
        raise Exception


def export_json(data, filename, indent=2):
    with open(filename, 'w') as jsonfile:
        json.dump(data, jsonfile, indent=indent)


# write excel
def write_excel(fname, worksheets, idx=False):
    '''
    Write a number of worksheets to an Excel File
    :param fname: file path and file name
    :param worksheets: dictionary: {(worksheet name): (worksheet DataFrame), ...}
    :param idx: Boolean, save DataFrame indes to Excel, default False
    :return: None yet
    '''
    with pd.ExcelWriter(fname) as writer:
        for sheetname, df_worksheet in worksheets.items():
            df_worksheet.to_excel(writer, sheet_name=sheetname, index=idx)


def strip_string_to_alphanum(text_in):
    if not isinstance(text_in, str):
        return text_in

    text_out = ''
    for c in text_in:
        if c.isalnum():
            text_out = f"{text_out}{c}"
        elif c in (' ', '-', '_', '.', ','):
            text_out = f"{text_out}_"
    return text_out.strip()


def read_publisher(text_in):
    text_out = str(text_in)
    tokens = text_out.split('>')
    if len(tokens) < 2:
        return text_out.strip()
    return tokens[-1].strip()


def base_v2_json():
    return copy.deepcopy({'identifier': None,
                          'summary': {'title': None,
                                      'abstract': None,
                                      'contactPoint': None,
                                      'keywords': None,
                                      'doiName': None,
                                      'publisher': {'name': None,
                                                    'contactPoint': None,
                                                    'memberOf': None,
                                                    },
                                      },
                          'documentation': {'description': None,
                                            'associatedMedia': None,
                                            'isPartOf': None,
                                            },
                          'coverage': {'spatial': None,
                                       'typicalAgeRange': None,
                                       'physicalSampleAvailability': None,
                                       'followup': None,
                                       'pathway': None,
                                       },
                          'provenance': {'origin': {'purpose': None,
                                                    'source': None,
                                                    'collectionSituation': None,
                                                    },
                                         'temporal': {'accrualPeriodicity': None,
                                                      'distributionReleaseDate': None,
                                                      'startDate': None,
                                                      'endDate': None,
                                                      'timeLag': None,
                                                      },
                                         },

                          'accessibility': {'usage': {'dataUseLimitation': None,
                                                      'dataUseRequirements': None,
                                                      'resourceCreator': None,
                                                      'investigations': None,
                                                      'isReferencedBy': None,
                                                      },
                                            'access': {'accessRights': None,
                                                       'accessService': None,
                                                       'accessRequestCost': None,
                                                       'deliveryLeadTime': None,
                                                       'jurisdiction': None,
                                                       'dataController': None,
                                                       'dataProcessor': None,
                                                       },
                                            'formatAndStandards': {'vocabularyEncodingScheme': None,
                                                                   'conformsTo': None,
                                                                   'language': None,
                                                                   'format': None,
                                                                   },
                                            },
                          'enrichmentAndLinkage': {'qualifiedRelation': None,
                                                   'derivation': None,
                                                   'tools': None, },
                          })


def base_v2_reporting():
    return copy.deepcopy({'identifier': 'U',
                          'summary/title': 'U',
                          'summary/abstract': 'U',
                          'summary/contactPoint': 'U',
                          'summary/keywords': 'U',
                          'summary/doiName': 'U',
                          'summary/publisher/name': 'U',
                          'summary/publisher/contactPoint': 'U',
                          'summary/publisher/memberOf': 'U',
                          'documentation/description': 'U',
                          'documentation/associatedMedia': 'U',
                          'documentation/isPartOf': 'U',
                          'coverage/spatial': 'U',
                          'coverage/typicalAgeRange': 'U',
                          'coverage/physicalSampleAvailability': 'U',
                          'coverage/followup': 'U',
                          'coverage/pathway': 'U',
                          'provenance/origin/purpose': 'U',
                          'provenance/origin/source': 'U',
                          'provenance/origin/collectionSituation': 'U',
                          'provenance/temporal/accrualPeriodicity': 'U',
                          'provenance/temporal/distributionReleaseDate': 'U',
                          'provenance/temporal/startDate': 'U',
                          'provenance/temporal/endDate': 'U',
                          'provenance/temporal/timeLag': 'U',
                          'accessibility/usage/dataUseLimitation': 'U',
                          'accessibility/usage/dataUseRequirements': 'U',
                          'accessibility/usage/resourceCreator': 'U',
                          'accessibility/usage/investigations': 'U',
                          'accessibility/usage/isReferencedBy': 'U',
                          'accessibility/access/accessRights': 'U',
                          'accessibility/access/accessService': 'U',
                          'accessibility/access/accessRequestCost': 'U',
                          'accessibility/access/deliveryLeadTime': 'U',
                          'accessibility/access/jurisdiction': 'U',
                          'accessibility/access/dataController': 'U',
                          'accessibility/access/dataProcessor': 'U',
                          'accessibility/formatAndStandards/vocabularyEncodingScheme': 'U',
                          'accessibility/formatAndStandards/conformsTo': 'U',
                          'accessibility/formatAndStandards/language': 'U',
                          'accessibility/formatAndStandards/format': 'U',
                          'enrichmentAndLinkage/qualifiedRelation': 'U',
                          'enrichmentAndLinkage/derivation': 'U',
                          'enrichmentAndLinkage/tools': 'U',
                          'technicalMetadata': 'U', })


def base_v2_dmd():
    return copy.deepcopy({'identifier': [],
                          'uuid': [],
                          'summary/title': [],
                          'summary/abstract': [],
                          'summary/contactPoint': [],
                          'summary/keywords': [],
                          'summary/doiName': [],
                          'summary/publisher/name': [],
                          'summary/publisher/contactPoint': [],
                          'summary/publisher/memberOf': [],
                          'documentation/description': [],
                          'documentation/associatedMedia': [],
                          'documentation/isPartOf': [],
                          'coverage/spatial': [],
                          'coverage/typicalAgeRange': [],
                          'coverage/physicalSampleAvailability': [],
                          'coverage/followup': [],
                          'coverage/pathway': [],
                          'provenance/origin/purpose': [],
                          'provenance/origin/source': [],
                          'provenance/origin/collectionSituation': [],
                          'provenance/temporal/accrualPeriodicity': [],
                          'provenance/temporal/distributionReleaseDate': [],
                          'provenance/temporal/startDate': [],
                          'provenance/temporal/endDate': [],
                          'provenance/temporal/timeLag': [],
                          'accessibility/usage/dataUseLimitation': [],
                          'accessibility/usage/dataUseRequirements': [],
                          'accessibility/usage/resourceCreator': [],
                          'accessibility/usage/investigations': [],
                          'accessibility/usage/isReferencedBy': [],
                          'accessibility/access/accessRights': [],
                          'accessibility/access/accessService': [],
                          'accessibility/access/accessRequestCost': [],
                          'accessibility/access/deliveryLeadTime': [],
                          'accessibility/access/jurisdiction': [],
                          'accessibility/access/dataController': [],
                          'accessibility/access/dataProcessor': [],
                          'accessibility/formatAndStandards/vocabularyEncodingScheme': [],
                          'accessibility/formatAndStandards/conformsTo': [],
                          'accessibility/formatAndStandards/language': [],
                          'accessibility/formatAndStandards/format': [],
                          'enrichmentAndLinkage/qualifiedRelation': [],
                          'enrichmentAndLinkage/derivation': [],
                          'enrichmentAndLinkage/tools': [],
                          'structuralMetadata': [], })


def remove_none_from_dict(json_data):
    keys = copy.deepcopy(list(json_data.keys()))
    for js_key in keys:
        js_value = json_data.get(js_key, None)
        if isinstance(js_value, dict):
            remove_none_from_dict(js_value)
            if 0==len(list(js_value.keys())):
                json_data.pop(js_key, None)
        else:
            if not js_value:
                json_data.pop(js_key, None)


def read_v2_attributes(db_connection, db_schema, dm_id):
    attributes = base_v2_json()
    assessment = base_v2_reporting()

    sql_statement = f"SELECT DISTINCT element_id AS dm_id, id AS kv_id, name AS kv_key, extension_value AS kv_value " \
                    f"FROM {db_schema}.extension_value " \
                    f"WHERE element_id = {dm_id} AND ( name LIKE 'properties/%' OR name = 'structuralMetadata') ORDER BY name;"
    sql_result = dbu.sql_select_to_json(db_connection, sql_statement)

    technical_metadata = False
    attributes['identifier'] = f"https://hdruk.metadata.works/hdrukOnboarding/progressOverview?dataModelId={dm_id}"
    assessment['identifier'] = 'A'
    for s in sql_result:
        attr_key = s.get('kv_key', None)
        attr_value = s.get('kv_value', None)
        if 'properties/summary/title' == attr_key:
            if attr_value:
                attributes['summary']['title'] = attr_value
                assessment['summary/title'] = 'A'
            else:
                attributes['summary'].pop('title', None)
        elif 'properties/summary/abstract' == attr_key:
            if attr_value:
                attributes['summary']['abstract'] = attr_value
                assessment['summary/abstract'] = 'A'
            else:
                attributes['summary'].pop('abstract', None)
        elif 'properties/summary/contactPoint' == attr_key:
            if attr_value:
                attributes['summary']['contactPoint'] = attr_value
                assessment['summary/contactPoint'] = 'A'
            else:
                attributes['summary'].pop('contactPoint', None)
        elif 'properties/summary/keywords' == attr_key:
            if attr_value:
                attributes['summary']['keywords'] = attr_value
                assessment['summary/keywords'] = 'A'
            else:
                attributes['summary'].pop('keywords', None)
        elif 'properties/summary/doiName' == attr_key:
            if attr_value:
                attributes['summary']['doiName'] = attr_value
                assessment['summary/doiName'] = 'A'
            else:
                attributes['summary'].pop('doiName', None)
        elif 'properties/summary/publisher/name' == attr_key:
            if attr_value:
                attributes['summary']['publisher']['name'] = attr_value
                assessment['summary/publisher/name'] = 'A'
            else:
                attributes['summary']['publisher'].pop('name', None)
        elif 'properties/summary/publisher/contactPoint' == attr_key:
            if attr_value:
                attributes['summary']['publisher']['contactPoint'] = attr_value
                assessment['summary/publisher/contactPoint'] = 'A'
            else:
                attributes['summary']['publisher'].pop('contactPoint', None)
        elif 'properties/summary/publisher/memberOf' == attr_key:
            if attr_value:
                attributes['summary']['publisher']['memberOf'] = attr_value
                assessment['summary/publisher/memberOf'] = 'A'
            else:
                attributes['summary']['publisher'].pop('memberOf', None)
        elif 'properties/documentation/description' == attr_key:
            if attr_value:
                attributes['documentation']['description'] = attr_value
                assessment['documentation/description'] = 'A'
            else:
                attributes['documentation'].pop('description', None)
        elif 'properties/documentation/associatedMedia' == attr_key:
            if attr_value:
                attributes['documentation']['associatedMedia'] = attr_value
                assessment['documentation/associatedMedia'] = 'A'
            else:
                attributes['documentation'].pop('associatedMedia', None)
        elif 'properties/documentation/isPartOf' == attr_key:
            if attr_value:
                attributes['documentation']['isPartOf'] = attr_value
                assessment['documentation/isPartOf'] = 'A'
            else:
                attributes['documentation'].pop('isPartOf', None)
        elif 'properties/coverage/spatial' == attr_key:
            if attr_value:
                attributes['coverage']['spatial'] = attr_value
                assessment['coverage/spatial'] = 'A'
            else:
                attributes['coverage'].pop('spatial', None)
        elif 'properties/coverage/typicalAgeRange' == attr_key:
            if attr_value:
                attributes['coverage']['typicalAgeRange'] = attr_value
                assessment['coverage/typicalAgeRange'] = 'A'
            else:
                attributes['coverage'].pop('typicalAgeRange', None)
        elif 'properties/coverage/physicalSampleAvailability' == attr_key:
            if attr_value:
                attributes['coverage']['physicalSampleAvailability'] = attr_value
                assessment['coverage/physicalSampleAvailability'] = 'A'
            else:
                attributes['coverage'].pop('physicalSampleAvailability', None)
        elif 'properties/coverage/followup' == attr_key:
            if attr_value:
                attributes['coverage']['followup'] = attr_value
                assessment['coverage/followup'] = 'A'
            else:
                attributes['coverage'].pop('followup', None)
        elif 'properties/coverage/pathway' == attr_key:
            if attr_value:
                attributes['coverage']['pathway'] = attr_value
                assessment['coverage/pathway'] = 'A'
            else:
                attributes['coverage'].pop('pathway', None)
        elif 'properties/provenance/origin/purpose' == attr_key:
            if attr_value:
                attributes['provenance']['origin']['purpose'] = attr_value
                assessment['provenance/origin/purpose'] = 'A'
            else:
                attributes['provenance']['origin'].pop('purpose', None)
        elif 'properties/provenance/origin/source' == attr_key:
            if attr_value:
                attributes['provenance']['origin']['source'] = attr_value
                assessment['provenance/origin/source'] = 'A'
            else:
                attributes['provenance']['origin'].pop('source', None)
        elif 'properties/provenance/origin/collectionSituation' == attr_key:
            if attr_value:
                attributes['provenance']['origin']['collectionSituation'] = attr_value
                assessment['provenance/origin/collectionSituation'] = 'A'
            else:
                attributes['provenance']['origin'].pop('collectionSituation', None)
        elif 'properties/provenance/temporal/accrualPeriodicity' == attr_key:
            if attr_value:
                attributes['provenance']['temporal']['accrualPeriodicity'] = attr_value
                assessment['provenance/temporal/accrualPeriodicity'] = 'A'
            else:
                attributes['provenance']['temporal'].pop('accrualPeriodicity', None)
        elif 'properties/provenance/temporal/distributionReleaseDate' == attr_key:
            if attr_value:
                attributes['provenance']['temporal']['distributionReleaseDate'] = attr_value
                assessment['provenance/temporal/distributionReleaseDate'] = 'A'
            else:
                attributes['provenance']['temporal'].pop('distributionReleaseDate', None)
        elif 'properties/provenance/temporal/startDate' == attr_key:
            if attr_value:
                attributes['provenance']['temporal']['startDate'] = attr_value
                assessment['provenance/temporal/startDate'] = 'A'
            else:
                attributes['provenance']['temporal'].pop('startDate', None)
        elif 'properties/provenance/temporal/endDate' == attr_key:
            if attr_value:
                attributes['provenance']['temporal']['endDate'] = attr_value
                assessment['provenance/temporal/endDate'] = 'A'
            else:
                attributes['provenance']['temporal'].pop('endDate', None)
        elif 'properties/provenance/temporal/timeLag' == attr_key:
            if attr_value:
                attributes['provenance']['temporal']['timeLag'] = attr_value
                assessment['provenance/temporal/timeLag'] = 'A'
            else:
                attributes['provenance']['temporal'].pop('timeLag', None)
        elif 'properties/accessibility/usage/dataUseLimitation' == attr_key:
            if attr_value:
                attributes['accessibility']['usage']['dataUseLimitation'] = attr_value
                assessment['accessibility/usage/dataUseLimitation'] = 'A'
            else:
                attributes['accessibility']['usage'].pop('dataUseLimitation', None)
        elif 'properties/accessibility/usage/dataUseRequirements' == attr_key:
            if attr_value:
                attributes['accessibility']['usage']['dataUseRequirements'] = attr_value
                assessment['accessibility/usage/dataUseRequirements'] = 'A'
            else:
                attributes['accessibility']['usage'].pop('dataUseRequirements', None)
        elif 'properties/accessibility/usage/resourceCreator' == attr_key:
            if attr_value:
                attributes['accessibility']['usage']['resourceCreator'] = attr_value
                assessment['accessibility/usage/resourceCreator'] = 'A'
            else:
                attributes['accessibility']['usage'].pop('resourceCreator', None)
        elif 'properties/accessibility/usage/investigations' == attr_key:
            if attr_value:
                attributes['accessibility']['usage']['investigations'] = attr_value
                assessment['accessibility/usage/investigations'] = 'A'
            else:
                attributes['accessibility']['usage'].pop('investigations', None)
        elif 'properties/accessibility/usage/isReferencedBy' == attr_key:
            if attr_value:
                attributes['accessibility']['usage']['isReferencedBy'] = attr_value
                assessment['accessibility/usage/isReferencedBy'] = 'A'
            else:
                attributes['accessibility']['usage'].pop('isReferencedBy', None)
        elif 'properties/accessibility/access/accessRights' == attr_key:
            if attr_value:
                attributes['accessibility']['access']['accessRights'] = attr_value
                assessment['accessibility/access/accessRights'] = 'A'
            else:
                attributes['accessibility']['access'].pop('accessRights', None)
        elif 'properties/accessibility/access/accessService' == attr_key:
            if attr_value:
                attributes['accessibility']['access']['accessService'] = attr_value
                assessment['accessibility/access/accessService'] = 'A'
            else:
                attributes['accessibility']['access'].pop('accessService', None)
        elif 'properties/accessibility/access/accessRequestCost' == attr_key:
            if attr_value:
                attributes['accessibility']['access']['accessRequestCost'] = attr_value
                assessment['accessibility/access/accessRequestCost'] = 'A'
            else:
                attributes['accessibility']['access'].pop('accessRequestCost', None)
        elif 'properties/accessibility/access/deliveryLeadTime' == attr_key:
            if attr_value:
                attributes['accessibility']['access']['deliveryLeadTime'] = attr_value
                assessment['accessibility/access/deliveryLeadTime'] = 'A'
            else:
                attributes['accessibility']['access'].pop('deliveryLeadTime', None)
        elif 'properties/accessibility/access/jurisdiction' == attr_key:
            if attr_value:
                attributes['accessibility']['access']['jurisdiction'] = attr_value
                assessment['accessibility/access/jurisdiction'] = 'A'
            else:
                attributes['accessibility']['access'].pop('jurisdiction', None)
        elif 'properties/accessibility/access/dataController' == attr_key:
            if attr_value:
                attributes['accessibility']['access']['dataController'] = attr_value
                assessment['accessibility/access/dataController'] = 'A'
            else:
                attributes['accessibility']['access'].pop('dataController', None)
        elif 'properties/accessibility/access/dataProcessor' == attr_key:
            if attr_value:
                attributes['accessibility']['access']['dataProcessor'] = attr_value
                assessment['accessibility/access/dataProcessor'] = 'A'
            else:
                attributes['accessibility']['access'].pop('dataProcessor', None)
        elif 'properties/accessibility/formatAndStandards/vocabularyEncodingScheme' == attr_key:
            if attr_value:
                attributes['accessibility']['formatAndStandards']['vocabularyEncodingScheme'] = attr_value
                assessment['accessibility/formatAndStandards/vocabularyEncodingScheme'] = 'A'
            else:
                attributes['accessibility']['formatAndStandards'].pop('vocabularyEncodingScheme', None)
        elif 'properties/accessibility/formatAndStandards/conformsTo' == attr_key:
            if attr_value:
                attributes['accessibility']['formatAndStandards']['conformsTo'] = attr_value
                assessment['accessibility/formatAndStandards/conformsTo'] = 'A'
            else:
                attributes['accessibility']['formatAndStandards'].pop('conformsTo', None)
        elif 'properties/accessibility/formatAndStandards/language' == attr_key:
            if attr_value:
                attributes['accessibility']['formatAndStandards']['language'] = attr_value
                assessment['accessibility/formatAndStandards/language'] = 'A'
            else:
                attributes['accessibility']['formatAndStandards'].pop('language', None)
        elif 'properties/accessibility/formatAndStandards/format' == attr_key:
            if attr_value:
                attributes['accessibility']['formatAndStandards']['format'] = attr_value
                assessment['accessibility/formatAndStandards/format'] = 'A'
            else:
                attributes['accessibility']['formatAndStandards'].pop('format', None)
        elif 'properties/enrichmentAndLinkage/qualifiedRelation' == attr_key:
            if attr_value:
                attributes['enrichmentAndLinkage']['qualifiedRelation'] = attr_value
                assessment['enrichmentAndLinkage/qualifiedRelation'] = 'A'
            else:
                attributes['enrichmentAndLinkage'].pop('qualifiedRelation', None)
        elif 'properties/enrichmentAndLinkage/derivation' == attr_key:
            if attr_value:
                attributes['enrichmentAndLinkage']['derivation'] = attr_value
                assessment['enrichmentAndLinkage/derivation'] = 'A'
            else:
                attributes['enrichmentAndLinkage'].pop('derivation', None)
        elif 'properties/enrichmentAndLinkage/tools' == attr_key:
            if attr_value:
                attributes['enrichmentAndLinkage']['tools'] = attr_value
                assessment['enrichmentAndLinkage/tools'] = 'A'
            else:
                attributes['enrichmentAndLinkage'].pop('tools', None)
        elif 'structuralMetadata' == attr_key:
            technical_metadata = True
            assessment['technicalMetadata'] = 'A'

    attribute_count = 0
    for a_key, a_value in assessment.items():
        if 'provenance/temporal/endDate' == a_key:
            continue
        if a_value != 'U':
            attribute_count += 1

    return {'dm_id': dm_id, 'dm_attributes': attributes, 'dm_assessment': assessment, 'attribute_count': attribute_count, 'tmd': technical_metadata}


def validate_dm(validator, dm):
    attributes = copy.deepcopy(dm['dm_attributes'])
    remove_none_from_dict(attributes)
    errors = sorted(validator.iter_errors(attributes), key=lambda e: e.path)
    dm['error_count'] = len(errors)
    dm['errors'] = {}
    for e in errors:
        assessment_key = '/'.join(e.absolute_path)
        if not assessment_key in dm['dm_assessment']:
            continue
        dm['dm_assessment'][assessment_key] = 'I'
        dm['errors'][assessment_key] = {'message': e.message, 'context': e.context}
    if dm['error_count'] > dm['attribute_count']:
        dm['assessment_mark'] = 0
    else:
        dm['assessment_mark'] = int(( 1000 * (dm['attribute_count'] - dm['error_count']) ) / 44)


def date_2_tld(curr_tld=None, test_flag = True, today=True):
    '''
    Date to (T)hree (L)etter (D)ate for versioning
    :param curr_tld:
    :param test_flag:
    :param today:
    :return:
    '''
