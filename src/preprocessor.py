"""Módulo de preprocesamiento de imágenes satelitales.

Este módulo proporciona funciones para preparar las imágenes antes del cálculo
de índices, incluyendo recorte con shapefiles y validación de datos.
"""

from pathlib import Path
import rasterio
import geopandas as gpd
from rasterio.mask import mask
from shapely.geometry import mapping
from loguru import logger


def clip_image_with_shapefile(
    image_path: Path, shapefile_path: Path, output_path: Path
) -> Path:
    """
    Recorta una imagen satelital multibanda usando un shapefile de polígonos.

    Args:
        image_path (Path): Ruta al archivo .tif
        shapefile_path (Path): Ruta al archivo .shp
        output_path (Path): Carpeta donde guardar el resultado

    Returns:
        Path: Ruta al nuevo archivo TIFF recortado
    """
    logger.info("🧩 Cargando shapefile...")
    gdf = gpd.read_file(shapefile_path)

    logger.info("🌍 Cargando imagen satelital...")
    with rasterio.open(image_path) as src:
        image_crs = src.crs
        if gdf.crs != image_crs:
            logger.warning(f"⚠️ Reproyectando shapefile desde {gdf.crs} a {image_crs}")
            gdf = gdf.to_crs(image_crs)

        geoms = [mapping(geom) for geom in gdf.geometry]
        clipped_image, clipped_transform = mask(src, geoms, crop=True)

        meta = src.meta.copy()
        meta.update(
            {
                "driver": "GTiff",
                "height": clipped_image.shape[1],
                "width": clipped_image.shape[2],
                "transform": clipped_transform,
            }
        )

        output_path.mkdir(parents=True, exist_ok=True)
        out_file = output_path / f"{image_path.stem}_clipped.tif"
        with rasterio.open(out_file, "w", **meta) as dst:
            dst.write(clipped_image)

        logger.success(f"✅ Imagen recortada guardada en {out_file}")

        return out_file
