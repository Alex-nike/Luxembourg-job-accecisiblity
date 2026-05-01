import geopandas as gpd
from pathlib import Path


def load_data(pr_path, gtfs_path):
    """Load GeoPackage files."""
    stops_pr = gpd.read_file(pr_path)
    stops_gtfs = gpd.read_file(gtfs_path)
    return stops_pr, stops_gtfs


def reproject_data(stops_pr, stops_gtfs, crs="EPSG:32632"):
    """Reproject both datasets to a metric CRS."""
    stops_pr = stops_pr.to_crs(crs)
    stops_gtfs = stops_gtfs.to_crs(crs)
    return stops_pr, stops_gtfs


def build_mapping(stops_pr, stops_gtfs, max_distance=200):
    """Create P+R → GTFS mapping."""
    
    # Spatial nearest join
    pr_to_gtfs = gpd.sjoin_nearest(
        stops_pr,
        stops_gtfs,
        how="left",
        distance_col="distance_m"
    )

    # Keep only relevant fields
    mapping = pr_to_gtfs[
        ["P+R_stop", "stop_id", "distance_m"]
    ]

    # Filter by distance
    mapping = mapping[mapping["distance_m"] < max_distance]

    # Remove duplicates
    mapping = mapping.drop_duplicates(subset=["P+R_stop", "stop_id"])

    return mapping


def validate_mapping(mapping):
    """Basic sanity checks."""
    print("\n--- Mapping Summary ---")
    print(f"Total rows: {len(mapping)}")
    print(f"Unique P+R stops: {mapping['P+R_stop'].nunique()}")
    print(f"Unique GTFS stops: {mapping['stop_id'].nunique()}")

    print("\nStops per P+R:")
    print(mapping.groupby("P+R_stop").size().describe())

    print("\nDistance stats (meters):")
    print(mapping["distance_m"].describe())


def save_mapping(mapping, output_path):
    """Save mapping to CSV."""
    mapping.to_csv(output_path, index=False)
    print(f"\nSaved mapping to: {output_path}")


def main():
    base_path = Path(r"C:\Users\luca\Downloads\Lux_public_transport_project")

    pr_file = base_path / "P+R_stations.gpkg"
    gtfs_file = base_path / "stops_freq.gpkg"
    output_file = base_path / "pr_to_gtfs_mapping.csv"
    
    stops_pr, stops_gtfs = load_data(pr_file, gtfs_file)
    stops_pr, stops_gtfs = reproject_data(stops_pr, stops_gtfs)

    mapping = build_mapping(stops_pr, stops_gtfs)

    validate_mapping(mapping)
    save_mapping(mapping, output_file)


if __name__ == "__main__":
    main()