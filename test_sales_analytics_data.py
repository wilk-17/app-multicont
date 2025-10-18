"""
Script de prueba para poblar datos de ejemplo del sistema de metas y análisis de ventas
Ejecutar: python test_sales_analytics_data.py
"""
import requests
from datetime import date, timedelta

BASE_URL = "http://127.0.0.1:5000/api"

def create_brands():
    """Crear marcas de ejemplo"""
    print("\n=== Creando Marcas ===")
    brands = [
        {"name": "Samsung", "description": "Electrónicos y electrodomésticos coreanos"},
        {"name": "Apple", "description": "Tecnología premium estadounidense"},
        {"name": "LG", "description": "Electrónica de consumo coreana"},
        {"name": "Sony", "description": "Electrónica japonesa de alta calidad"}
    ]
    
    created_brands = []
    for brand_data in brands:
        response = requests.post(f"{BASE_URL}/brands/", json=brand_data)
        if response.status_code == 201:
            brand = response.json()['data']
            print(f"✅ Marca creada: {brand['name']} (ID: {brand['id']})")
            created_brands.append(brand)
        else:
            print(f"❌ Error al crear marca {brand_data['name']}: {response.text}")
    
    return created_brands


def create_sales_goals(employee_ids, branch_ids):
    """Crear metas de ventas de ejemplo"""
    print("\n=== Creando Metas de Ventas ===")
    
    # Meta mensual para empleado 1 (si existe)
    if employee_ids:
        employee_id = employee_ids[0]
        goal_data = {
            "employee_id": employee_id,
            "period_type": "monthly",
            "start_date": "2025-10-01",
            "end_date": "2025-10-31",
            "target_amount": 50000.00,
            "created_by_user_id": 1
        }
        response = requests.post(f"{BASE_URL}/sales_goals/", json=goal_data)
        if response.status_code == 201:
            goal = response.json()['data']
            print(f"✅ Meta mensual creada para empleado {employee_id}: ${goal['target_amount']}")
        else:
            print(f"❌ Error al crear meta: {response.text}")
    
    # Meta trimestral para sucursal 1 (si existe)
    if branch_ids:
        branch_id = branch_ids[0]
        goal_data = {
            "branch_id": branch_id,
            "period_type": "quarterly",
            "start_date": "2025-10-01",
            "end_date": "2025-12-31",
            "target_amount": 300000.00,
            "created_by_user_id": 1
        }
        response = requests.post(f"{BASE_URL}/sales_goals/", json=goal_data)
        if response.status_code == 201:
            goal = response.json()['data']
            print(f"✅ Meta trimestral creada para sucursal {branch_id}: ${goal['target_amount']}")
        else:
            print(f"❌ Error al crear meta: {response.text}")


def get_existing_employees():
    """Obtener empleados existentes"""
    response = requests.get(f"{BASE_URL}/employees/?per_page=10")
    if response.status_code == 200:
        employees = response.json()['data']['items']
        employee_ids = [int(emp['id']) for emp in employees]
        print(f"\n✅ Encontrados {len(employee_ids)} empleados: {employee_ids}")
        return employee_ids
    return []


def get_existing_branches():
    """Obtener sucursales existentes"""
    response = requests.get(f"{BASE_URL}/branches/?per_page=10")
    if response.status_code == 200:
        branches = response.json()['data']['items']
        branch_ids = [int(branch['id']) for branch in branches]
        print(f"✅ Encontradas {len(branch_ids)} sucursales: {branch_ids}")
        return branch_ids
    return []


