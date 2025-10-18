"""
Vista previa de Metas vs Actual (Sin servidor)
Simula el resultado del endpoint /api/analytics/goals/vs_actual

Ejecutar: python preview_goals_vs_actual.py
"""
from datetime import date
from app import create_app, db
from app.entities.sales_goal import SalesGoal
from app.entities.invoice import Invoice
from app.entities.employee import Employee
from app.entities.branch import Branch
from app.entities.person import Person
from sqlalchemy import func, and_


def print_header(title):
    print("\n" + "=" * 70)
    print(f" {title}")
    print("=" * 70)


def calculate_achievement(target, actual):
    """Calcular porcentaje de cumplimiento"""
    if target == 0:
        return 0
    return (actual / target) * 100


def determine_status(achievement_pct):
    """Determinar status basado en porcentaje"""
    if achievement_pct >= 100:
        return 'exceeded', '🎉'
    elif achievement_pct >= 80:
        return 'on_track', '✅'
    elif achievement_pct >= 50:
        return 'at_risk', '⚠️'
    else:
        return 'failed', '❌'


def preview_monthly_goals():
    """Vista previa de metas mensuales vs ventas reales"""
    print_header("📊 METAS MENSUALES vs VENTAS REALES")
    
    # Obtener todas las metas mensuales
    goals = db.session.query(SalesGoal).filter_by(period_type='monthly').order_by(
        SalesGoal.start_date
    ).all()
    
    print(f"\n  Total metas mensuales: {len(goals)}\n")
    print(f"  {'PERÍODO':<12} {'EMPLEADO':<20} {'META':>13} {'VENTAS':>13} {'%':>7} {'STATUS':<15}")
    print("  " + "-" * 85)
    
    for goal in goals:
        # Calcular ventas reales del empleado en el período
        actual_sales = db.session.query(
            func.coalesce(func.sum(Invoice.total), 0)
        ).filter(
            Invoice.employee_id == goal.employee_id,
            Invoice.date >= goal.start_date,
            Invoice.date <= goal.end_date
        ).scalar()
        
        # Obtener nombre del empleado
        employee_name = db.session.query(
            Person.first_name, Person.last_name
        ).join(
            Employee, Employee.person_id == Person.id
        ).filter(
            Employee.id == goal.employee_id
        ).first()
        
        name = f"{employee_name[0]} {employee_name[1]}" if employee_name else f"Emp-{goal.employee_id}"
        period = goal.start_date.strftime('%b %Y')
        
        # Calcular porcentaje y status
        achievement = calculate_achievement(float(goal.target_amount), float(actual_sales))
        status_text, status_icon = determine_status(achievement)
        
        print(f"  {period:<12} {name:<20} ${float(goal.target_amount):>12,.0f} ${float(actual_sales):>12,.0f} {achievement:>6.1f}% {status_icon} {status_text:<12}")


def preview_quarterly_goals():
    """Vista previa de metas trimestrales vs ventas reales"""
    print_header("📊 METAS TRIMESTRALES vs VENTAS REALES")
    
    # Obtener todas las metas trimestrales
    goals = db.session.query(SalesGoal).filter_by(period_type='quarterly').order_by(
        SalesGoal.start_date
    ).all()
    
    print(f"\n  Total metas trimestrales: {len(goals)}\n")
    print(f"  {'PERÍODO':<12} {'SUCURSAL':<20} {'META':>13} {'VENTAS':>13} {'%':>7} {'STATUS':<15}")
    print("  " + "-" * 85)
    
    for goal in goals:
        # Calcular ventas reales de la sucursal en el período
        # (sumando todas las facturas de empleados de esa sucursal)
        actual_sales = db.session.query(
            func.coalesce(func.sum(Invoice.total), 0)
        ).join(
            Employee, Invoice.employee_id == Employee.id
        ).filter(
            Employee.branch_id == goal.branch_id,
            Invoice.date >= goal.start_date,
            Invoice.date <= goal.end_date
        ).scalar()
        
        # Obtener info de sucursal
        branch = db.session.query(Branch).filter_by(id=goal.branch_id).first()
        branch_name = f"Sucursal {branch.id}" if branch else f"Branch-{goal.branch_id}"
        
        quarter = "Q2" if goal.start_date.month == 4 else "Q3" if goal.start_date.month == 7 else "Q?"
        period = f"{quarter} 2025"
        
        # Calcular porcentaje y status
        achievement = calculate_achievement(float(goal.target_amount), float(actual_sales))
        status_text, status_icon = determine_status(achievement)
        
        print(f"  {period:<12} {branch_name:<20} ${float(goal.target_amount):>12,.0f} ${float(actual_sales):>12,.0f} {achievement:>6.1f}% {status_icon} {status_text:<12}")


