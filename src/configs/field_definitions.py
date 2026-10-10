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
        },


        # ============================================================
        # EMBEDDING DATA
        # ============================================================

        "CREATE_EMBEDDING": {

            "PROJECT_ID": {
                "field": "projectId",
                "required": True,
                "validation": validation_rules["mongoId"],
                "description": "MongoDB project ID"
            },

            "ENTITY_ID": {
                "field": "entityId",
                "required": True,
                "validation": validation_rules["mongoId"],
                "description": "MongoDB entity ID"
            },

            "ENTITY_TYPE": {
                "field": "entityType",
                "required": True,
                "validation": validation_rules["entityType"],
                "description": "Entity type"
            },

            "TITLE": {
                "field": "title",
                "required": False,
                "validation": validation_rules["title"],
                "description": "Entity title"
            },

            "DESCRIPTION": {
                "field": "description",
                "required": False,
                "validation": validation_rules["description"],
                "description": "Entity description"
            }

        },

        # ============================================================
        # UPDATE EMBEDDING
        # ============================================================

        "UPDATE_EMBEDDING": {

            "ENTITY_ID": {
                "field": "entityId",
                "required": True,
                "validation": validation_rules["mongoId"],
                "description": "MongoDB entity ID"
            },

            "TITLE": {
                "field": "title",
                "required": False,
                "validation": validation_rules["title"],
                "description": "Updated entity title"
            },

            "DESCRIPTION": {
                "field": "description",
                "required": False,
                "validation": validation_rules["description"],
                "description": "Updated entity description"
            }

        },

        # ============================================================
        # FORCE UPDATE EMBEDDING
        # ============================================================

        "FORCE_UPDATE_EMBEDDING": {

            "ENTITY_ID": {
                "field": "entityId",
                "required": True,
                "validation": validation_rules["mongoId"],
                "description": "MongoDB entity ID"
            },

            "TITLE": {
                "field": "title",
                "required": False,
                "validation": validation_rules["title"],
                "description": "Updated entity title"
            },

            "DESCRIPTION": {
                "field": "description",
                "required": False,
                "validation": validation_rules["description"],
                "description": "Updated entity description"
            }

        },

        # ============================================================
        # GET EMBEDDING
        # ============================================================

        "GET_EMBEDDING": {

            "ENTITY_ID": {
                "field": "entityId",
                "required": True,
                "validation": validation_rules["mongoId"],
                "description": "MongoDB entity ID"
            }

        },

        # ============================================================
        # LIST EMBEDDINGS
        # ============================================================

        "LIST_EMBEDDINGS": {

            "PROJECT_ID": {
                "field": "projectId",
                "required": False,
                "validation": validation_rules["mongoId"],
                "description": "MongoDB project ID"
            },

            "ENTITY_TYPE": {
                "field": "entityType",
                "required": False,
                "validation": validation_rules["entityType"],
                "description": "Entity type filter"
            },

            "PAGE": {
                "field": "page",
                "required": False,
                "description": "Page number"
            },

            "LIMIT": {
                "field": "limit",
                "required": False,
                "description": "Number of embeddings per page"
            }

        },

        # ============================================================
        # DELETE EMBEDDING
        # ============================================================

        "DELETE_EMBEDDING": {

            "ENTITY_ID": {
                "field": "entityId",
                "required": True,
                "validation": validation_rules["mongoId"],
                "description": "MongoDB entity ID"
            }

        }

    }
}