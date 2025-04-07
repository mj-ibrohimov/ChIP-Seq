import os
import json
import pybedtools
from tqdm import tqdm

DATABASE_RAW = "database/raw"
DATABASE_PROCESSED = "database/processed"
METADATA_FILE = os.path.join(DATABASE_PROCESSED, "metadata.json")

def process_bed_file(filename):
    """Process a BED file: merge intervals and calculate total length"""
    bed = pybedtools.BedTool(os.path.join(DATABASE_RAW, filename))
    merged = bed.sort().merge()
    
    # Calculate total length
    total_length = sum(interval.length for interval in merged)
    
    # Save processed file
    processed_path = os.path.join(DATABASE_PROCESSED, filename)
    merged.saveas(processed_path)
    
    return {
        "filename": filename,
        "processed_path": processed_path,
        "total_length": total_length
    }

def main():
    os.makedirs(DATABASE_PROCESSED, exist_ok=True)
    
    metadata = []
    for bed_file in tqdm(os.listdir(DATABASE_RAW)):
        if bed_file.endswith(".bed"):
            metadata.append(process_bed_file(bed_file))
    
    with open(METADATA_FILE, 'w') as f:
        json.dump(metadata, f, indent=2)

if __name__ == "__main__":
    main()