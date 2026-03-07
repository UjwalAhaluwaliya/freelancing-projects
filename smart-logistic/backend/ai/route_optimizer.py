"""
Route Optimization using Google OR-Tools
Solves the Vehicle Routing Problem (VRP) to find optimal delivery routes.
"""
import math
from typing import List, Tuple

try:
    from ortools.constraint_solver import routing_enums_pb2, pywrapcp
    HAS_ORTOOLS = True
except ImportError:
    HAS_ORTOOLS = False


def haversine_distance(lat1: float, lng1: float, lat2: float, lng2: float) -> float:
    """Calculate the great-circle distance between two points on Earth (in km)."""
    R = 6371  # Earth's radius in km
    dlat = math.radians(lat2 - lat1)
    dlng = math.radians(lng2 - lng1)
    a = math.sin(dlat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlng / 2) ** 2
    c = 2 * math.asin(math.sqrt(a))
    return R * c


def create_distance_matrix(locations: List[Tuple[float, float]]) -> List[List[int]]:
    """Create a distance matrix from a list of (lat, lng) tuples. Distances in meters."""
    n = len(locations)
    matrix = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if i != j:
                dist = haversine_distance(locations[i][0], locations[i][1], locations[j][0], locations[j][1])
                matrix[i][j] = int(dist * 1000)  # Convert to meters for OR-Tools
    return matrix


def optimize_route(depot: Tuple[float, float], stops: List[Tuple[float, float]], 
                   stop_names: List[str], num_vehicles: int = 1) -> dict:
    """
    Optimize delivery route using OR-Tools.
    
    Args:
        depot: (lat, lng) of the depot/starting point
        stops: list of (lat, lng) for delivery stops
        stop_names: names of each stop
        num_vehicles: number of vehicles
    
    Returns:
        dict with optimized_order, total_distance_km, route_polyline
    """
    if not HAS_ORTOOLS:
        # Fallback: nearest neighbor heuristic
        return _nearest_neighbor_fallback(depot, stops, stop_names)

    # All locations: depot + stops
    all_locations = [depot] + stops
    all_names = ["Depot"] + stop_names
    distance_matrix = create_distance_matrix(all_locations)

    # Create routing model
    manager = pywrapcp.RoutingIndexManager(len(all_locations), num_vehicles, 0)
    routing = pywrapcp.RoutingModel(manager)

    def distance_callback(from_index, to_index):
        from_node = manager.IndexToNode(from_index)
        to_node = manager.IndexToNode(to_index)
        return distance_matrix[from_node][to_node]

    transit_callback_index = routing.RegisterTransitCallback(distance_callback)
    routing.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

    # Search parameters
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy = routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
    search_parameters.local_search_metaheuristic = routing_enums_pb2.LocalSearchMetaheuristic.GUIDED_LOCAL_SEARCH
    search_parameters.time_limit.seconds = 5

    solution = routing.SolveWithParameters(search_parameters)

    if not solution:
        return _nearest_neighbor_fallback(depot, stops, stop_names)

    # Extract solution
    route_order = []
    route_polyline = []
    total_distance = 0
    index = routing.Start(0)

    while not routing.IsEnd(index):
        node = manager.IndexToNode(index)
        route_order.append({
            "name": all_names[node],
            "lat": all_locations[node][0],
            "lng": all_locations[node][1],
        })
        route_polyline.append([all_locations[node][0], all_locations[node][1]])
        previous_index = index
        index = solution.Value(routing.NextVar(index))
        total_distance += routing.GetArcCostForVehicle(previous_index, index, 0)

    # Add final node (back to depot or last stop)
    node = manager.IndexToNode(index)
    route_polyline.append([all_locations[node][0], all_locations[node][1]])

    return {
        "optimized_order": route_order,
        "total_distance_km": round(total_distance / 1000, 2),
        "route_polyline": route_polyline,
    }


def _nearest_neighbor_fallback(depot: Tuple[float, float], stops: List[Tuple[float, float]], 
                                stop_names: List[str]) -> dict:
    """Simple nearest-neighbor heuristic as fallback when OR-Tools is not available."""
    if not stops:
        return {"optimized_order": [], "total_distance_km": 0, "route_polyline": []}

    visited = [False] * len(stops)
    route_order = [{"name": "Depot", "lat": depot[0], "lng": depot[1]}]
    route_polyline = [[depot[0], depot[1]]]
    current = depot
    total_distance = 0

    for _ in range(len(stops)):
        best_dist = float("inf")
        best_idx = -1
        for j, stop in enumerate(stops):
            if not visited[j]:
                d = haversine_distance(current[0], current[1], stop[0], stop[1])
                if d < best_dist:
                    best_dist = d
                    best_idx = j
        
        visited[best_idx] = True
        total_distance += best_dist
        current = stops[best_idx]
        route_order.append({
            "name": stop_names[best_idx],
            "lat": stops[best_idx][0],
            "lng": stops[best_idx][1],
        })
        route_polyline.append([stops[best_idx][0], stops[best_idx][1]])

    return {
        "optimized_order": route_order,
        "total_distance_km": round(total_distance, 2),
        "route_polyline": route_polyline,
    }
