#!/usr/bin/env python

import json

from ClassStructure.CourseClassStructure import AClassDecoder, AClassEncoder


def convert_to_json_str(class_obj):
    json_str = json.dumps(class_obj, indent=4, default=AClassEncoder.default)

    return json_str


def extract_from_json_str(json_str):
    class_obj = json.loads(json_str, cls=AClassDecoder)

    return class_obj
