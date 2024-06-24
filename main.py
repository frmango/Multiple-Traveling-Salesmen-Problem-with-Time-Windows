from scripts.data_processing import load_data, preprocess_data
from scripts.api_utils import calculate_brand_travel_time_matrix
from scripts.optimization_model import create_optimization_model

def main():
    # Load and preprocess data
    file_path = 'data/Modacruising.xlsx'
    df = load_data(file_path)
    df = preprocess_data(df)

    # Set parameters
    n = len(df)  # Number of brands (showrooms)
    m = 2  # Number of retail company buyers
    api_key = "Please insert yours here"  # Google Maps API key

    # Calculate travel time matrix
    travel_time_matrix = calculate_brand_travel_time_matrix(df, api_key)

    # Create optimization model
    model = create_optimization_model(n, m, travel_time_matrix, df)

    # Optimize model
    model.optimize()

    # Print results
    if model.status == GRB.OPTIMAL:
        print("Optimal solution found.")
    else:
        print("No optimal solution found.")

if __name__ == "__main__":
    main()
