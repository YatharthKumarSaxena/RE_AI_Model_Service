from src.configs.field_lengths import FIELD_LENGTHS
from src.utils.enum_helpers import (
    ProjectTypesHelper
)

validation_rules = {

    # ─── Project Fields ───────────────────────────────────────────────
    "projectName": {
        "length": {
            "min": FIELD_LENGTHS["projectNameLength"]["min"],
            "max": FIELD_LENGTHS["projectNameLength"]["max"]
        }
    },

    "projectType": {
        "enum": ProjectTypesHelper
    },


    "projectDescription": {
        "length": {
            "min": FIELD_LENGTHS["descriptionLength"]["min"],
            "max": FIELD_LENGTHS["descriptionLength"]["max"]
        }
    },

    "problemStatement": {
        "length": {
            "min": FIELD_LENGTHS["problemStatementLength"]["min"],
            "max": FIELD_LENGTHS["problemStatementLength"]["max"]
        }
    },

    "projectGoal": {
        "length": {
            "min": FIELD_LENGTHS["projectGoalLength"]["min"],
            "max": FIELD_LENGTHS["projectGoalLength"]["max"]
        }
    },

    "title": {
        "length": {
            "min": FIELD_LENGTHS["titleLength"]["min"],
            "max": FIELD_LENGTHS["titleLength"]["max"]
        }
    },

    "description": {
        "length": {
            "min": FIELD_LENGTHS["descriptionLength"]["min"],
            "max": FIELD_LENGTHS["descriptionLength"]["max"]
        }
    },

    "productVision": {
        "length": {
            "min": FIELD_LENGTHS["productVisionLength"]["min"],
            "max": FIELD_LENGTHS["productVisionLength"]["max"]
        }
    },

    "acceptanceCriteria": {
        "length": {
            "min": FIELD_LENGTHS["acceptanceCriteriaLength"]["min"],
            "max": FIELD_LENGTHS["acceptanceCriteriaLength"]["max"]
        }
    }
}