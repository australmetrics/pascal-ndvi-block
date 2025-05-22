"""Módulo principal de PASCAL NDVI Block.

Este módulo proporciona la interfaz de línea de comandos y las funciones
principales para procesar imágenes satelitales y calcular índices vegetativos.
"""

from pathlib import Path
import typer
from loguru import logger
from typing import Optional, List, Dict
from src.preprocessor import clip_image_with_shapefile
from src.indices import calculate_all_indices
from src.logging_config import setup_logging

app = typer.Typer()


def init_logging(output_dir: Path) -> None:
    """Inicializa el sistema de logging."""
    setup_logging(output_dir)
    logger.info("🚀 Iniciando P.A.S.C.A.L NDVI Block")
    logger.info(f"📁 Directorio de salida: {output_dir}")


@app.command("clip")
def clip(
    image: Path = typer.Option(..., exists=True, help="Archivo .tif multibanda"),
    shapefile: Path = typer.Option(..., exists=True, help="Archivo .shp de polígonos"),
    output: Path = typer.Option("results", help="Directorio de salida"),
) -> Path:
    """Recorta una imagen satelital usando un shapefile.

    Args:
        image: Ruta al archivo de imagen multibanda.
        shapefile: Ruta al archivo shapefile con polígonos.
        output: Directorio donde guardar el resultado.

    Returns:
        Path: Ruta al archivo recortado.
    """
    # Inicializar logging
    init_logging(Path(output))
    """
    Recorta una imagen satelital usando un shapefile de polígonos.
    """
    logger.info(f"🛰️ Iniciando recorte de: {image}")
    logger.info(f"🗺️ Usando shapefile: {shapefile}")

    output.mkdir(parents=True, exist_ok=True)

    clipped_path = clip_image_with_shapefile(image, shapefile, output)
    logger.success(f"✅ Imagen recortada guardada en: {clipped_path}")

    return clipped_path


@app.command("indices")
def indices(
    image: Path = typer.Option(..., exists=True, help="Archivo .tif multibanda"),
    output: Path = typer.Option("results", help="Directorio de salida"),
    indices_list: Optional[List[str]] = typer.Option(
        None,
        help="Lista de índices a calcular (ndvi,ndre,savi). Por defecto calcula todos.",
    ),
) -> Dict[str, Path]:
    """Calcula índices vegetativos para una imagen satelital.

    Args:
        image: Ruta al archivo de imagen multibanda.
        output: Directorio donde guardar los resultados.
        indices_list: Lista opcional de índices a calcular.

    Returns:
        Dict[str, Path]: Diccionario con nombres de índices y rutas a los archivos.
    """
    # Inicializar logging
    init_logging(Path(output))
    """
    Calcula índices vegetativos (NDVI, NDRE, SAVI) a partir de una imagen.
    """
    logger.info(f"🛰️ Procesando imagen: {image}")
    logger.info("📊 Calculando índices vegetativos")  # Removido f-string innecesario

    output.mkdir(parents=True, exist_ok=True)

    result_paths = calculate_all_indices(image, output)

    for index_name, path in result_paths.items():
        logger.success(f"✅ Índice {index_name.upper()} guardado en: {path}")

    return result_paths


@app.command("auto")
def auto_process(
    image: Path = typer.Option(..., exists=True, help="Archivo .tif multibanda"),
    shapefile: Optional[Path] = typer.Option(
        None, exists=True, help="Archivo .shp opcional"
    ),
    output: Path = typer.Option("results", help="Directorio de salida"),
) -> Dict[str, Path]:
    """Procesa una imagen automáticamente, opcional con recorte.

    Args:
        image: Ruta al archivo de imagen multibanda.
        shapefile: Ruta opcional al archivo shapefile para recorte.
        output: Directorio donde guardar los resultados.

    Returns:
        Dict[str, Path]: Diccionario con nombres de índices y rutas a los archivos.
    """
    # Inicializar logging
    init_logging(Path(output))
    """
    Proceso automático: opcional recorte + cálculo de todos los índices.
    """
    logger.info(f"🚀 Iniciando procesamiento automático de {image}")

    output.mkdir(parents=True, exist_ok=True)

    # Paso 1: Recortar si se proporciona shapefile
    processed_image = image
    if shapefile:
        logger.info("✂️ Recortando imagen")
        logger.debug(f"Usando shapefile: {shapefile}")
        processed_image = clip_image_with_shapefile(
            image_path=image, shapefile_path=shapefile, output_path=output
        )  # Realizar recorte

    # Paso 2: Calcular índices
    logger.info("📊 Calculando índices vegetativos")
    result_paths = calculate_all_indices(processed_image, output)

    for index_name, path in result_paths.items():
        logger.success(f"✅ Índice {index_name.upper()} guardado en: {path}")

    logger.success(f"🏁 Procesamiento completo. Resultados en: {output}")
    return result_paths


def process_image(
    image_path: Path, output_dir: Path, indices: List[str], savi_l: float = 0.5
) -> Dict[str, Path]:
    """
    Función principal para procesar una imagen satelital y calcular índices vegetativos.
    Esta función implementa el flujo de trabajo principal según ISO 42001.

    Args:
        image_path: Ruta a la imagen satelital multibanda
        output_dir: Directorio donde guardar los resultados
        indices: Lista de índices a calcular (ndvi, savi, ndre)
        savi_l: Factor de ajuste para el índice SAVI

    Returns:
        Diccionario con los nombres de índices y rutas a los archivos generados
    """
    # Inicializar logging
    init_logging(output_dir)

    # Crear directorio de salida
    output_dir.mkdir(parents=True, exist_ok=True)

    # Procesar imagen y calcular índices
    logger.info(f"🛰️ Procesando imagen: {image_path}")
    logger.info(f"📊 Calculando índices: {', '.join(indices)}")

    result_paths = calculate_all_indices(image_path, output_dir)

    # Registrar resultados
    for index_name, path in result_paths.items():
        if index_name in indices:
            logger.success(f"✅ Índice {index_name.upper()} guardado en: {path}")

    # Filtrar solo los índices solicitados
    return {k: v for k, v in result_paths.items() if k in indices}


if __name__ == "__main__":
    app()
