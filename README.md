# ChIP-Seq Similarity Search

A web application for finding similar ChIP-Seq peak files using Jaccard index similarity measure.

## Overview

This application allows users to upload BED files containing genomic intervals and find similar files from a pre-processed database of ChIP-Seq peak files. The similarity is calculated using the Jaccard index, which measures the overlap between genomic intervals.

## Features

- Modern, responsive web interface
- Secure file upload handling
- Real-time similarity calculation
- Visual representation of similarity scores
- Detailed results with file descriptions
- Error handling and user feedback

## Database

The application uses a pre-processed database containing the following ChIP-Seq datasets:
- CTCF ChIP-seq on human Monocytes-CD14+ (RO01746)
- H3K27me3 ChIP-seq on human monocytes CD14+ (RO01746)
- H3K36me3 ChIP-seq on human monocytes CD14+ (RO01746)
- H3K4me1 ChIP-seq on human Monocytes CD14+ (RO01746)
- H3K4me3 ChIP-seq on human monocytes CD14+ (RO01746)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd chip-seq-similarity
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Start the Flask application:
```bash
python app.py
```

2. Open your web browser and navigate to `http://localhost:5000`

3. Upload a BED file and specify the number of similar files to find

4. View the results showing the most similar files from the database

## Technical Details

### Similarity Calculation

The Jaccard index is calculated as:
```
Jaccard(A,B) = |A ∩ B| / |A ∪ B|
```
where:
- A ∩ B is the intersection of intervals in files A and B
- A ∪ B is the union of intervals in files A and B

### File Format

The application accepts BED files (Browser Extensible Data) with the following format:
```
chromosome start end [name] [score] [strand]
```

### Dependencies

- Flask: Web framework
- pybedtools: BED file processing
- Bootstrap 5: Frontend framework

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments

- ENCODE project for the ChIP-Seq datasets
- pybedtools developers for the BED file processing library
