import io
from collections import defaultdict, namedtuple
from enum import Enum
from functools import lru_cache
from itertools import groupby
from pathlib import Path
from typing import Type

import pandas as pd
from pydantic import Field, BaseModel
from pymultirole_plugins.v1.formatter import FormatterBase, FormatterParameters
from pymultirole_plugins.v1.schema import Document, Annotation, Category
from starlette.responses import Response


class OutputFormat(str, Enum):
    xlsx = 'xlsx'


class AFPQualityParameters(FormatterParameters):
    format: OutputFormat = Field(OutputFormat.xlsx, description="Output format")


class AFPQualityFormatter(FormatterBase):
    """AFPQuality formatter.
    """

    def format(self, document: Document, parameters: FormatterParameters) \
            -> Response:
        """Parse the input document and return a formatted response.

        :param document: An annotated document.
        :param options: options of the parser.
        :returns: Response.
        """
        parameters: AFPQualityParameters = parameters
        try:
            dfs = {}

            # categories
            cats_true, cats_pred = parse_categories(document)
            cats_all = set(cats_true)
            cats_all.update(cats_pred)
            serie = []
            for y in cats_all:
                code, name = y.split(':', maxsplit=1)
                serie.append({'Code': code,
                              'Name': name,
                              'True': 1 if y in cats_true else 0,
                              'Pred': 1 if y in cats_pred else 0,
                              })
            dfs['medtop'] = pd.DataFrame.from_records(serie)

            # annotations
            ann_groups = group_annotations(document, by_label)
            for subject in ['afpperson', 'afplocation', 'afporganization']:
                serie = []
                y_true = document.metadata.get(subject, [])
                y_all = set(y_true)
                y_pred = ann_groups.get(subject, [])
                y_all.update(y_pred)
                for y in y_all:
                    code, name = y.split(':', maxsplit=1)
                    serie.append({'Code': code,
                                  'Name': name,
                                  'True': 1 if y in y_true else 0,
                                  'Pred': 1 if y in y_pred else 0,
                                  })
                dfs[subject] = pd.DataFrame.from_records(serie)
            resp: Response = None
            filename = f"file.{parameters.format.value}"
            if document.properties and "fileName" in document.properties:
                filepath = Path(document.properties['fileName'])
                filename = f"{filepath.stem}.{parameters.format.value}"
            if parameters.format == OutputFormat.xlsx:
                bio = io.BytesIO()
                writer = pd.ExcelWriter(bio, engine='openpyxl')
                for subject, df in dfs.items():
                    df.to_excel(writer, index=False, sheet_name=subject, columns=['Code', 'Name', 'True', 'Pred'])
                writer.save()
                writer.close()
                resp = Response(content=bio.getvalue(),
                                media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
                resp.headers["Content-Disposition"] = f"attachment; filename={filename}"
            return resp
        except BaseException as err:
            raise err

    @classmethod
    def get_model(cls) -> Type[BaseModel]:
        return AFPQualityParameters


def parse_categories(doc: Document):
    topics = get_mediatopics()
    root_cats = ['11000000', '04000000', '07000000', '11000000']
    medtops_true = [medtop.split(':', maxsplit=1)[0] for medtop in doc.metadata.get('medtop', [])]
    cats_true = set()
    for t in medtops_true:
        levels = topics[t].levels
        if len(levels) == 1 or levels[0] in root_cats:
            cats_true.add(f"{t}:{topics[t].label}")
    medtops_pred = set()
    if doc.categories:
        for cat in doc.categories:
            medtops_pred.update(cat.labelName.split('_'))
    cats_pred = [f"{t}:{topics[t].label}" for t in medtops_pred]
    return cats_true, cats_pred


def group_annotations(doc: Document, keyfunc):
    groups = defaultdict(list)
    if doc.annotations:
        for k, g in groupby(sorted(doc.annotations, key=keyfunc), keyfunc):
            afpterms = set()
            for a in g:
                if a.terms:
                    afpterms.update([f"{t.identifier[len(k) + 1:]}:{t.preferredForm}" for t in a.terms if
                                     t.identifier.startswith(k)])
            groups[k] = list(afpterms)
    return groups


def by_label(a: Annotation):
    return a.labelName


def by_len_and_alpha_str(k: str):
    return len(k), k

def by_len_and_alpha_cat(c: Category):
    return len(c.labelName), c.labelName

Mediatopic = namedtuple('Mediatopic', ['label', 'levels'])


@lru_cache(maxsize=None)
def get_mediatopics():
    iptc = Path(__file__).parent / "IPTC-MediaTopic-NewsCodes.xlsx"
    topics = {}
    iptc_codes = pd.read_excel(iptc, header=1).fillna(value="")
    levels = [None] * 6
    for index, row in iptc_codes.iterrows():
        topic_url = row['NewsCode-QCode (flat)']
        topic_code = topic_url[len('medtop:'):]

        for lev in range(0, 6):
            level = f"Level{lev + 1}/NewsCode"
            level_url = row[level]
            if level_url:
                level_code = level_url[len('medtop:'):]
                levels[lev] = level_code
                break
        for k in range(lev + 1, 6):
            levels[k] = None
        topics[topic_code] = Mediatopic(label=row['Name (en-GB)'],
                                        levels=levels[0:lev + 1].copy())
    return topics
