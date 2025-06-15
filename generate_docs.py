#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Генератор деталювальних відомостей та карт розкрою
Parts List and Cutting Diagram Generator
"""

import csv
from kitchen_calculator import KitchenDesign

def generate_cutting_diagrams():
    """Генерація карт розкрою для виробництва"""
    
    kitchen = KitchenDesign()
    
    # Розрахунок всіх компонентів
    lower_components = kitchen.calculate_lower_cabinets()
    upper_components = kitchen.calculate_upper_cabinets()
    countertop = kitchen.calculate_countertop()
    
    all_components = lower_components + upper_components + [countertop]
    
    # Групування деталей по матеріалах
    parts_by_material = {}
    for component in all_components:
        material = component.material
        if material not in parts_by_material:
            parts_by_material[material] = []
        parts_by_material[material].append(component)
    
    # Створення деталювальної відомості
    with open('/home/runner/work/furniture-price-calculation-demo/furniture-price-calculation-demo/cutting_list.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Поз.', 'Назва деталі', 'Матеріал', 'Розміри (Д×Ш×Т)', 'К-ть', 'Кромка', 'Примітки'])
        
        position = 1
        for material, components in parts_by_material.items():
            # Заголовок для кожного матеріалу
            writer.writerow([f'--- {material.upper()} ---', '', '', '', '', '', ''])
            
            for component in components:
                # Визначення типу кромки
                edge_type = "2×0" if component.edge_length == 0 else "по периметру"
                if component.material == "mdf_facade":
                    edge_type = "без кромки (МДФ)"
                elif component.material == "back_panel":
                    edge_type = "без кромки (ДВП)"
                
                # Примітки
                notes = ""
                if "Фасад" in component.name:
                    notes = "Фрезерування профілю"
                elif "під петлі" in component.name or "Фасад" in component.name:
                    notes = "Свердління ø35×13"
                elif "Стільниця" in component.name:
                    notes = "Вирізи під техніку"
                
                writer.writerow([
                    position,
                    component.name_ua,
                    material,
                    f"{component.length}×{component.width}×{component.thickness}",
                    component.quantity,
                    edge_type,
                    notes
                ])
                position += 1
    
    # Створення карт розкрою для кожного матеріалу
    create_cutting_maps(parts_by_material)
    
    print("Деталювальна відомість створена: cutting_list.csv")
    print("Карти розкрою створені: cutting_maps.txt")

def create_cutting_maps(parts_by_material):
    """Створення карт розкрою"""
    
    # Стандартні розміри листів
    standard_sheets = {
        "chipboard_18": {"length": 2800, "width": 2070, "thickness": 18, "name": "ДСП 18мм"},
        "chipboard_16": {"length": 2800, "width": 2070, "thickness": 16, "name": "ДСП 16мм"},
        "mdf_facade": {"length": 2800, "width": 2070, "thickness": 19, "name": "МДФ 19мм"},
        "back_panel": {"length": 2750, "width": 1700, "thickness": 3, "name": "ДВП 3мм"}
    }
    
    with open('/home/runner/work/furniture-price-calculation-demo/furniture-price-calculation-demo/cutting_maps.txt', 'w', encoding='utf-8') as f:
        f.write("КАРТИ РОЗКРОЮ МАТЕРІАЛІВ\n")
        f.write("=" * 50 + "\n\n")
        
        for material, components in parts_by_material.items():
            if material == "countertop":
                continue  # Стільниця замовляється готова
                
            if material in standard_sheets:
                sheet = standard_sheets[material]
                f.write(f"МАТЕРІАЛ: {sheet['name']} ({sheet['length']}×{sheet['width']}×{sheet['thickness']}мм)\n")
                f.write("-" * 50 + "\n")
                
                # Оптимізація розкрою (спрощена версія)
                total_area = 0
                f.write("Деталі для розкрою:\n")
                
                for i, component in enumerate(components, 1):
                    area = (component.length * component.width * component.quantity) / 1000000  # м²
                    total_area += area
                    
                    f.write(f"{i:2d}. {component.name_ua:<40} "
                           f"{component.length:4.0f}×{component.width:4.0f}×{component.thickness:2.0f} "
                           f"({component.quantity} шт) - {area:.3f} м²\n")
                
                sheet_area = (sheet['length'] * sheet['width']) / 1000000
                sheets_needed = (total_area / sheet_area) * 1.1  # +10% на відходи
                
                f.write(f"\nЗагальна площа деталей: {total_area:.3f} м²\n")
                f.write(f"Площа листа: {sheet_area:.3f} м²\n")
                f.write(f"Потрібно листів: {sheets_needed:.1f} шт\n")
                f.write(f"Рекомендовано замовити: {int(sheets_needed) + 1} шт\n\n")
                
                # Спрощена схема розкрою
                f.write("СХЕМА РОЗКРОЮ (оптимізована):\n")
                f.write("┌" + "─" * 48 + "┐\n")
                
                current_x = 0
                current_y = 0
                sheet_num = 1
                
                for component in components:
                    if component.quantity > 0:
                        f.write(f"│ {component.name_ua[:20]:<20} {component.length:4.0f}×{component.width:4.0f} │\n")
                
                f.write("└" + "─" * 48 + "┘\n")
                f.write("Примітка: Точну схема розкрою має розробити технолог\n")
                f.write("з урахуванням структури матеріалу та мінімізації відходів.\n\n")

def create_hardware_specification():
    """Створення специфікації фурнітури"""
    
    kitchen = KitchenDesign()
    hardware = kitchen.calculate_hardware()
    
    with open('/home/runner/work/furniture-price-calculation-demo/furniture-price-calculation-demo/hardware_specification.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Поз.', 'Найменування', 'Одиниця', 'Кількість', 'Ціна за од.', 'Сума', 'Постачальник', 'Артикул'])
        
        total_cost = 0
        for i, item in enumerate(hardware, 1):
            cost = item.price_per_unit * item.quantity
            total_cost += cost
            
            # Визначення постачальника та артикула
            supplier = "За вибором"
            article = "-"
            
            if "петлі" in item.name_ua.lower():
                supplier = "GTV / Blum"
                article = "04.4200 / 71B3550"
            elif "направляючі" in item.name_ua.lower():
                supplier = "GTV / Blum"
                article = "Life / Tandem"
            elif "ручки" in item.name_ua.lower():
                supplier = "Firmax / Gamet"
                article = "RT128"
            elif "підсвітка" in item.name_ua.lower():
                supplier = "LED Ukraine"
                article = "KIT-5M-3000K"
            
            writer.writerow([
                i,
                item.name_ua,
                item.unit,
                item.quantity,
                f"{item.price_per_unit:.2f}",
                f"{cost:.2f}",
                supplier,
                article
            ])
        
        writer.writerow(['', 'ВСЬОГО:', '', '', '', f"{total_cost:.2f}", '', ''])
    
    print("Специфікація фурнітури створена: hardware_specification.csv")

def create_assembly_instructions():
    """Створення інструкції зі збірки"""
    
    with open('/home/runner/work/furniture-price-calculation-demo/furniture-price-calculation-demo/assembly_instructions.md', 'w', encoding='utf-8') as f:
        f.write("""# ІНСТРУКЦІЯ ЗІ ЗБІРКИ ТА ВСТАНОВЛЕННЯ
