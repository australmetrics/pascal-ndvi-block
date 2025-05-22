# PASCAL NDVI Block Technical Documentation

## Implemented Vegetation Indices

### NDVI (Normalized Difference Vegetation Index)
```python
def calculate_ndvi(red_band: np.ndarray, nir_band: np.ndarray) -> np.ndarray:
    """
    NDVI = (NIR - RED) / (NIR + RED)
    Range: -1.0 to 1.0
    """
```
- **Input**: Red and NIR bands as NumPy arrays
- **Output**: Array with NDVI values
- **Validation**: Verifies dimensions and data types

### SAVI (Soil Adjusted Vegetation Index)
```python
def calculate_savi(red_band: np.ndarray, nir_band: np.ndarray, L: float = 0.5) -> np.ndarray:
    """
    SAVI = ((NIR - RED) / (NIR + RED + L)) * (1 + L)
    L = soil adjustment factor (0 to 1)
    """
```
- **Input**: Red band, NIR band, and L factor
- **Output**: Array with SAVI values
- **Validation**: Verifies L range (0-1)

## Preprocessing

### Image Clipping
```python
def clip_raster(image_path: Path, shapefile_path: Path) -> Path:
    """
    Clips raster image using a shapefile
    """
```
- **Input**: Paths to image and shapefile
- **Output**: Path to clipped image
- **Validation**: Verifies CRS and extent

## Logging System

### Configuration
```python
def setup_logging(output_dir: Path) -> None:
    """
    Configures ISO 42001 compliant logging system
    """
```
- Format: Timestamp, process, user
- Backup: Automático con hash SHA-256
- Retención: 90 días por defecto

## Gestión de Memoria

### Procesamiento por Bloques
- Tamaño máximo de imagen: 10GB
- Procesamiento en chunks de 1024x1024
- Uso de memoria monitoreado

## Límites y Validaciones

### Validaciones de Entrada
- Formatos soportados: GeoTIFF
- Satélites: Sentinel-2, Landsat 8
- Cobertura de nubes: <50%

### Validaciones de Salida
- Rango de valores NDVI: [-1, 1]
- Rango de valores SAVI: [-1, 1]
- Metadata preservada

## APIs y Funciones

### Función Principal
```python
def process_image(
    image_path: Path,
    output_dir: Path,
    indices: List[str],
    savi_l: float = 0.5
) -> Dict[str, Path]:
```

### Parámetros Configurables
```python
MAX_IMAGE_SIZE_GB = 10.0
DEFAULT_SAVI_L = 0.5
LOG_RETENTION_DAYS = 90
```

## Manejo de Errores

### Errores Controlados
- ImageTooLargeError
- InvalidBandError
- ProcessingError
- ValidationError

### Logging de Errores
- Stacktrace completo
- Contexto de error
- Estado del sistema