def test_analytics_endpoints():
    """Probar endpoints de analytics"""
    print("\n=== Probando Endpoints de Analytics ===")
    
    start_date = "2025-10-01"
    end_date = "2025-10-31"
    
    # Test 1: Resumen de ventas
    print("\n1. Resumen de ventas:")
    response = requests.get(f"{BASE_URL}/analytics/sales/summary", 
                           params={"start_date": start_date, "end_date": end_date})
    if response.status_code == 200:
        data = response.json()['data']
        print(f"   Total facturado: ${data['total_invoiced']}")
        print(f"   Facturas: {data['invoice_count']}")
        print(f"   Cotizaciones: {data['quote_count']}")
        print(f"   Empleados activos: {data['active_employees']}")
    else:
        print(f"   ❌ Error: {response.text}")
    
    # Test 2: Facturación por empleado
    print("\n2. Facturación por empleado:")
    response = requests.get(f"{BASE_URL}/analytics/invoicing/by_employee",
                           params={"start_date": start_date, "end_date": end_date})
    if response.status_code == 200:
        data = response.json()['data']
        if data:
            for item in data[:3]:  # Mostrar top 3
                print(f"   {item['employee_name']}: ${item['total_invoiced']} ({item['invoice_count']} facturas)")
        else:
            print("   (Sin datos)")
    else:
        print(f"   ❌ Error: {response.text}")
    
    # Test 3: Facturación por sucursal
    print("\n3. Facturación por sucursal:")
    response = requests.get(f"{BASE_URL}/analytics/invoicing/by_branch",
                           params={"start_date": start_date, "end_date": end_date})
    if response.status_code == 200:
        data = response.json()['data']
        if data:
            for item in data[:3]:
                print(f"   Sucursal {item['branch_id']}: ${item['total_invoiced']} ({item['employee_count']} empleados)")
        else:
            print("   (Sin datos)")
    else:
        print(f"   ❌ Error: {response.text}")
    
    # Test 4: Facturación por marca
    print("\n4. Facturación por marca:")
    response = requests.get(f"{BASE_URL}/analytics/invoicing/by_brand",
                           params={"start_date": start_date, "end_date": end_date})
    if response.status_code == 200:
        data = response.json()['data']
        if data:
            for item in data[:3]:
                print(f"   {item['brand_name']}: ${item['total_invoiced']} ({item['total_quantity']} unidades)")
        else:
            print("   (Sin datos - asignar brand_id a inventory_items)")
    else:
        print(f"   ❌ Error: {response.text}")
    
    # Test 5: Metas vs reales
    print("\n5. Metas vs facturación real (mensual):")
    response = requests.get(f"{BASE_URL}/analytics/goals/vs_actual",
                           params={"period_type": "monthly"})
    if response.status_code == 200:
        data = response.json()['data']
        if data:
            for item in data[:3]:
                print(f"   {item['scope_type']} {item['scope_name']}: "
                      f"{item['achievement_percentage']}% - Estado: {item['status']}")
                print(f"      Meta: ${item['target_amount']} | Real: ${item['actual_amount']}")
        else:
            print("   (Sin datos - crear metas con sales_goals API)")
    else:
        print(f"   ❌ Error: {response.text}")
    
    # Test 6: Top performers
    print("\n6. Top 5 vendedores:")
    response = requests.get(f"{BASE_URL}/analytics/top_performers",
                           params={"start_date": start_date, "end_date": end_date, "limit": 5})
    if response.status_code == 200:
        data = response.json()['data']
        if data:
            for item in data:
                print(f"   #{item['rank']} {item['employee_name']}: ${item['total_invoiced']} "
                      f"({item['invoice_count']} facturas, promedio: ${item['avg_invoice']:.2f})")
        else:
            print("   (Sin datos - asignar employee_id a invoices)")
    else:
        print(f"   ❌ Error: {response.text}")


def main():
    print("=" * 60)
    print("SCRIPT DE PRUEBA - SISTEMA DE METAS Y ANÁLISIS DE VENTAS")
    print("=" * 60)
    
    try:
        # 1. Crear marcas
        brands = create_brands()
        
        # 2. Obtener empleados y sucursales existentes
        employee_ids = get_existing_employees()
        branch_ids = get_existing_branches()
        
        # 3. Crear metas si hay empleados/sucursales
        if employee_ids or branch_ids:
            create_sales_goals(employee_ids, branch_ids)
        else:
            print("\n⚠️ No hay empleados ni sucursales para crear metas")
        
        # 4. Probar endpoints de analytics
        test_analytics_endpoints()
        
        print("\n" + "=" * 60)
        print("✅ SCRIPT COMPLETADO")
        print("=" * 60)
        print("\nPróximos pasos:")
        print("1. Asignar brand_id a inventory_items existentes")
        print("2. Asignar employee_id a quotes, sales_orders e invoices")
        print("3. Crear más metas de ventas para diferentes periodos")
        print("4. Generar facturas con employee_id para ver analytics completos")
        
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: No se puede conectar al servidor Flask")
        print("   Asegúrate de que el servidor esté corriendo en http://127.0.0.1:5000")
    except Exception as e:
        print(f"\n❌ ERROR INESPERADO: {e}")


if __name__ == "__main__":
    main()
