from typing import Dict, List

COMMIT = "commit"
LANGS = "langs"
USER = "user"

MeasurementTypes = {
    "count": None,
    "hours": "h",
    "days": "d",
    "weeks": "w",
    "boolean": None,
    "percentage": "%",

}

Rating = Dict[str, Dict[str, int | float]]
MetricScore = Dict[str, int | str | Rating]
Metric_scores: List[MetricScore]
Metric_scores = [
        {
            "id": 9, # issue_closed_per_day
            "title": "Issues cerrados por día",
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
            "title": "Commits en PR",
            "rating": {
                "A": {
                    "max": 250,
                    "min": 0
                }
            }
        }
    ]
