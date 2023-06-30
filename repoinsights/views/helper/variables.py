from typing import Dict, List

COMMIT = "commit"
LANGS = "langs"
USER = "user"
SORT = "sort"

MeasurementTypes = {
    "count": None,
    "hours": "h",
    "days": "d",
    "weeks": "w",
    "boolean": None,
    "percentage": "%",

}

Rating = Dict[str, Dict[str, int | float | bool ]]
Weight = Dict[str, int | float | bool]
MetricScore = Dict[str, int | str | float | Rating | Weight ]
Metric_scores: List[MetricScore]

N = 5
Metric_scores = [
        {
            "id": 9, # issue_closed_per_day
            "title": "Issues cerrados por día",
            "weight": {
                "value": 0.2,
                "invert": False
            },
            "rating": {
                "F": {
                    "max": 7,
                    "min": 0
                },
                "C": {
                    "max": 30,
                    "min": 7
                },
                "B": {
                    "max": 60,
                    "min": 30
                },
                "A": {
                    "max": 1000000,
                    "min": 60
                }
            }
        },
        {
            "id": 3, # hero project
            "weight": {
                "value": 0.2,
                "invert": True
            },
            "title": "Hero project",
            "show_value": False,
            "rating": {
                "A":{
                    "max": 0.50,
                    "min": 0
                },
                "F": {
                    "max": 1,
                    "min": 0.50
                }
            }
        },
        {
            "id": 202, # time_to_first_response_issues_avg
            "weight": {
                "value": 0.2,
                "invert": True
            },
            "title": "Tiempo primera respuesta issue",
            "rating": {
                "A": {
                    "max": 20,
                    "min": 0
                },
                "F":{
                    "max": 1000000,
                    "min": 20
                }
            }
        },
        {
            "id": 6, # active_days_coverage
            "weight": {
                "value": 0.2,
                "invert": False
            },
            "title": "Días activos",
            "rating": {
                "A": {
                    "max": 1,
                    "min": 0.80
                },
                "B": {
                    "max": 0.80,
                    "min": 0.60
                },
                "C": {
                    "max": 0.60,
                    "min": 0.40
                },
                "D": {
                    "max": 0.40,
                    "min": 0.20
                },
                "E": {
                    "max": 0.20,
                    "min": 0.1
                },
                "F": {
                    "max": 0.1,
                    "min": 0
                }
            }
        },
        {
            "id": 29, # commits_in_pr_avg
            "weight": {
                "value": 0.2,
                "invert": False
            },
            "title": "Commits en PR",
            "rating": {
                "A": {
                    "max": 250,
                    "min": 0
                }
            }
        }
    ]
