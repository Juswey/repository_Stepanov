from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
import pandas as pd
from .core import (
    summarize_dataset,
    missing_table,
    compute_quality_flags,
    DatasetSummary
)
import time

app = FastAPI(
    title="EDA Quality Service",
    description="HTTP-сервис для оценки качества датасетов",
    version="0.2.0"
)


class QualityRequest(BaseModel):
    n_rows: int
    n_cols: int
    max_missing_share: float
    numeric_cols: List[str]
    categorical_cols: List[str]


class QualityResponse(BaseModel):
    ok_for_model: bool
    quality_score: float
    message: str
    latency_ms: float
    flags: Dict[str, Any]
    dataset_shape: Dict[str, int]


@app.get("/health")
async def health():
    return {
        "status": "ok",
        "service": "eda-quality",
        "version": "0.2.0"
    }


@app.post("/quality", response_model=QualityResponse)
async def quality_prediction(request: QualityRequest):
    start = time.perf_counter()
    
    # Простейшая эвристика для качества
    score = 1.0
    if request.n_rows < 100:
        score -= 0.3
    if request.max_missing_share > 0.5:
        score -= 0.4
    if request.n_cols > 50:
        score -= 0.1
    
    score = max(0.0, min(1.0, score))
    
    flags = {
        "too_few_rows": request.n_rows < 100,
        "too_many_missing": request.max_missing_share > 0.5,
        "too_many_columns": request.n_cols > 50,
    }
    
    latency_ms = (time.perf_counter() - start) * 1000
    
    return QualityResponse(
        ok_for_model=score > 0.5,
        quality_score=score,
        message="Эвристическая оценка качества",
        latency_ms=latency_ms,
        flags=flags,
        dataset_shape={"n_rows": request.n_rows, "n_cols": request.n_cols}
    )


@app.post("/quality-from-csv", response_model=QualityResponse)
async def quality_from_csv(file: UploadFile = File(...)):
    start = time.perf_counter()
    
    # Проверка расширения
    if not file.filename.endswith('.csv'):
        raise HTTPException(400, "Файл должен быть CSV")
    
    try:
        df = pd.read_csv(file.file)
    except Exception as e:
        raise HTTPException(400, f"Ошибка чтения CSV: {e}")
    
    # Используем функции из core.py
    summary = summarize_dataset(df)
    missing_df = missing_table(df)
    quality_flags = compute_quality_flags(summary, missing_df)
    
    latency_ms = (time.perf_counter() - start) * 1000
    
    return QualityResponse(
        ok_for_model=quality_flags["quality_score"] > 0.5,
        quality_score=quality_flags["quality_score"],
        message="Оценка качества на основе CSV",
        latency_ms=latency_ms,
        flags=quality_flags,
        dataset_shape={"n_rows": summary.n_rows, "n_cols": summary.n_cols}
    )

@app.post("/quality-flags-from-csv")
async def quality_flags_from_csv(file: UploadFile = File(...)):
    """
    Возвращает полный набор флагов качества для загруженного CSV-файла.
    """
    if not file.filename.endswith('.csv'):
        raise HTTPException(400, "Файл должен быть CSV")
    
    try:
        df = pd.read_csv(file.file)
    except Exception as e:
        raise HTTPException(400, f"Ошибка чтения CSV: {e}")
    
    summary = summarize_dataset(df)
    missing_df = missing_table(df)
    quality_flags = compute_quality_flags(summary, missing_df)
    
    return {"flags": quality_flags}