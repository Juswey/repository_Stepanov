# Отчёт по HW10-11

## Часть A: Классификация

### Дано
- Датасет: STL10 (10 классов, 96x96)
- Разделение: train 80% / val 20% / test официальный
- Семя: 42

### Эксперименты
Проведены 4 эксперимента:
- **C1 (simple-cnn-base)**: простая CNN без аугментаций
- **C2 (simple-cnn-aug)**: та же CNN с аугментациями
- **C3 (resnet18-head-only)**: ResNet18 предобучен, заморожен, обучается только голова
- **C4 (resnet18-finetune)**: ResNet18 предобучен, разморожен layer4 и голова

### Результаты

| Эксперимент | Лучшая val accuracy | Test accuracy |
|-------------|---------------------|---------------|
| C1          | 0.654               | 0.637         |
| C2          | 0.671               | 0.654         |
| C3          | 0.812               | 0.803         |
| C4          | 0.873               | 0.865         |

*Таблица полных результатов см. в [artifacts/runs.csv](./artifacts/runs.csv).*

### Анализ
- Аугментации (C2) дали прирост ~1.7% по сравнению с базовой CNN.
- Transfer learning (C3) значительно улучшил качество (с 67% до 81%).
- Дополнительное дообучение layer4 (C4) дало ещё +6% к val accuracy.

График сравнения: [classification_compare.png](./artifacts/figures/classification_compare.png)  
Графики обучения лучшей модели (C4): [classification_curves_best.png](./artifacts/figures/classification_curves_best.png)  
Примеры аугментаций: [augmentations_preview.png](./artifacts/figures/augmentations_preview.png)

### Выводы
Лучшая модель — C4 (ResNet18 fine-tune) с test accuracy 86.5%. Сохранена в `best_classifier.pt`.

---

## Часть B: Детекция (Pascal VOC)

### Дано
- Датасет: Pascal VOC 2012, валидационная выборка (первые 100 изображений)
- Модель: Faster R-CNN с ResNet50+FPN, предобученная на COCO, адаптированная под 20 классов VOC.

### Режимы инференса
- **V1**: порог уверенности 0.3
- **V2**: порог уверенности 0.7

### Результаты

| Режим | Precision | Recall | mIoU (по сопоставленным) |
|-------|-----------|--------|--------------------------|
| V1    | 0.43      | 0.67   | 0.61                     |
| V2    | 0.67      | 0.41   | 0.68                     |

*Полная таблица: [artifacts/runs.csv](./artifacts/runs.csv).*

### Анализ
- При низком пороге (0.3) модель выдаёт много предсказаний → recall высокий (0.67), но precision низкий (0.43).
- При высоком пороге (0.7) остаются только уверенные предсказания → precision высокий (0.67), но recall падает (0.41).
- mIoU выше при высоком пороге, так как остаются только хорошо совпадающие боксы.

### Визуализация
Примеры детекции для обоих порогов:  
- [detection_examples_thresh0.3.png](./artifacts/figures/detection_examples_thresh0.3.png)  
- [detection_examples_thresh0.7.png](./artifacts/figures/detection_examples_thresh0.7.png)

График сравнения метрик: [detection_metrics.png](./artifacts/figures/detection_metrics.png)

### Выводы
Модель работает ожидаемо. Выбор порога зависит от задачи: если важнее найти все объекты (высокий recall) — используем низкий порог; если важна точность (высокий precision) — высокий порог.

---

## Заключение
Все эксперименты выполнены, результаты зафиксированы. Структура папок и файлов соответствует требованиям.