def summary_statistics():
    """Estadísticas de resumen"""
    print_header("📈 ESTADÍSTICAS DE CUMPLIMIENTO")
    
    # Metas mensuales
    monthly_goals = db.session.query(SalesGoal).filter_by(period_type='monthly').all()
    
    monthly_exceeded = 0
    monthly_on_track = 0
    monthly_at_risk = 0
    monthly_failed = 0
    
    for goal in monthly_goals:
        actual_sales = db.session.query(
            func.coalesce(func.sum(Invoice.total), 0)
        ).filter(
            Invoice.employee_id == goal.employee_id,
            Invoice.date >= goal.start_date,
            Invoice.date <= goal.end_date
        ).scalar()
        
        achievement = calculate_achievement(float(goal.target_amount), float(actual_sales))
        status, _ = determine_status(achievement)
        
        if status == 'exceeded':
            monthly_exceeded += 1
        elif status == 'on_track':
            monthly_on_track += 1
        elif status == 'at_risk':
            monthly_at_risk += 1
        else:
            monthly_failed += 1
    
    # Metas trimestrales
    quarterly_goals = db.session.query(SalesGoal).filter_by(period_type='quarterly').all()
    
    quarterly_exceeded = 0
    quarterly_on_track = 0
    quarterly_at_risk = 0
    quarterly_failed = 0
    
    for goal in quarterly_goals:
        actual_sales = db.session.query(
            func.coalesce(func.sum(Invoice.total), 0)
        ).join(
            Employee, Invoice.employee_id == Employee.id
        ).filter(
            Employee.branch_id == goal.branch_id,
            Invoice.date >= goal.start_date,
            Invoice.date <= goal.end_date
        ).scalar()
        
        achievement = calculate_achievement(float(goal.target_amount), float(actual_sales))
        status, _ = determine_status(achievement)
        
        if status == 'exceeded':
            quarterly_exceeded += 1
        elif status == 'on_track':
            quarterly_on_track += 1
        elif status == 'at_risk':
            quarterly_at_risk += 1
        else:
            quarterly_failed += 1
    
    # Imprimir resumen
    print("\n  METAS MENSUALES:")
    print(f"    🎉 Superadas (≥100%):  {monthly_exceeded}/{len(monthly_goals)}")
    print(f"    ✅ En camino (80-99%):  {monthly_on_track}/{len(monthly_goals)}")
    print(f"    ⚠️  En riesgo (50-79%):  {monthly_at_risk}/{len(monthly_goals)}")
    print(f"    ❌ Fallidas (<50%):     {monthly_failed}/{len(monthly_goals)}")
    
    print("\n  METAS TRIMESTRALES:")
    print(f"    🎉 Superadas (≥100%):  {quarterly_exceeded}/{len(quarterly_goals)}")
    print(f"    ✅ En camino (80-99%):  {quarterly_on_track}/{len(quarterly_goals)}")
    print(f"    ⚠️  En riesgo (50-79%):  {quarterly_at_risk}/{len(quarterly_goals)}")
    print(f"    ❌ Fallidas (<50%):     {quarterly_failed}/{len(quarterly_goals)}")


def main():
    """Función principal"""
    print("\n" + "=" * 70)
    print(" VISTA PREVIA: METAS vs ACTUAL - MULTICONT")
    print(" Simulación del endpoint /api/analytics/goals/vs_actual")
    print("=" * 70)
    
    app = create_app()
    
    with app.app_context():
        try:
            preview_monthly_goals()
            preview_quarterly_goals()
            summary_statistics()
            
            print("\n" + "=" * 70)
            print(" ✅ VISTA PREVIA COMPLETADA")
            print("=" * 70)
            print("\n🚀 Para ver esto en Swagger UI:")
            print("   1. Inicia el servidor: python run.py")
            print("   2. Abre: http://127.0.0.1:5000/api/docs/")
            print("   3. Prueba: GET /api/analytics/goals/vs_actual")
            print("\n📊 Parámetros sugeridos:")
            print("   - period_type: monthly")
            print("   - start_date: 2025-04-01")
            print("   - end_date: 2025-09-30\n")
            
        except Exception as e:
            print(f"\n❌ ERROR: {e}")
            import traceback
            traceback.print_exc()


if __name__ == "__main__":
    main()
