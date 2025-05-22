"""Configuración del sistema de logging para el proyecto PASCAL NDVI Block.

Este módulo proporciona funciones para configurar el sistema de logging,
incluyendo manejo de archivos de log, rotación, y formatos personalizados
que cumplen con ISO 42001.
"""

from loguru import logger
import sys
import os
import hashlib
import shutil
from pathlib import Path
from datetime import datetime


def calculate_hash(file_path: Path) -> str:
    """Calcula el hash SHA-256 de un archivo."""
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()


def backup_log(log_file: Path, backup_dir: Path) -> None:
    """Crea una copia de respaldo del archivo de log."""
    backup_dir.mkdir(parents=True, exist_ok=True)
    backup_file = backup_dir / f"{log_file.stem}_backup{log_file.suffix}"
    shutil.copy2(log_file, backup_file)

    # Crear archivo de verificación con hash
    hash_value = calculate_hash(log_file)
    hash_file = backup_file.with_suffix(".sha256")
    hash_file.write_text(hash_value)


def setup_logging(output_dir: Path) -> None:
    """
    Configura el sistema de logging para ISO 42001.
    Implementa logging auditable y permanente según estándares.

    Args:
        output_dir: Directorio donde guardar los logs
    """
    # Crear directorios
    log_dir = output_dir / "logs"
    backup_dir = output_dir / "logs" / "backup"
    log_dir.mkdir(parents=True, exist_ok=True)
    backup_dir.mkdir(parents=True, exist_ok=True)

    # Formato para auditoría ISO 42001
    log_format = (
        "[{time:YYYY-MM-DD HH:mm:ss.SSS}] "
        "{process}.{thread} | "
        "{level: <8} | "
        "{name}:{function}:{line} | "
        "usuario={extra[user]} | "
        "hash={extra[hash]} | "
        "{message}"
    )

    # Archivo de log con fecha y hora exacta
    current_datetime = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_file = log_dir / f"pascal_ndvi_{current_datetime}.log"

    # Configurar contexto para auditoría
    logger.configure(
        extra={"user": os.getenv("USERNAME", "unknown"), "hash": "calculating..."}
    )

    # Log a archivo (sin rotación - permanente)
    logger.add(
        log_file,
        format=log_format,
        level="INFO",
        rotation=None,  # Sin rotación - logs permanentes
        enqueue=True,  # Thread-safe
        backtrace=True,  # Más info para debug
        diagnose=True,  # Más info para diagnóstico
    )

    # Log a consola (formato simplificado)
    logger.add(
        sys.stderr,
        format=(
            "<green>{time:HH:mm:ss}</green> | "
            "<level>{level: <8}</level> | "
            "<cyan>{name}</cyan> | {message}"
        ),
        level="INFO",
    )

    # Registrar inicio con metadata
    logger.info("🚀 Iniciando P.A.S.C.A.L NDVI Block")
    logger.info(f"📁 Directorio de salida: {output_dir}")
    logger.info(f"📝 Archivo de log: {log_file}")

    # Crear backup inmediatamente
    backup_log(log_file, backup_dir)

    # Registrar también backup al finalizar por si hay cambios
    import atexit

    atexit.register(backup_log, log_file, backup_dir)
