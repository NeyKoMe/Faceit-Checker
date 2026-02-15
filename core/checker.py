from services.faceit_service import get_faceit_data


def check_players(inputs: list):
    results = []

    for player_input in inputs:
        data = get_faceit_data(player_input)

        if "error" not in data:
            results.append(data)

    return results