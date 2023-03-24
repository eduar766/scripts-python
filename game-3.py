def get_team_data():
    """
    Solicita los datos del equipo al usuario y devuelve un diccionario con los datos.
    """
    team_name = input("Ingrese el nombre del equipo: ")
    matches_played = int(input("Ingrese la cantidad de partidos jugados: "))
    goals_scored = int(input("Ingrese la cantidad de goles anotados: "))
    goals_received = int(input("Ingrese la cantidad de goles recibidos: "))
    recent_form_str = input("Forma reciente (últimos 5 partidos, 1 para ganar, 0.5 para empate, 0 para perder, separados por comas): ")
    recent_form = [float(x) for x in recent_form_str.replace('[', '').replace(']', '').split(',')]

    return {
        "team_name": team_name,
        "matches_played": matches_played,
        "goals_scored": goals_scored,
        "goals_received": goals_received,
        "recent_form": recent_form,
    }

def calculate_win_probability_and_draw(team_data1, team_data2):
    """
    Calcula la probabilidad de ganar y empatar para cada equipo en función de la diferencia promedio de goles y la forma reciente.
    Devuelve un diccionario con las probabilidades de ganar y empatar para cada equipo.
    """
    avg_goal_difference1 = (team_data1["goals_scored"] - team_data1["goals_received"]) / team_data1["matches_played"]
    avg_goal_difference2 = (team_data2["goals_scored"] - team_data2["goals_received"]) / team_data2["matches_played"]

    recent_form_weight = 0.3
    goal_difference_weight = 1 - recent_form_weight

    win_probability1 = goal_difference_weight * abs(avg_goal_difference1) + recent_form_weight * sum([1 if x == 1 else 0 for x in team_data1["recent_form"]])
    win_probability2 = goal_difference_weight * abs(avg_goal_difference2) + recent_form_weight * sum([1 if x == 1 else 0 for x in team_data2["recent_form"]])

    goal_difference_similarity = 1 - abs(avg_goal_difference1 - avg_goal_difference2) / max(abs(avg_goal_difference1), abs(avg_goal_difference2))
    recent_form_similarity = 1 - abs(sum(team_data1["recent_form"]) - sum(team_data2["recent_form"])) / max(sum(team_data1["recent_form"]), sum(team_data2["recent_form"]))

    draw_probability = goal_difference_weight * goal_difference_similarity + recent_form_weight * recent_form_similarity

    total_probability = win_probability1 + win_probability2 + draw_probability

    win_probability1 /= total_probability
    win_probability2 /= total_probability
    draw_probability /= total_probability

    return {
        team_data1["team_name"]: win_probability1,
        team_data2["team_name"]: win_probability2,
        "draw": draw_probability
    }
     
def estimate_goals(team_data1, team_data2):
    # Calcular el promedio de goles anotados y recibidos por cada equipo
    avg_goals_scored1 = team_data1["goals_scored"] / team_data1["matches_played"]
    avg_goals_received1 = team_data1["goals_received"] / team_data1["matches_played"]
    avg_goals_scored2 = team_data2["goals_scored"] / team_data2["matches_played"]
    avg_goals_received2 = team_data2["goals_received"] / team_data2["matches_played"]

    # Calcular el peso de la forma reciente (ganar = 1, perder = 0)
    recent_form_weight1 = sum(team_data1["recent_form"]) / len(team_data1["recent_form"])
    recent_form_weight2 = sum(team_data2["recent_form"]) / len(team_data2["recent_form"])

    # Ajustar el promedio de goles según la forma reciente de cada equipo
    estimated_goals1 = avg_goals_scored1 * recent_form_weight1 + avg_goals_received2 * (1 - recent_form_weight2)
    estimated_goals2 = avg_goals_scored2 * recent_form_weight2 + avg_goals_received1 * (1 - recent_form_weight1)

    return {
        team_data1["team_name"]: estimated_goals1,
        team_data2["team_name"]: estimated_goals2,
    }
    
def main():
    print("Ingrese los datos del primer equipo:")
    team_data1 = get_team_data()

    print("\nIngrese los datos del segundo equipo:")
    team_data2 = get_team_data()

    win_probabilities = calculate_win_probability_and_draw(team_data1, team_data2)

    print(f"\nProbabilidad de ganar para {team_data1['team_name']}: {win_probabilities[team_data1['team_name']]:.2%}")
    print(f"Probabilidad de ganar para {team_data2['team_name']}: {win_probabilities[team_data2['team_name']]:.2%}")
    print(f"Probabilidad de empate: {win_probabilities['draw']:.2%}")

    estimated_goals = estimate_goals(team_data1, team_data2)

    print(f"\nEstimación de goles para {team_data1['team_name']}: {estimated_goals[team_data1['team_name']]:.2f}")
    print(f"Estimación de goles para {team_data2['team_name']}: {estimated_goals[team_data2['team_name']]:.2f}")

if __name__ == "__main__":
    main()