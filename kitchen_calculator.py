#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kitchen Furniture Price Calculation Demo
Система розрахунку вартості кухонних меблів

Ukrainian Kitchen Project - Classic Style, MDF Oak Sonoma
"""

import json
import csv
from dataclasses import dataclass
from typing import Dict, List, Tuple
from datetime import datetime

@dataclass
class Material:
    name: str
    name_ua: str
    unit: str
    price_per_unit: float
    description: str = ""

@dataclass
class Component:
    name: str
    name_ua: str
    material: str
    length: float
    width: float
    thickness: float
    quantity: int
    edge_length: float = 0.0  # Довжина кромки в мм

@dataclass
class Hardware:
    name: str
    name_ua: str
    unit: str
    price_per_unit: float
    quantity: int
    description: str = ""

class KitchenCalculator:
    def __init__(self):
        self.materials = {}
        self.components = []
        self.hardware = []
        self.work_costs = {}
        self.initialize_materials()
        self.initialize_work_costs()
    
    def initialize_materials(self):
        """Ініціалізація матеріалів та їх цін"""
        self.materials = {
            "mdf_facade": Material(
                name="MDF Facade Oak Sonoma",
                name_ua="МДФ фасад дуб сонома",
                unit="м²",
                price_per_unit=850.0,
                description="МДФ 19мм з фрезеруванням, дуб сонома"
            ),
            "chipboard_18": Material(
                name="Chipboard 18mm Oak Sonoma",
                name_ua="ДСП 18мм дуб сонома",
                unit="м²",
                price_per_unit=320.0,
                description="ДСП ламіноване 18мм, дуб сонома"
            ),
            "chipboard_16": Material(
                name="Chipboard 16mm Oak Sonoma",
                name_ua="ДСП 16мм дуб сонома",
                unit="м²",
                price_per_unit=290.0,
                description="ДСП ламіноване 16мм, дуб сонома"
            ),
            "countertop": Material(
                name="Countertop Oak Sonoma",
                name_ua="Стільниця дуб сонома",
                unit="пог.м",
                price_per_unit=750.0,
                description="Стільниця 38мм, дуб сонома"
            ),
            "edge_pvc": Material(
                name="PVC Edge 2mm",
                name_ua="Кромка ПВХ 2мм",
                unit="пог.м",
                price_per_unit=12.0,
                description="Кромка ПВХ 2мм, дуб сонома"
            ),
            "back_panel": Material(
                name="Back Panel DVP",
                name_ua="Задня стінка ДВП",
                unit="м²",
                price_per_unit=80.0,
                description="ДВП 3мм"
            )
        }
    
    def initialize_work_costs(self):
        """Ініціалізація вартості робіт"""
        self.work_costs = {
            "production": {
                "name": "Production",
                "name_ua": "Виробництво",
                "rate": 300.0,  # грн за м² фасадів
                "description": "Розпил, свердління, кромкування, складання"
            },
            "assembly": {
                "name": "Assembly",
                "name_ua": "Збірка та встановлення",
                "rate": 2500.0,  # грн за кухню
                "description": "Збірка та встановлення кухні"
            },
            "delivery": {
                "name": "Delivery",
                "name_ua": "Доставка",
                "rate": 800.0,  # грн за доставку
                "description": "Доставка в межах міста"
            }
        }

class KitchenDesign:
    """Клас для розрахунку конкретної кухні згідно ТЗ"""
    
    def __init__(self):
        self.calculator = KitchenCalculator()
        # Розміри кухні згідно ТЗ
        self.left_wall = 3000  # мм
        self.right_wall = 4300  # мм
        self.upper_cabinet_height = 800  # мм
        self.upper_cabinet_depth = 400  # мм
        self.lower_cabinet_depth = 600  # мм
        self.lower_cabinet_height = 850  # мм (з стільницею)
        self.lower_cabinet_body_height = 720  # мм (без стільниці)
        
        # Товщини матеріалів
        self.facade_thickness = 19  # мм
        self.body_thickness = 18  # мм
        self.shelf_thickness = 16  # мм
        self.back_thickness = 3  # мм
        
    def calculate_lower_cabinets(self):
        """Розрахунок нижніх шаф"""
        components = []
        
        # Ліва стіна - 3000мм
        # Секція під мийку - 800мм
        sink_width = 800
        components.extend(self._create_lower_cabinet("Тумба під мийку", sink_width))
        
        # Секція під плиту - 600мм
        cooktop_width = 600
        components.extend(self._create_lower_cabinet("Тумба під варильну поверхню", cooktop_width))
        
        # Секція звичайна - 600мм
        regular1_width = 600
        components.extend(self._create_lower_cabinet("Тумба звичайна 1", regular1_width))
        
        # Кутовий елемент (умовно 1000мм по діагоналі)
        corner_width = 1000
        components.extend(self._create_corner_cabinet("Кутовий елемент"))
        
        # Права стіна - 4300мм
        # Секція під посудомийку - 600мм
        dishwasher_width = 600
        components.extend(self._create_lower_cabinet("Тумба під посудомийку", dishwasher_width))
        
        # Секція під холодильник - 600мм
        fridge_width = 600
        components.extend(self._create_lower_cabinet("Тумба під холодильник", fridge_width))
        
        # Звичайні секції - решта простору
        remaining_width = self.right_wall - dishwasher_width - fridge_width
        regular_sections = remaining_width // 600
        for i in range(int(regular_sections)):
            components.extend(self._create_lower_cabinet(f"Тумба звичайна {i+2}", 600))
        
        return components
    
    def _create_lower_cabinet(self, name: str, width: int):
        """Створення компонентів нижньої тумби"""
        components = []
        
        # Фасад
        components.append(Component(
            name=f"{name} - Фасад",
            name_ua=f"{name} - Фасад",
            material="mdf_facade",
            length=width,
            width=self.lower_cabinet_body_height,
            thickness=self.facade_thickness,
            quantity=1,
            edge_length=(width + self.lower_cabinet_body_height) * 2
        ))
        
        # Бокові стінки
        components.append(Component(
            name=f"{name} - Бокові стінки",
            name_ua=f"{name} - Бокові стінки",
            material="chipboard_18",
            length=self.lower_cabinet_depth - self.back_thickness,
            width=self.lower_cabinet_body_height,
            thickness=self.body_thickness,
            quantity=2,
            edge_length=(self.lower_cabinet_depth + self.lower_cabinet_body_height) * 4
        ))
        
        # Верх і низ
        components.append(Component(
            name=f"{name} - Верх/низ",
            name_ua=f"{name} - Верх/низ",
            material="chipboard_18",
            length=width - self.body_thickness * 2,
            width=self.lower_cabinet_depth - self.back_thickness,
            thickness=self.body_thickness,
            quantity=2,
            edge_length=(width + self.lower_cabinet_depth) * 4
        ))
        
        # Полиця
        components.append(Component(
            name=f"{name} - Полиця",
            name_ua=f"{name} - Полиця",
            material="chipboard_16",
            length=width - self.body_thickness * 2,
            width=self.lower_cabinet_depth - self.back_thickness,
            thickness=self.shelf_thickness,
            quantity=1,
            edge_length=(width + self.lower_cabinet_depth) * 2
        ))
        
        # Задня стінка
        components.append(Component(
            name=f"{name} - Задня стінка",
            name_ua=f"{name} - Задня стінка",
            material="back_panel",
            length=width,
            width=self.lower_cabinet_body_height,
            thickness=self.back_thickness,
            quantity=1
        ))
        
        return components
    
    def _create_corner_cabinet(self, name: str):
        """Створення кутового елемента"""
        # Спрощена версія кутового елемента
        return self._create_lower_cabinet(name, 1000)
    
    def calculate_upper_cabinets(self):
        """Розрахунок верхніх шаф"""
        components = []
        
        # Верхні шафи на лівій стіні (2400мм - без кутового)
        left_upper_width = 2400
        sections = left_upper_width // 600
        for i in range(int(sections)):
            components.extend(self._create_upper_cabinet(f"Верхня шафа ліва {i+1}", 600))
        
        # Верхні шафи на правій стіні (3000мм)
        right_upper_width = 3000
        sections = right_upper_width // 600
        for i in range(int(sections)):
            components.extend(self._create_upper_cabinet(f"Верхня шафа права {i+1}", 600))
        
        return components
    
    def _create_upper_cabinet(self, name: str, width: int):
        """Створення компонентів верхньої шафи"""
        components = []
        
        # Фасад
        components.append(Component(
            name=f"{name} - Фасад",
            name_ua=f"{name} - Фасад",
            material="mdf_facade",
            length=width,
            width=self.upper_cabinet_height,
            thickness=self.facade_thickness,
            quantity=1,
            edge_length=(width + self.upper_cabinet_height) * 2
        ))
        
        # Бокові стінки
        components.append(Component(
            name=f"{name} - Бокові стінки",
            name_ua=f"{name} - Бокові стінки",
            material="chipboard_18",
            length=self.upper_cabinet_depth - self.back_thickness,
            width=self.upper_cabinet_height,
            thickness=self.body_thickness,
            quantity=2,
            edge_length=(self.upper_cabinet_depth + self.upper_cabinet_height) * 4
        ))
        
        # Верх і низ
        components.append(Component(
            name=f"{name} - Верх/низ",
            name_ua=f"{name} - Верх/низ",
            material="chipboard_18",
            length=width - self.body_thickness * 2,
            width=self.upper_cabinet_depth - self.back_thickness,
            thickness=self.body_thickness,
            quantity=2,
            edge_length=(width + self.upper_cabinet_depth) * 4
        ))
        
        # Полиця
        components.append(Component(
            name=f"{name} - Полиця",
            name_ua=f"{name} - Полиця",
            material="chipboard_16",
            length=width - self.body_thickness * 2,
            width=self.upper_cabinet_depth - self.back_thickness,
            thickness=self.shelf_thickness,
            quantity=1,
            edge_length=(width + self.upper_cabinet_depth) * 2
        ))
        
        # Задня стінка
        components.append(Component(
            name=f"{name} - Задня стінка",
            name_ua=f"{name} - Задня стінка",
            material="back_panel",
            length=width,
            width=self.upper_cabinet_height,
            thickness=self.back_thickness,
            quantity=1
        ))
        
        return components
    
    def calculate_countertop(self):
        """Розрахунок стільниці"""
        # Загальна довжина стільниці (ліва стіна + права стіна)
        total_length = (self.left_wall + self.right_wall) / 1000  # переводимо в метри
        
        return Component(
            name="Countertop",
            name_ua="Стільниця",
            material="countertop",
            length=total_length * 1000,
            width=600,  # стандартна глибина
            thickness=38,
            quantity=1
        )
    
    def calculate_hardware(self):
        """Розрахунок фурнітури"""
        hardware = []
        
        # Петлі для фасадів (2 петлі на фасад)
        total_doors = 13  # приблизна кількість дверцят
        hardware.append(Hardware(
            name="Soft-close hinges",
            name_ua="Петлі з доводчиками",
            unit="шт",
            price_per_unit=45.0,
            quantity=total_doors * 2,
            description="Blum Clip Top петлі з інтегрованими доводчиками"
        ))
        
        # Направляючі для ящиків
        drawers_count = 8  # кількість ящиків
        hardware.append(Hardware(
            name="Drawer slides soft-close",
            name_ua="Направляючі для ящиків з доводчиками",
            unit="комп",
            price_per_unit=85.0,
            quantity=drawers_count,
            description="Blum Tandem направляючі повного висуву"
        ))
        
        # Ручки
        handles_count = total_doors + drawers_count
        hardware.append(Hardware(
            name="Cabinet handles",
            name_ua="Ручки меблеві",
            unit="шт",
            price_per_unit=25.0,
            quantity=handles_count,
            description="Ручки класичні, під бронзу"
        ))
        
        # Підсвітка робочої зони
        hardware.append(Hardware(
            name="LED strip lighting",
            name_ua="Світлодіодна підсвітка",
            unit="компл",
            price_per_unit=1200.0,
            quantity=1,
            description="LED стрічка 5м + профіль + блок живлення"
        ))
        
        return hardware

def main():
    """Головна функція для розрахунку кухні"""
    kitchen = KitchenDesign()
    
    print("=== РОЗРАХУНОК КУХОННИХ МЕБЛІВ ===")
    print("Класичний стиль, МДФ дуб сонома")
    print("=" * 50)
    
    # Розрахунок компонентів
    print("\n1. Розрахунок нижніх тумб...")
    lower_components = kitchen.calculate_lower_cabinets()
    
    print("2. Розрахунок верхніх шаф...")
    upper_components = kitchen.calculate_upper_cabinets()
    
    print("3. Розрахунок стільниці...")
    countertop = kitchen.calculate_countertop()
    
    print("4. Розрахунок фурнітури...")
    hardware = kitchen.calculate_hardware()
    
    # Об'єднання всіх компонентів
    all_components = lower_components + upper_components + [countertop]
    
    # Розрахунок вартості матеріалів
    print("\n=== РОЗРАХУНОК ВАРТОСТІ МАТЕРІАЛІВ ===")
    material_costs = calculate_material_costs(all_components, kitchen.calculator.materials)
    
    print("\n=== РОЗРАХУНОК ФУРНІТУРИ ===")
    hardware_costs = calculate_hardware_costs(hardware)
    
    print("\n=== РОЗРАХУНОК РОБІТ ===")
    work_costs = calculate_work_costs(kitchen.calculator.work_costs, material_costs, hardware_costs)
    
    print("\n=== ЗАГАЛЬНИЙ РОЗРАХУНОК ===")
    total_materials = sum(material_costs.values())
    total_hardware = sum([h.price_per_unit * h.quantity for h in hardware])
    total_work = sum(work_costs.values())
    total_cost = total_materials + total_hardware + total_work
    
    print(f"Матеріали: {total_materials:.2f} грн")
    print(f"Фурнітура: {total_hardware:.2f} грн")
    print(f"Роботи: {total_work:.2f} грн")
    print(f"ВСЬОГО: {total_cost:.2f} грн")
    
    # Генерація звітів
    generate_reports(all_components, hardware, material_costs, hardware_costs, work_costs, kitchen.calculator.materials)

def calculate_material_costs(components: List[Component], materials: Dict[str, Material]) -> Dict[str, float]:
    """Розрахунок вартості матеріалів"""
    costs = {}
    
    for component in components:
        material = materials[component.material]
        
        if material.unit == "м²":
            area = (component.length * component.width) / 1000000  # мм² в м²
            component_cost = area * material.price_per_unit * component.quantity
        elif material.unit == "пог.м":
            length = component.length / 1000  # мм в м
            component_cost = length * material.price_per_unit * component.quantity
        else:
            component_cost = material.price_per_unit * component.quantity
        
        if component.material not in costs:
            costs[component.material] = 0
        costs[component.material] += component_cost
        
        # Додаємо вартість кромки
        if component.edge_length > 0:
            edge_cost = (component.edge_length / 1000) * materials["edge_pvc"].price_per_unit * component.quantity
            if "edge_pvc" not in costs:
                costs["edge_pvc"] = 0
            costs["edge_pvc"] += edge_cost
    
    return costs

def calculate_hardware_costs(hardware: List[Hardware]) -> Dict[str, float]:
    """Розрахунок вартості фурнітури"""
    costs = {}
    for item in hardware:
        costs[item.name] = item.price_per_unit * item.quantity
    return costs

def calculate_work_costs(work_rates: Dict, material_costs: Dict[str, float], hardware_costs: Dict[str, float]) -> Dict[str, float]:
    """Розрахунок вартості робіт"""
    costs = {}
    
    # Виробництво базується на площі фасадів
    facade_area = material_costs.get("mdf_facade", 0) / 850.0  # приблизна площа фасадів
    costs["production"] = facade_area * work_rates["production"]["rate"]
    
    costs["assembly"] = work_rates["assembly"]["rate"]
    costs["delivery"] = work_rates["delivery"]["rate"]
    
    return costs

def generate_reports(components, hardware, material_costs, hardware_costs, work_costs, materials):
    """Генерація звітів"""
    
    # Створення детального звіту
    with open('/home/runner/work/furniture-price-calculation-demo/furniture-price-calculation-demo/kitchen_calculation_report.txt', 'w', encoding='utf-8') as f:
        f.write("ТЕХНІЧНЕ ЗАВДАННЯ НА ВИРОБНИЦТВО КУХОННИХ МЕБЛІВ\n")
        f.write("=" * 60 + "\n\n")
        
        f.write("ЗАГАЛЬНІ ХАРАКТЕРИСТИКИ:\n")
        f.write("- Стиль: Класичний\n")
        f.write("- Фасади: МДФ, декор 'дуб сонома'\n")
        f.write("- Корпус: ДСП, дуб сонома\n")
        f.write("- Фурнітура: з доводчиками soft-close\n")
        f.write("- Підсвітка робочої зони: включена\n\n")
        
        f.write("ГАБАРИТИ КУХНІ:\n")
        f.write("- Ліва стіна: 3000 мм\n")
        f.write("- Права стіна: 4300 мм\n")
        f.write("- Висота верхніх шаф: 800 мм\n")
        f.write("- Глибина верхніх шаф: 400 мм\n")
        f.write("- Глибина нижніх шаф: 600 мм\n")
        f.write("- Висота нижніх шаф зі стільницею: 850 мм\n\n")
        
        f.write("РОЗРАХУНОК МАТЕРІАЛІВ:\n")
        f.write("-" * 40 + "\n")
        total_materials = 0
        for material_key, cost in material_costs.items():
            material = materials[material_key]
            f.write(f"{material.name_ua}: {cost:.2f} грн\n")
            total_materials += cost
        f.write(f"Загалом матеріали: {total_materials:.2f} грн\n\n")
        
        f.write("РОЗРАХУНОК ФУРНІТУРИ:\n")
        f.write("-" * 40 + "\n")
        total_hardware = 0
        for item in hardware:
            cost = item.price_per_unit * item.quantity
            f.write(f"{item.name_ua}: {item.quantity} {item.unit} x {item.price_per_unit:.2f} = {cost:.2f} грн\n")
            total_hardware += cost
        f.write(f"Загалом фурнітура: {total_hardware:.2f} грн\n\n")
        
        f.write("РОЗРАХУНОК РОБІТ:\n")
        f.write("-" * 40 + "\n")
        total_work = 0
        for work_name, cost in work_costs.items():
            f.write(f"{work_name}: {cost:.2f} грн\n")
            total_work += cost
        f.write(f"Загалом роботи: {total_work:.2f} грн\n\n")
        
        f.write("ЗАГАЛЬНА ВАРТІСТЬ:\n")
        f.write("=" * 40 + "\n")
        total_cost = total_materials + total_hardware + total_work
        f.write(f"Матеріали: {total_materials:.2f} грн\n")
        f.write(f"Фурнітура: {total_hardware:.2f} грн\n")
        f.write(f"Роботи: {total_work:.2f} грн\n")
        f.write(f"ВСЬОГО: {total_cost:.2f} грн\n\n")
        
        f.write(f"Дата розрахунку: {datetime.now().strftime('%d.%m.%Y %H:%M')}\n")
    
    # Створення CSV файлу з деталізацією
    with open('/home/runner/work/furniture-price-calculation-demo/furniture-price-calculation-demo/kitchen_components.csv', 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Назва', 'Матеріал', 'Довжина (мм)', 'Ширина (мм)', 'Товщина (мм)', 'Кількість'])
        
        for component in components:
            writer.writerow([
                component.name_ua,
                component.material,
                component.length,
                component.width,  
                component.thickness,
                component.quantity
            ])

if __name__ == "__main__":
    main()