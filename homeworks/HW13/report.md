# Отчёт по HW13

## 1. Датасет
- Название: `emotion` (из библиотеки `datasets`)
- Классы: sadness, joy, love, anger, fear, surprise (6 классов)
- Разбиение: train (16000), validation (2000), test (2000)
- Пример текста: *"i am feeling very sad and lonely"* → sadness

## 2. Токенизация
- Использован токенизатор `bert-base-uncased`
- Продемонстрированы: разбиение на токены, `input_ids`, `attention_mask`, special tokens (`[CLS]`, `[SEP]`)
- Показано применение `padding` и `truncation` до 128 токенов

## 3. Инференс готовой модели
- Модель: `bhadresh-savani/bert-base-uncased-emotion` (уже обучена на эмоциях)
- На 5 примерах модель правильно определила эмоции (joy, sadness, love, anger, fear)
- Вывод: готовая модель хорошо подходит для задачи, но в рамках ДЗ мы дообучаем `bert-base-uncased` с нуля

## 4. Fine-tuning
- Базовая модель: `bert-base-uncased`
- Гиперпараметры: эпох = 3, lr = 2e-5 (по умолчанию в Trainer), batch_size = 16 (train) / 64 (eval)
- Лучшая модель выбрана по `f1_macro` на валидации (early stopping patience=2)
- Финальные метрики на **test**:
  - Accuracy: 0.9355
  - F1 macro: 0.9342

## 5. Анализ ошибок
- Матрица ошибок сохранена в `artifacts/confusion_matrix.png`
- Чаще всего путаются классы *fear* и *surprise*, а также *love* и *joy*
- Пример ошибки: текст *"i am scared of the dark"* → истинный `fear`, модель предсказала `surprise`
- Всего ошибок: 129 из 2000 (6.45%)

## 6. Артефакты
- `sample_predictions.csv` – 100 примеров с текстом, истинной меткой, предсказанием и уверенностью
- `confusion_matrix.png` – изображение матрицы ошибок

## 7. Вывод
Пайплайн токенизации, инференса и fine-tuning успешно реализован. BERT-base после дообучения показывает высокое качество (93.5% accuracy) на задаче классификации эмоций.