## Assembly and Installation Instructions

---

## ЗАГАЛЬНІ ВІДОМОСТІ

**Проект:** Класична кухня МДФ дуб сонома  
**Кількість модулів:** 12 шт (8 нижніх + 4 верхніх)  
**Тривалість монтажу:** 6-8 годин (бригада 2 чол.)  

---

## ІНСТРУМЕНТИ ТА ОБЛАДНАННЯ

### Необхідні інструменти:
- [ ] Шуруповерт з бітами PH2, PZ2
- [ ] Дриль з свердлами ø6, ø8 мм
- [ ] Рівень будівельний 600-1000мм
- [ ] Рулетка 3-5м
- [ ] Олівець для розмітки
- [ ] Стамеска 12-16мм
- [ ] Ножівка по дереву
- [ ] Шліфувальна шкурка P120

### Кріпильні елементи:
- [ ] Конфірмати 7×50мм - 120 шт
- [ ] Саморізи 4×30мм - 50 шт
- [ ] Дюбелі 8×50мм - 24 шт
- [ ] Кутники меблеві - 20 шт

---

## ПІДГОТОВЧІ РОБОТИ

### 1. Перевірка комплектності
- [ ] Звірка деталей з пакувальним листом
- [ ] Перевірка якості деталей
- [ ] Розкладання фурнітури по видах
- [ ] Підготовка робочого місця

### 2. Розмітка приміщення
- [ ] Перевірка розмірів стін
- [ ] Розмітка горизонталі для нижніх тумб
- [ ] Розмітка висоти верхніх шаф (1500-1600мм)
- [ ] Позначення місць кріплення до стіни

---

## ЗБІРКА НИЖНІХ ТУМБ

### Порядок збірки стандартної тумби:

#### Крок 1: Підготовка деталей
- [ ] Розкладання деталей однієї тумби
- [ ] Перевірка наявності всіх отворів
- [ ] Підготовка фурнітури

#### Крок 2: Збірка корпусу
```
1. З'єднати дно з боковинами на конфірмати
2. Встановити верхню планку
3. Закріпити задню стінку на саморізи 4×30
4. Встановити полицю на полицетримачі
5. Перевірити геометрію корпусу
```

