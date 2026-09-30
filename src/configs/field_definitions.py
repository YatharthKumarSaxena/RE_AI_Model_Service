from src.configs.validation import validation_rules


FieldDefinitions = {

    "CONVERT_CONTENT_TO_ENGLISH": {

        "RAW_TITLE": {
            "field": "rawTitle",
            "required": True,
            "validation": validation_rules["title"],
            "description": "Raw content title"
        },

        "RAW_DESCRIPTION": {
            "field": "rawDescription",
            "required": False,
            "validation": validation_rules["description"],
            "description": "Raw content description"
        }

    },

    # ============================================================
    # ENTITY TYPE DATA
    # ============================================================

    "CLASSIFY_ENTITY_TYPE": {
        "PROJECT_TITLE": {
            "field": "projectTitle",
            "required": True,
            "validation": validation_rules["projectName"],
            "description": "Project title"
        },

        "PROJECT_DESCRIPTION": {
            "field": "projectDescription",
            "required": True,
            "validation": validation_rules["projectDescription"],
            "description": "Project description"
        },

        "PROBLEM_STATEMENT": {
            "field": "problemStatement",
            "required": True,
            "validation": validation_rules["problemStatement"],
            "description": "Project problem statement"
        },

        "PROJECT_GOAL": {
            "field": "projectGoal",
            "required": True,
            "validation": validation_rules["projectGoal"],
            "description": "Project goal"
        },

        "PROJECT_TYPE": {
            "field": "projectType",
            "required": True,
            "validation": validation_rules["projectType"],
            "description": "Project type"
        },

        "PRODUCT_VISION": {
            "field": "productVision",
            "required": False,
            "validation": validation_rules["productVision"],
            "description": "Product vision"
        },

        "ENTITY_TITLE": {
            "field": "rawTitle",
            "required": True,
            "validation": validation_rules["title"],
            "description": "Entity title"
        },

        "ENTITY_DESCRIPTION": {
            "field": "rawDescription",
            "required": False,
            "validation": validation_rules["description"],
            "description": "Entity description"
        }
    },

    "IMPORT_ENTITY_TYPE": {

        "ROW_ID": {
            "field": "rowId",
            "required": True,
            "description": "Unique row identifier"
        },

        "PROJECT_TITLE": {
            "field": "projectTitle",
            "required": True,
            "validation": validation_rules["projectName"],
            "description": "Project title"
        },

        "PROJECT_DESCRIPTION": {
            "field": "projectDescription",
            "required": True,
            "validation": validation_rules["projectDescription"],
            "description": "Project description"
        },

        "PROBLEM_STATEMENT": {
            "field": "problemStatement",
            "required": True,
            "validation": validation_rules["problemStatement"],
            "description": "Project problem statement"
        },

        "PROJECT_GOAL": {
            "field": "projectGoal",
            "required": True,
            "validation": validation_rules["projectGoal"],
            "description": "Project goal"
        },

        "PROJECT_TYPE": {
            "field": "projectType",
            "required": True,
            "validation": validation_rules["projectType"],
            "description": "Project type"
        },

        "PRODUCT_VISION": {
            "field": "productVision",
            "required": False,
            "validation": validation_rules["productVision"],
            "description": "Product vision"
        },

        "ENTITY_TITLE": {
            "field": "entityTitle",
            "required": True,
            "validation": validation_rules["title"],
            "description": "Entity title"
        },

        "ENTITY_DESCRIPTION": {
            "field": "entityDescription",
            "required": False,
            "validation": validation_rules["description"],
            "description": "Entity description"
        }

    }
}