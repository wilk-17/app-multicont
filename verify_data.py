"""
Script de verificación de datos poblados
Consulta directa a la base de datos para validar el dataset

Ejecutar: python verify_data.py
"""
from app import create_app, db
from app.entities.employee import Employee
from app.entities.invoice import Invoice
from app.entities.quote import Quote
from app.entities.brand import Brand
from app.entities.sales_goal import SalesGoal
from app.entities.person import Person
from sqlalchemy import func, extract
from datetime import date


def print_header(title):
    """Imprime un encabezado formateado"""
    print("\n" + "=" * 70)
    print(f" {title}")
    print("=" * 70)


def verify_basic_data():
    """Verificar datos básicos poblados"""
    print_header("📊 DATOS BÁSICOS")
    
    # Contar registros
    counts = {
        'Empleados': db.session.query(Employee).count(),
        'Cotizaciones': db.session.query(Quote).count(),
        'Facturas': db.session.query(Invoice).count(),
        'Marcas': db.session.query(Brand).count(),
        'Metas de Venta': db.session.query(SalesGoal).count()
    }
    
    for entity, count in counts.items():
        print(f"  ✅ {entity}: {count}")


def verify_invoices_by_employee():
    """Verificar facturación por empleado"""
    print_header("💰 FACTURACIÓN POR EMPLEADO (Abril-Septiembre 2025)")
    
    results = db.session.query(
        Employee.id,
        Person.first_name,
        Person.last_name,
        func.count(Invoice.id).label('num_invoices'),
        func.sum(Invoice.total).label('total_sales')
    ).join(
        Person, Employee.person_id == Person.id
    ).join(
        Invoice, Invoice.employee_id == Employee.id
    ).filter(
        Invoice.date >= date(2025, 4, 1),
        Invoice.date <= date(2025, 9, 30)
    ).group_by(
        Employee.id, Person.first_name, Person.last_name
    ).order_by(
        func.sum(Invoice.total).desc()
    ).all()
    
    if not results:
        print("  ⚠️  No se encontraron facturas con employee_id asignado")
        return
    
    print(f"\n  {'ID':<5} {'EMPLEADO':<25} {'FACTURAS':<12} {'TOTAL VENTAS':>15}")
    print("  " + "-" * 60)
    
    for emp_id, fname, lname, num_inv, total in results:
        name = f"{fname} {lname}"
        print(f"  {emp_id:<5} {name:<25} {num_inv:<12} ${total:>14,.0f}")


def verify_invoices_by_brand():
    """Verificar facturación por marca"""
    print_header("🏷️  FACTURACIÓN POR MARCA (Abril-Septiembre 2025)")
    
    # Nota: Esto requeriría invoice_item → inventory_item → brand
    # Por simplicidad, mostraremos las marcas existentes
    brands = db.session.query(Brand).all()
    
    print(f"\n  {'ID':<5} {'MARCA':<30} {'DESCRIPCIÓN':<30}")
    print("  " + "-" * 70)
    
    for brand in brands:
        print(f"  {brand.id:<5} {brand.name:<30} {brand.description[:30]:<30}")
    
    print("\n  ℹ️  Nota: Para ver ventas por marca, necesitamos invoice_items")


def verify_sales_goals():
    """Verificar metas de ventas"""
    print_header("🎯 METAS DE VENTAS (Octubre 2025)")
    
    goals = db.session.query(SalesGoal).all()
    
    print(f"\n  {'ID':<5} {'TIPO':<12} {'EMP/SUCURSAL':<15} {'META':>15} {'PERÍODO':<15}")
    print("  " + "-" * 70)
    
    for goal in goals:
        entity = f"Emp-{goal.employee_id}" if goal.employee_id else f"Suc-{goal.branch_id}"
        meta = f"${goal.target_amount:,.0f}"
        period = f"{goal.start_date} a {goal.end_date}"[:15]
        print(f"  {goal.id:<5} {goal.period_type:<12} {entity:<15} {meta:>15} {period:<15}")


