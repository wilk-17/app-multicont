"""
Script para probar los endpoints de analytics
Requiere que el servidor Flask esté corriendo (python run.py)

Ejecutar: python test_analytics_endpoints.py
"""
import requests
import json
from datetime import date

BASE_URL = "http://127.0.0.1:5000/api"


def print_header(title):
    print("\n" + "=" * 70)
    print(f" {title}")
    print("=" * 70)


def print_json(data):
    """Imprime JSON formateado"""
    print(json.dumps(data, indent=2, ensure_ascii=False))


def test_invoicing_by_employee():
    """Probar facturación por empleado"""
    print_header("💰 TEST: Facturación por Empleado")
    
    url = f"{BASE_URL}/analytics/invoicing/by_employee"
    params = {
        'start_date': '2025-04-01',
        'end_date': '2025-09-30'
    }
    
    try:
        response = requests.get(url, params=params)
        print(f"  Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                employees = data.get('data', [])
                print(f"\n  Empleados con ventas: {len(employees)}")
                print(f"\n  {'EMPLEADO':<30} {'FACTURAS':<12} {'TOTAL':>15}")
                print("  " + "-" * 60)
                for emp in employees[:5]:  # Top 5
                    print(f"  {emp['employee_name']:<30} {emp['invoice_count']:<12} ${emp['total_sales']:>14,.2f}")
            else:
                print(f"  ❌ Error: {data.get('error')}")
        else:
            print(f"  ❌ HTTP Error: {response.text}")
    except Exception as e:
        print(f"  ❌ Exception: {e}")


def test_invoicing_by_branch():
    """Probar facturación por sucursal"""
    print_header("🏢 TEST: Facturación por Sucursal")
    
    url = f"{BASE_URL}/analytics/invoicing/by_branch"
    params = {
        'start_date': '2025-04-01',
        'end_date': '2025-09-30'
    }
    
    try:
        response = requests.get(url, params=params)
        print(f"  Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                branches = data.get('data', [])
                print(f"\n  Sucursales con ventas: {len(branches)}")
                print(f"\n  {'SUCURSAL':<20} {'CIUDAD':<20} {'TOTAL':>15}")
                print("  " + "-" * 60)
                for branch in branches:
                    print(f"  Suc-{branch['branch_id']:<15} {branch.get('city', 'N/A'):<20} ${branch['total_sales']:>14,.2f}")
            else:
                print(f"  ❌ Error: {data.get('error')}")
        else:
            print(f"  ❌ HTTP Error: {response.text}")
    except Exception as e:
        print(f"  ❌ Exception: {e}")


def test_sales_summary():
    """Probar resumen de ventas"""
    print_header("📊 TEST: Resumen de Ventas")
    
    url = f"{BASE_URL}/analytics/sales/summary"
    params = {
        'start_date': '2025-04-01',
        'end_date': '2025-09-30'
    }
    
    try:
        response = requests.get(url, params=params)
        print(f"  Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                summary = data.get('data', {})
                print(f"\n  📈 Total Facturación: ${summary.get('total_invoiced', 0):,.2f}")
                print(f"  📝 Total Cotizaciones: ${summary.get('total_quoted', 0):,.2f}")
                print(f"  🧾 Facturas: {summary.get('invoice_count', 0)}")
                print(f"  💼 Cotizaciones: {summary.get('quote_count', 0)}")
                print(f"  💵 Ticket Promedio: ${summary.get('avg_invoice', 0):,.2f}")
                print(f"  🎯 Tasa Conversión: {summary.get('conversion_rate', 0):.1f}%")
            else:
                print(f"  ❌ Error: {data.get('error')}")
        else:
            print(f"  ❌ HTTP Error: {response.text}")
    except Exception as e:
        print(f"  ❌ Exception: {e}")


def test_goals_vs_actual():
    """Probar comparación de metas vs real"""
    print_header("🎯 TEST: Metas vs Actual")
    
    url = f"{BASE_URL}/analytics/goals/vs_actual"
    params = {
        'period_type': 'monthly',
        'start_date': '2025-10-01',
        'end_date': '2025-10-31'
    }
    
    try:
        response = requests.get(url, params=params)
        print(f"  Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                goals = data.get('data', [])
                print(f"\n  Metas encontradas: {len(goals)}")
                print(f"\n  {'OBJETIVO':<20} {'META':>15} {'ACTUAL':>15} {'%':>8} {'STATUS':<12}")
                print("  " + "-" * 75)
                for goal in goals:
                    entity = f"Emp-{goal.get('employee_id', 'N/A')}" if goal.get('employee_id') else f"Suc-{goal.get('branch_id', 'N/A')}"
                    achievement = goal.get('achievement_percentage', 0)
                    status_icon = {
                        'exceeded': '🎉',
                        'on_track': '✅',
                        'at_risk': '⚠️',
                        'failed': '❌'
                    }.get(goal.get('status'), '❓')
                    print(f"  {entity:<20} ${goal.get('target_amount', 0):>14,.0f} ${goal.get('actual_sales', 0):>14,.0f} {achievement:>7.1f}% {status_icon} {goal.get('status', 'N/A'):<10}")
            else:
                print(f"  ❌ Error: {data.get('error')}")
        else:
            print(f"  ❌ HTTP Error: {response.text}")
    except Exception as e:
        print(f"  ❌ Exception: {e}")


def test_top_performers():
    """Probar top performers"""
    print_header("🏆 TEST: Top Performers")
    
    url = f"{BASE_URL}/analytics/top_performers"
    params = {
        'start_date': '2025-04-01',
        'end_date': '2025-09-30',
        'limit': 5
    }
    
    try:
        response = requests.get(url, params=params)
        print(f"  Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                performers = data.get('data', [])
                print(f"\n  {'POS':<5} {'EMPLEADO':<30} {'VENTAS':>15}")
                print("  " + "-" * 55)
                for i, perf in enumerate(performers, 1):
                    medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else "  "
                    print(f"  {medal}{i:<3} {perf['employee_name']:<30} ${perf['total_sales']:>14,.2f}")
            else:
                print(f"  ❌ Error: {data.get('error')}")
        else:
            print(f"  ❌ HTTP Error: {response.text}")
    except Exception as e:
        print(f"  ❌ Exception: {e}")


def test_brands():
    """Probar listado de marcas"""
    print_header("🏷️  TEST: Listado de Marcas")
    
    url = f"{BASE_URL}/brands/"
    
    try:
        response = requests.get(url)
        print(f"  Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                brands_data = data.get('data', {})
                brands = brands_data.get('items', [])
                print(f"\n  Total marcas: {brands_data.get('total', 0)}")
                print(f"\n  {'ID':<5} {'MARCA':<30}")
                print("  " + "-" * 40)
                for brand in brands:
                    print(f"  {brand['id']:<5} {brand['name']:<30}")
            else:
                print(f"  ❌ Error: {data.get('error')}")
        else:
            print(f"  ❌ HTTP Error: {response.text}")
    except Exception as e:
        print(f"  ❌ Exception: {e}")


def test_sales_goals():
    """Probar listado de metas"""
    print_header("🎯 TEST: Listado de Metas de Venta")
    
    url = f"{BASE_URL}/sales_goals/"
    
    try:
        response = requests.get(url)
        print(f"  Status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                goals_data = data.get('data', {})
                goals = goals_data.get('items', [])
                print(f"\n  Total metas: {goals_data.get('total', 0)}")
                print(f"\n  {'ID':<5} {'TIPO':<12} {'OBJETIVO':<15} {'MONTO':>15}")
                print("  " + "-" * 50)
                for goal in goals:
                    entity = f"Emp-{goal.get('employee_id')}" if goal.get('employee_id') else f"Suc-{goal.get('branch_id')}"
                    print(f"  {goal['id']:<5} {goal['period_type']:<12} {entity:<15} ${float(goal['target_amount']):>14,.0f}")
            else:
                print(f"  ❌ Error: {data.get('error')}")
        else:
            print(f"  ❌ HTTP Error: {response.text}")
    except Exception as e:
        print(f"  ❌ Exception: {e}")


def main():
    """Función principal"""
    print("\n" + "=" * 70)
    print(" PRUEBA DE ENDPOINTS DE ANALYTICS - MULTICONT")
    print("=" * 70)
    print("\n⚠️  IMPORTANTE: El servidor debe estar corriendo en http://127.0.0.1:5000")
    print("   Ejecuta: python run.py (en otra terminal)\n")
    
    input("Presiona ENTER para continuar...")
    
    try:
        # Probar endpoints CRUD básicos primero
        test_brands()
        test_sales_goals()
        
        # Probar endpoints de analytics
        test_invoicing_by_employee()
        test_invoicing_by_branch()
        test_sales_summary()
        test_top_performers()
        test_goals_vs_actual()
        
        print("\n" + "=" * 70)
        print(" ✅ PRUEBAS COMPLETADAS")
        print("=" * 70)
        print("\n📝 Notas:")
        print("   - Si algún endpoint falló, verifica que el servidor esté corriendo")
        print("   - Revisa los logs del servidor para más detalles")
        print("   - Puedes probar manualmente en: http://127.0.0.1:5000/api/docs/\n")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Pruebas interrumpidas por el usuario")
    except Exception as e:
        print(f"\n❌ Error general: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
