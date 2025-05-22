# PASCAL NDVI Block

© 2025 AustralMetrics SpA. All rights reserved.

A high-performance module for calculating NDVI, NDRE, and SAVI indices from Sentinel-2/Landsat imagery, focusing on simplicity and ISO 42001 compliance.

## Project Status
![Tests & Lint](https://github.com/australmetrics/pascal-ndvi-block/actions/workflows/test.yml/badge.svg)
[![ISO 42001](https://img.shields.io/badge/ISO-42001-blue.svg)](docs/compliance/iso42001_compliance.md)

- **Version**: 1.0.0
- **Compatibility**: Windows, Linux, macOS
- **Python**: 3.7+

## Features

- **Simplified Input**: Process satellite imagery without complex configuration files
- **Automatic Detection**: Smart identification of spectral bands based on image type
- **Multiple Indices**: Calculate NDVI, NDRE, and SAVI in a single pass
- **Intuitive CLI**: Simple commands for all operations
- **Automated Pipeline**: Complete processing with a single command

## Quality Control & CI/CD

This project implements robust Continuous Integration (CI) and Continuous Delivery (CD) practices:

- **Automated Testing**: Every push and pull request triggers:
  - Unit tests with pytest
  - Style verification with flake8
  - Type checking with mypy
- **Quality Control**: 
  - 100-character line limit
  - Consistent formatting
  - Mandatory documentation

## Traceability & Audit

ISO 42001-compliant logging system:

- **Location**: `results/logs/`
  - Main logs: `pascal_ndvi_YYYYMMDD_HHMMSS.log`
  - Automatic backups: `backup/pascal_ndvi_*_backup.log`
  - Integrity verification: SHA-256 hashes in `*.sha256`
- **Logged Information**:
  - Precise timestamps
  - User and process data
  - Input parameters
  - Results and errors

## Installation

```bash
# Clone repository
git clone https://github.com/australmetrics/pascal-ndvi-block.git
cd pascal-ndvi-block

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # Linux/Mac
# or
venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt
```

## Basic Usage

### Simple Index Calculation

```bash
# Calculate all indices for an image
python -m src.main indices --image=data/my_image.tif

# Specify output directory
python -m src.main indices --image=data/my_image.tif --output=results
```

### Process with Clipping (optional)

```bash
# Clip image using shapefile
python -m src.main clip --image=data/my_image.tif --shapefile=data/area.shp

# Complete processing: clip + indices
python -m src.main auto --image=data/my_image.tif --shapefile=data/area.shp
```

### Automated Processing

```bash
# Simplest option: image only, no clipping
python -m src.main auto --image=data/my_image.tif
```

## Project Structure

```
pascal-ndvi-block/
├── data/                  # Input imagery folder
├── results/              # Generated results (default)
├── src/
│   ├── __init__.py
│   ├── main.py            # Punto de entrada y CLI
│   ├── preprocessor.py    # Funciones de preprocesamiento (recorte)
│   └── indices.py         # Cálculo de índices vegetativos
├── tests/
│   └── test_main.py       # Tests unitarios
├── README.md
└── requirements.txt
```

## Conformidad con ISO 42001

Este módulo está diseñado siguiendo los principios de ISO 42001 para sistemas de gestión de inteligencia artificial:

- **Simplicidad**: Interfaces mínimas y flujos de trabajo claros
- **Documentación**: Código y APIs completamente documentados
- **Mantenibilidad**: Estructura modular y pruebas automatizadas
- **Reproducibilidad**: Resultados consistentes con los mismos datos de entrada
- **Trazabilidad**: Registro detallado del procesamiento mediante loguru

## Requisitos

- Python 3.7+
- rasterio
- geopandas
- numpy
- typer
- loguru

## Soporte y Contacto

- **Repositorio Interno**: Crear issue en GitHub para reportar problemas
- **Documentación**: Ver documentación en la carpeta `docs/` del repositorio
- **Contacto**: Contactar al equipo de desarrollo de AustralMetrics SpA

## Licencia y Uso

Este software es propiedad de AustralMetrics SpA. Su uso, modificación y distribución está restringido a personal autorizado de la empresa.