#### Крок 3: Встановлення фурнітури
- [ ] Встановлення петель на фасади
- [ ] Регулювання петель на корпусі
- [ ] Встановлення направляючих для ящиків
- [ ] Збірка ящиків та їх установка

#### Крок 4: Навішування фасадів
- [ ] Встановлення фасадів на петлі
- [ ] Регулювання зазорів (3мм по периметру)
- [ ] Встановлення ручок
- [ ] Перевірка плавності відкривання

### Особливості окремих модулів:

#### Тумба під мойку:
- Зміцнення кріплення стільниці
- Підготовка отворів під комунікації
- Гідроізоляція дна

#### Тумба під варильну поверхню:
- Додаткове кріплення до стіни
- Термоізоляція задньої стінки
- Вентиляційні отвори

#### Кутовий елемент:
- Послідовна збірка з лівої секції
- Використання кутових з'єднувачів
- Регулювання по двох стінах

---

## ВСТАНОВЛЕННЯ НИЖНІХ ТУМБ

### Крок 1: Встановлення та регулювання
- [ ] Встановлення тумб по розмітці
- [ ] Регулювання по рівню опорами
- [ ] З'єднання тумб між собою стяжками
- [ ] Кріплення до стіни кутниками

### Крок 2: Встановлення стільниці
- [ ] Примірка стільниці на місце
- [ ] Підрізка під техніку (якщо потрібно)
- [ ] Кріплення з нижньої сторони саморізами
- [ ] Герметизація стиків силіконом

---

## ВСТАНОВЛЕННЯ ВЕРХНІХ ШАФ

### Крок 1: Розмітка
- [ ] Розмітка висоти кріплення (1500-1600мм)
- [ ] Розмітка кріпильних точок
- [ ] Свердління отворів під дюбелі

### Крок 2: Кріплення
- [ ] Встановлення монтажної планки на стіну
- [ ] Навішування шаф на планку
- [ ] Регулювання горизонталі
- [ ] Додаткове кріплення до стіни

### Крок 3: З'єднання шаф
- [ ] Стягування шаф між собою
- [ ] Регулювання фасадів
- [ ] Встановлення ручок

---

## ВСТАНОВЛЕННЯ ПІДСВІТКИ

### Підготовка:
- [ ] Перевірка наявності електроживлення
- [ ] Розмітка розташування стрічки
- [ ] Підготовка алюмінієвого профілю

### Монтаж:
- [ ] Кріплення профілю під шафами
- [ ] Укладання LED стрічки в профіль
- [ ] Підключення до блоку живлення
- [ ] Встановлення вимикача
- [ ] Тестування роботи

---

## ФІНАЛЬНІ РОБОТИ

### Регулювання:
- [ ] Остаточне регулювання всіх фасадів
- [ ] Перевірка роботи всіх механізмів
- [ ] Налаштування доводчиків

### Прибирання:
- [ ] Видалення пакувальних матеріалів
- [ ] Очищення поверхонь від пилу
- [ ] Нанесення захисних засобів

### Здача в експлуатацію:
- [ ] Демонстрація роботи всіх механізмів
- [ ] Передача гарантійних документів
- [ ] Інструктаж з експлуатації

---

## КОНТРОЛЬ ЯКОСТІ

### Перевірка геометрії:
- [ ] Паралельність фасадів
- [ ] Рівномірність зазорів
- [ ] Горизонталь стільниці

### Перевірка функціональності:
- [ ] Плавність відкривання дверцят
- [ ] Робота доводчиків
- [ ] Висування ящиків

### Перевірка кріплення:
- [ ] Надійність кріплення до стіни
- [ ] Стійкість конструкції
- [ ] Відсутність люфтів

---

## ГАРАНТІЙНЕ ОБСЛУГОВУВАННЯ

### Перші 6 місяців:
- Безкоштовне регулювання фурнітури
- Усунення дефектів збірки
- Додаткове налаштування

### Рекомендації з експлуатації:
- Уникати перевантаження полиць
- Регулярне очищення доводчиків
- Періодичне регулювання петель

---

**Увага:** При виявленні складнощів у процесі збірки зверніться до технічної підтримки виробника. Самостійні зміни конструкції можуть призвести до втрати гарантії.
""")
    
    print("Інструкція зі збірки створена: assembly_instructions.md")

if __name__ == "__main__":
    print("Генерація технічної документації...")
    print("=" * 50)
    
    generate_cutting_diagrams()
    create_hardware_specification()  
    create_assembly_instructions()
    
    print("\nВся технічна документація створена успішно!")
    print("Файли:")
    print("- cutting_list.csv - деталювальна відомість")
    print("- cutting_maps.txt - карти розкрою")  
    print("- hardware_specification.csv - специфікація фурнітури")
    print("- assembly_instructions.md - інструкція зі збірки")