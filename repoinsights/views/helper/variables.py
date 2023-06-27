from typing import Dict, List

COMMIT = "commit"
LANGS = "langs"
USER = "user"

Rating = Dict[str, Dict[str, int | float]]
MetricScore = Dict[str, int | str | Rating]
Metric_scores: List[MetricScore]

Metric_scores = [
        {
            "id": 9,
            "rating": {
                # Una semana
                "A": {
                    "min": 0,
                    "max": 7
                },
                # 2 - 4 semanas
                "B": {
                    "min": 8,
                    "max": 30
                },
                # 1 - 2 meses
                "C": {
                    "min": 31,
                    "max": 60
                },
                # más de 3 meses
                "F": {
                    "min": 61,
                    "max": 1000000
                }
            }
        },
        {
            "id": 3,
            "rating": {
                "A":{
                    "min": 0,
                    "max": 0.5
                },
                "F": {
                    "min": 0.51,
                    "max": 1
                }
            }
        }
    ]
