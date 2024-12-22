#!/usr/bin/python3

import os
import yaml
import json
from datetime import datetime

def parse_chart_yaml(chart_path):
    with open(chart_path, 'r') as file:
        chart_data = yaml.safe_load(file)
    
    json_data = {
        "app_readme": f"<h1>{chart_data.get('name', '')}</h1><p>{chart_data.get('description', '')}</p>",
        "categories": [chart_data.get("annotations", {}).get("truecharts.org/category", "")],
        "description": chart_data.get("description", ""),
        "healthy": True,
        "healthy_error": None,
        "home": chart_data.get("home", ""),
        "location": os.path.abspath(os.path.dirname(chart_path)),  # Абсолютный путь
        "latest_version": chart_data.get("version", ""),
        "latest_app_version": chart_data.get("appVersion", ""),
        "latest_human_version": f"{chart_data.get('appVersion', '')}_{chart_data.get('version', '')}",
        "last_update": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "name": chart_data.get("name", ""),
        "recommended": False,
        "title": chart_data.get("name", "").capitalize(),
        "maintainers": [
            {
                "name": maintainer.get("name", ""),
                "url": maintainer.get("url", ""),
                "email": maintainer.get("email", "")
            } for maintainer in chart_data.get("maintainers", [])
        ],
        "tags": chart_data.get("keywords", []),
        "screenshots": [chart_data.get("icon", "")],
        "sources": chart_data.get("sources", []),
        "icon_url": chart_data.get("icon", "")
    }
    return json_data

def generate_json(charts_dir, output_file):
    charts_data = {}
    for root, dirs, files in os.walk(charts_dir):
        for file in files:
            if file == "Chart.yaml":
                chart_path = os.path.join(root, file)
                app_name = os.path.basename(os.path.dirname(chart_path))
                charts_data[app_name] = parse_chart_yaml(chart_path)

    catalog_data = {
        "charts": charts_data
    }

    with open(output_file, 'w') as json_file:
        json.dump(catalog_data, json_file, indent=4)

# Использование
charts_directory = "charts"
output_json_file = "catalog.json"
generate_json(charts_directory, output_json_file)
print(f"JSON файл создан: {output_json_file}")
