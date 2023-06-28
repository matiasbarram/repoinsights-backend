from django.db import connections
from typing import Dict

from .variables import Metric_scores as Metric_scores, Rating as Rating, MetricScore as MetricScore


class ProjectMetricScore:

    @staticmethod
    def calc_metric_value(metric_id, project_id):
        query = f"""
            SELECT
                pm.value AS value,
                m.name AS metric_name
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
            WHERE pm.metric_id = {metric_id}
        """
        cursor = connections['repoinsights'].cursor()
        cursor.execute(query)
        response = cursor.fetchone()
        metric_value = float(response[0]) if response else None
        metric_name: str | None = str(response[1]) if response else None
        return metric_value, metric_name
                

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
    def calc_metric_score(projects) -> list:
        projects = list(projects)
        for project in projects:
            project["rating"] = []
            project_id = project["id"]
            for metric_score in Metric_scores:
                metric_id = metric_score["id"]
                metric_rating = metric_score["rating"]
                metric_value, metric_name = ProjectMetricScore.calc_metric_value(metric_id, project_id)
                if metric_value is None:
                    continue
                if metric_name is None:
                    continue
                rating = ProjectMetricScore.calc_rating(metric_rating, metric_value) 
                data = {
                    "id": metric_id,
                    "name": metric_name,
                    "value": metric_value,
                    "rating": rating,
                }
                project["rating"].append(data)
        return projects