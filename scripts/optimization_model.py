from gurobipy import Model, GRB, quicksum
from itertools import combinations

def create_optimization_model(n, m, travel_time_matrix, df):
    """
    Creates the optimization model for the multiple Travelling Salesmen Problem with Time Windows (mTSPTW).

    Args:
    n (int): Number of brands (showrooms)
    m (int): Number of retail company buyers
    travel_time_matrix (DataFrame): Matrix of travel times between brands
    df (DataFrame): DataFrame containing brand data with time windows and meeting lengths

    Returns:
    Model: Gurobi optimization model
    """
    model = Model("multiple_Travelling_Salesmen_Time_Window")
    x = model.addVars(n, n, m, vtype=GRB.BINARY, name="x")  # Binary decision variables for travel between showrooms
    t_meeting_start = model.addVars(n, m, vtype=GRB.CONTINUOUS, name="t")  # Start times for meetings at showrooms
    y = model.addVars(n, n, m, vtype=GRB.BINARY, name="y")  # Binary variables for travel between showrooms

    M = 1000  # Large constant for constraints
    meeting_durations = []

    # Constraint 1: Time window constraints
    for i in range(n):
        for j in range(n):
            if i != j:
                for k in range(m):
                    model.addConstr(t_meeting_start[j, k] >= t_meeting_start[i, k] + travel_time_matrix[i][j] - M * (1 - y[i, j, k]))

    # Constraint 2: Time compatibility with showroom's time window
    for j in range(n):
        a = df.at[j, 'Opening hour'].total_seconds() / 3600  # Opening hour in hours
        b = df.at[j, 'Closing hour'].total_seconds() / 3600  # Closing hour in hours
        d = df.at[j, 'Length'].total_seconds() / 3600  # Meeting length in hours
        meeting_durations.append(d)

        for k in range(m):
            model.addConstr(t_meeting_start[j, k] >= a)
            model.addConstr(t_meeting_start[j, k] + d <= b)
            model.addConstr(t_meeting_start[j, k] >= 0)

    # Constraint 3: Each showroom is visited exactly once by one buyer
    for j in range(n):
        sum_entering = quicksum(quicksum(x[i, j, k] for i in range(n)) for k in range(m))
        sum_exiting = quicksum(quicksum(x[j, i, k] for i in range(n)) for k in range(m))
        model.addConstr(sum_entering == 1)
        model.addConstr(sum_exiting == 1)
        model.addConstr(sum_entering == sum_exiting)

    # Constraint 4: Subtour elimination for each buyer
    for k in range(m):
        for S in range(2, n):
            for subset in combinations(range(1, n + 1), S):
                model.addConstr(quicksum(x[i, j, k] for i in subset for j in subset if i != j) <= len(subset) - 1)

    # Objective function: Minimize total travel time and meeting durations
    objective = quicksum(quicksum(quicksum(x[i, j, k] * travel_time_matrix[i][j] for j in range(n) if j != i) for i in range(n)) for k in range(m))
    objective += quicksum(quicksum(x[i, j, k] * meeting_durations[i] for j in range(n) if j != i) for i in range(n) for k in range(m))
    model.setObjective(objective, GRB.MINIMIZE)

    return model
