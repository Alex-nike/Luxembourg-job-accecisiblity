import geopandas as gpd
from pathlib import Path

def load_data(quarters_path, commercial_path, stops_path):
    """Load spatial datasets."""
    quarters = gpd.read_file(quarters_path)
    commercial = gpd.read_file(commercial_path)
    stops = gpd.read_file(stops_path)
    return quarters, commercial, stops


def reproject_data(quarters, commercial, stops, crs="EPSG:2169"):
    """Ensure all layers share a projected CRS."""
    quarters = quarters.to_crs(crs)
    commercial = commercial.to_crs(crs)
    stops = stops.to_crs(crs)
    return quarters, commercial, stops


def compute_coverage(quarters, commercial):
    """Compute commercial land-use coverage per quarter."""
    
    # Intersection
    commercial_intersect = gpd.overlay(quarters, commercial, how='intersection')
    commercial_intersect["comm_area"] = commercial_intersect.geometry.area

    # Aggregate per quarter
    comm_area_quarter = (
        commercial_intersect
        .groupby("FK_QUART_NAME")["comm_area"]
        .sum()
        .reset_index()
    )

    # Total area
    quarters["total_area"] = quarters.geometry.area

    # Merge + compute ratio
    quarters = (
        quarters
        .merge(comm_area_quarter, on="FK_QUART_NAME", how="left")
        .fillna(0)
    )

    quarters["coverage"] = quarters["comm_area"] / quarters["total_area"]

    return quarters


def select_top_districts(quarters, top_n=5):
    """Select top N districts by coverage."""
    top_districts = quarters.sort_values("coverage", ascending=False).head(top_n)
    return top_districts


def extract_commercial_in_districts(commercial, top_districts):
    """Clip commercial land-use to top districts."""
    top_comm = gpd.overlay(commercial, top_districts, how="intersection")
    return top_comm


def find_candidate_stops(top_comm, stops, max_distance=50):
    """Find nearby PT stops for commercial areas."""
    
    stops_near = gpd.sjoin_nearest(
        top_comm,
        stops,
        how="left",
        distance_col="dist"
    )

    # Apply distance threshold
    stops_near = stops_near[stops_near["dist"] < max_distance]

    # Keep relevant fields
    stops_comm = (
        stops_near[["FK_QUART_NAME", "stop_id", "dist"]]
        .drop_duplicates()
    )

    return stops_comm


def validate_outputs(top_districts, stops_comm):
    """Basic QA checks."""
    print("\n--- District Summary ---")
    print(f"Number of districts: {len(top_districts)}")
    print(top_districts["coverage"].describe())

    print("\n--- Stop Mapping Summary ---")
    print(f"Total mappings: {len(stops_comm)}")
    print(f"Unique districts: {stops_comm['FK_QUART_NAME'].nunique()}")
    print(f"Unique stops: {stops_comm['stop_id'].nunique()}")

    print("\nStops per district:")
    print(stops_comm.groupby("FK_QUART_NAME").size().describe())

    print("\nDistance stats (meters):")
    print(stops_comm["dist"].describe())


def save_outputs(top_districts, stops_comm, top_comm,
                 districts_out, stops_out, commercial_out):
    """Save outputs to disk."""

    top_districts[["FK_QUART_NAME", "coverage", "geometry"]].to_file(
        districts_out,
        driver="GPKG"
    )

    stops_comm.to_csv(stops_out, index=False)

    top_comm.to_file(commercial_out, driver="GPKG")

    print("\nSaved outputs:")
    print(f"- Districts: {districts_out}")
    print(f"- Stops: {stops_out}")
    print(f"- Commercial areas: {commercial_out}")


def main():
    base_path = Path(r"C:\Users\luca\Downloads\Lux_public_transport_project")

    quarters_fp = base_path / "Lux_quaters.geojson"
    commercial_fp = base_path / "Commerical_land.gpkg"
    stops_fp = base_path / "stops_freq.gpkg"

    districts_out = base_path / "business_districts.gpkg"
    stops_out = base_path / "district_candidate_stops.csv"
    commercial_out = base_path / "top_district_commercial.gpkg"

    # Load
    quarters, commercial, stops = load_data(
        quarters_fp, commercial_fp, stops_fp
    )

    # Reproject
    quarters, commercial, stops = reproject_data(
        quarters, commercial, stops
    )

    # Compute coverage
    quarters = compute_coverage(quarters, commercial)

    # Select districts
    top_districts = select_top_districts(quarters, top_n=5)

    # Extract commercial areas
    top_comm = extract_commercial_in_districts(commercial, top_districts)

    # Find candidate stops
    stops_comm = find_candidate_stops(top_comm, stops, max_distance=50)

    # Validate
    validate_outputs(top_districts, stops_comm)

    # Save
    save_outputs(
        top_districts,
        stops_comm,
        top_comm,
        districts_out,
        stops_out,
        commercial_out
    )


if __name__ == "__main__":
    main()



