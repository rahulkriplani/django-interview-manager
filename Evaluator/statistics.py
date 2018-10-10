from .models import Round
import json


def get_all_round_bar_graph():
    pass

def filter_candi_past_round(round_number, after_date):
    pass

def get_points_rating_sheet_for_round(rating_aspects):
    point_list = list()
    aspect_name = list()

    for aspect in rating_aspects:
        point_list.append(aspect.points)

    return json.dumps(point_list)
