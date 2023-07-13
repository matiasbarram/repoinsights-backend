from django.db import connections
from typing import Dict

from .variables import (
    Metric_scores as Metric_scores,
    Rating as Rating,
    MetricScore as MetricScore,
    MeasurementTypes as MeasurementTypes,
)


class ProjectMetricScore:
    @staticmethod
    def calc_metric_value(metric_name, project_id):
        query = f"""
            SELECT
                pm.value AS value,
                m.name AS metric_name,
                m.measurement_type
            FROM "ghtorrent_restore_2015"."project_metrics" pm
            JOIN extractions e ON pm.extraction_id = e.id
            JOIN (
                SELECT MAX(date) as max_date, project_id
                FROM extractions e
                WHERE e.project_id = {project_id}
                GROUP BY project_id
            ) AS max_extractions ON e.date = max_extractions.max_date AND e.project_id = max_extractions.project_id
            JOIN "ghtorrent_restore_2015"."projects" p ON e.project_id = p.id
            JOIN metrics m ON pm.metric_id = m.id
            WHERE m.name = '{metric_name}'
        """
        cursor = connections["repoinsights"].cursor()
        cursor.execute(query)
        response = cursor.fetchone()
        value = float(response[0]) if response else None
        name: str | None = str(response[1]) if response else None
        measurement: str | None = str(response[2]) if response else None
        return value, name, measurement

    @staticmethod
    def calc_rating(metric_data, metric_value: float):
        if metric_value is None:
            return None
        if isinstance(metric_data, dict):
            for metric in metric_data.items():
                rate = metric[0]
                min_value = float(metric[1]["min"])
                max_value = float(metric[1]["max"])
                if metric_value >= min_value and metric_value <= max_value:
                    return rate
            return None

    @staticmethod
    def calc_metric_score(projects, empty_values=False) -> list:
        projects = list(projects)
        for project in projects:
            project["rating"] = []
            project_id = project["id"]
            for metric_score in Metric_scores:
                score_metric_name = metric_score["name"]
                score_metric_rating = metric_score["rating"]
                (
                    metric_value,
                    metric_name,
                    metric_measurement,
                ) = ProjectMetricScore.calc_metric_value(score_metric_name, project_id)
                if metric_value is None or metric_name is None or metric_measurement is None:
                    if empty_values:
                        data = {
                            "id": score_metric_name,
                            "name": score_metric_name,
                            "value": None,
                            "rating": None,
                            "show_value": False,
                            "measurement": None
                        }
                        project["rating"].append(data)
                        continue
                    else:
                        continue

                rating = ProjectMetricScore.calc_rating(score_metric_rating, metric_value)
                show_value = metric_score.get("show_value", True)
                metric_title = (
                    metric_score["title"] if metric_score.get("title") else score_metric_name
                )
                data = {
                    "id": score_metric_name,
                    "name": metric_title,
                    "value": metric_value,
                    "rating": rating,
                    "show_value": show_value,
                    "measurement": MeasurementTypes[metric_measurement.lower()]
                    if metric_measurement
                    else None,
                }
                project["rating"].append(data)
            if all([metric["value"] is None for metric in project["rating"]]):
                project["empty"] = True
            else:
                project["empty"] = False

        return projects

    @staticmethod
    def get_metrics():
        return [
            {
                "id": metric["name"], 
                "name": metric["title"],
                "invert": metric["weight"]["invert"] # type: ignore
            } for metric in Metric_scores
        ]