def verify_quotes_by_month():
    """Verificar cotizaciones por mes"""
    print_header("📝 COTIZACIONES POR MES")
    
    results = db.session.query(
        extract('month', Quote.date).label('month'),
        func.count(Quote.id).label('num_quotes'),
        func.sum(Quote.total).label('total_amount')
    ).filter(
        Quote.date >= date(2025, 4, 1),
        Quote.date <= date(2025, 9, 30)
    ).group_by(
        extract('month', Quote.date)
    ).order_by(
        'month'
    ).all()
    
    months = {4: 'Abril', 5: 'Mayo', 6: 'Junio', 7: 'Julio', 8: 'Agosto', 9: 'Septiembre'}
    
    print(f"\n  {'MES':<15} {'COTIZACIONES':<15} {'MONTO TOTAL':>18}")
    print("  " + "-" * 50)
    
    for month, num, total in results:
        month_name = months.get(int(month), f"Mes {month}")
        print(f"  {month_name:<15} {num:<15} ${total:>17,.0f}")


def verify_top_employees():
    """Verificar top 5 empleados por ventas"""
    print_header("🏆 TOP 5 EMPLEADOS POR VENTAS")
    
    results = db.session.query(
        Person.first_name,
        Person.last_name,
        func.count(Invoice.id).label('invoices'),
        func.sum(Invoice.total).label('total')
    ).join(
        Employee, Employee.person_id == Person.id
    ).join(
        Invoice, Invoice.employee_id == Employee.id
    ).group_by(
        Person.first_name, Person.last_name
    ).order_by(
        func.sum(Invoice.total).desc()
    ).limit(5).all()
    
    print(f"\n  {'POSICIÓN':<12} {'EMPLEADO':<25} {'FACTURAS':<12} {'TOTAL':>18}")
    print("  " + "-" * 70)
    
    for i, (fname, lname, invoices, total) in enumerate(results, 1):
        name = f"{fname} {lname}"
        medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else "  "
        print(f"  {medal} {i:<8} {name:<25} {invoices:<12} ${total:>17,.0f}")


def verify_quarterly_summary():
    """Verificar resumen trimestral"""
    print_header("📈 RESUMEN TRIMESTRAL")
    
    q2 = db.session.query(
        func.count(Invoice.id).label('invoices'),
        func.sum(Invoice.total).label('total')
    ).filter(
        Invoice.date >= date(2025, 4, 1),
        Invoice.date <= date(2025, 6, 30)
    ).first()
    
    q3 = db.session.query(
        func.count(Invoice.id).label('invoices'),
        func.sum(Invoice.total).label('total')
    ).filter(
        Invoice.date >= date(2025, 7, 1),
        Invoice.date <= date(2025, 9, 30)
    ).first()
    
    print(f"\n  {'TRIMESTRE':<15} {'FACTURAS':<15} {'TOTAL':>20}")
    print("  " + "-" * 52)
    
    print(f"  {'Q2 (Abr-Jun)':<15} {q2.invoices:<15} ${q2.total:>19,.0f}")
    print(f"  {'Q3 (Jul-Sep)':<15} {q3.invoices:<15} ${q3.total:>19,.0f}")
    
    total_invoices = q2.invoices + q3.invoices
    total_amount = q2.total + q3.total
    
    print("  " + "-" * 52)
    print(f"  {'TOTAL':<15} {total_invoices:<15} ${total_amount:>19,.0f}")
    
    # Crecimiento
    if q2.total > 0:
        growth = ((q3.total - q2.total) / q2.total) * 100
        arrow = "📈" if growth > 0 else "📉"
        print(f"\n  {arrow} Crecimiento Q2→Q3: {growth:+.1f}%")


def main():
    """Función principal"""
    print("\n" + "=" * 70)
    print(" VERIFICACIÓN DE DATOS POBLADOS - MULTICONT")
    print("=" * 70)
    
    app = create_app()
    
    with app.app_context():
        try:
            verify_basic_data()
            verify_invoices_by_employee()
            verify_invoices_by_brand()
            verify_quotes_by_month()
            verify_top_employees()
            verify_sales_goals()
            verify_quarterly_summary()
            
            print("\n" + "=" * 70)
            print(" ✅ VERIFICACIÓN COMPLETADA")
            print("=" * 70)
            print("\n🚀 Siguiente paso: Probar los endpoints de analytics")
            print("   Inicia el servidor: python run.py")
            print("   Swagger UI: http://127.0.0.1:5000/api/docs/")
            print("\n📊 Endpoints clave:")
            print("   GET /api/analytics/invoicing/by_employee")
            print("   GET /api/analytics/goals/vs_actual")
            print("   GET /api/analytics/sales/summary")
            print("   GET /api/analytics/top_performers\n")
            
        except Exception as e:
            print(f"\n❌ ERROR: {e}")
            import traceback
            traceback.print_exc()


if __name__ == "__main__":
    main()
