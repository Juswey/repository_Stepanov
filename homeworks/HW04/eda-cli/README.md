# S03 – eda_cli: мини-EDA для CSV

Небольшое CLI-приложение для базового анализа CSV-файлов.
Используется в рамках Семинара 03 курса «Инженерия ИИ».

## Требования

- Python 3.11+
- [uv](https://docs.astral.sh/uv/) установлен в систему

## Инициализация проекта

В корне проекта (S03):

```bash
uv sync
```

Эта команда:

- создаст виртуальное окружение `.venv`;
- установит зависимости из `pyproject.toml`;
- установит сам проект `eda-cli` в окружение.

## Запуск CLI

### Краткий обзор

```bash
uv run eda-cli overview data/example.csv
```

Параметры:

- `--sep` – разделитель (по умолчанию `,`);
- `--encoding` – кодировка (по умолчанию `utf-8`).

## Полный EDA-отчёт

```bash
uv run eda-cli report data/example.csv --out-dir reports
```

В результате в каталоге `reports/` появятся:

- `report.md` – основной отчёт в Markdown;
- `summary.csv` – таблица по колонкам;
- `missing.csv` – пропуски по колонкам;
- `correlation.csv` – корреляционная матрица (если есть числовые признаки);
- `top_categories/*.csv` – top-k категорий по строковым признакам;
- `hist_*.png` – гистограммы числовых колонок;
- `missing_matrix.png` – визуализация пропусков;
- `correlation_heatmap.png` – тепловая карта корреляций;
- `--top-k-categories` – сколько top-значений выводить для категориальных признаков (по умолчанию: 5);
- `--min-missing-share` – порог доли пропусков для выделения проблемных колонок (по умолчанию: 0.3);
- `--max-hist-columns` – сколько числовых колонок включать в гистограммы (можно изменить).

## Тесты

```bash
uv run pytest -q
```
## HTTP-сервис (FastAPI)

Запуск сервиса:
```bash
uv run uvicorn eda_cli.api:app --reload --port 8000
```
Доступные эндпоинты:
GET /health
Проверка работоспособности сервиса. Возвращает статус и версию.

POST /quality
Оценка качества датасета на основе переданных метрик в JSON.

## Пример запроса:

```bash
curl -X POST "http://localhost:8000/quality" \
  -H "Content-Type: application/json" \
  -d '{
    "n_rows": 1000,
    "n_cols": 10,
    "missing_share": 0.05,
    "quality_score": 0.85
  }'
```
## POST /quality-from-csv
Оценка качества датасета из загруженного CSV-файла.

Пример запроса:

```bash
curl -X POST "http://localhost:8000/quality-from-csv" \
  -F "file=@data/example.csv"
```
## POST /quality-flags-from-csv
Полный набор флагов качества для CSV-файла, включая расширенные эвристики из HW03.

Пример запроса:

```bash
curl -X POST "http://localhost:8000/quality-flags-from-csv" \
  -F "file=@data/example.csv"
```
Пример ответа:

json
{
  "flags": {
    "too_few_rows": false,
    "too_many_missing": true,
    "has_constant_columns": false,
    "has_high_cardinality_categoricals": true,
    "has_suspicious_id_duplicates": false,
    "has_many_zero_values": true
  }
}

## Документация API:
После запуска сервиса документация доступна по адресам:

```
http://localhost:8000/docs (Swagger UI)

http://localhost:8000/redoc (ReDoc)
```

## Тесты
```bash
uv run pytest -q
```

## Структура проекта (HW04)
```
HW04/eda-cli/
  pyproject.toml
  README.md
  src/eda_cli/
    api.py        # FastAPI приложение
    cli.py        # CLI интерфейс
    core.py       # EDA и расчёт метрик
    viz.py        # Визуализация
  data/
    example.csv
  tests/
    test_core.py
```

## Примечания
CLI и HTTP-сервис используют общий код анализа данных

Проект предназначен для учебных целей и демонстрации простого ML/EDA пайплайна

Для HW04 был добавлен новый эндпоинт /quality-flags-from-csv, использующий эвристики качества данных из HW03