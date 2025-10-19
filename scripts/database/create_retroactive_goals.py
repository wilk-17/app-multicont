"""
Script para crear metas retroactivas (Abril-Septiembre 2025)
Esto permite ver el endpoint /analytics/goals/vs_actual con datos reales

Ejecutar: python create_retroactive_goals.py
"""
from datetime import date
from app import create_app, db
from app.entities.sales_goal import SalesGoal
from app.entities.employee import Employee
from app.entities.branch import Branch


def print_header(title):
    print("\n" + "=" * 70)
    print(f" {title}")
    print("=" * 70)


def create_monthly_goals_q2():
    """Crear metas mensuales para Q2 (Abril-Junio)"""
    print_header("🎯 Creando Metas Mensuales Q2 (Abril-Junio)")
    
    # Metas por mes para empleados top
    goals_data = [
        # Abril 2025
        (1, date(2025, 4, 1), date(2025, 4, 30), 12000000),  # Ana
        (4, date(2025, 4, 1), date(2025, 4, 30), 15000000),  # Diego
        (2, date(2025, 4, 1), date(2025, 4, 30), 8000000),   # Bruno
        
        # Mayo 2025
        (6, date(2025, 5, 1), date(2025, 5, 31), 10000000),  # Felipe
        (8, date(2025, 5, 1), date(2025, 5, 31), 7000000),   # Hugo
        
        # Junio 2025
        (10, date(2025, 6, 1), date(2025, 6, 30), 20000000), # Jorge
        (2, date(2025, 6, 1), date(2025, 6, 30), 9000000),   # Bruno
    ]
    
    count = 0
    for employee_id, start_date, end_date, target in goals_data:
        goal = SalesGoal(
            employee_id=employee_id,
            period_type='monthly',
            start_date=start_date,
            end_date=end_date,
            target_amount=target,
            created_by_user_id=1
        )
        db.session.add(goal)
        count += 1
        print(f"  ✅ Meta mensual Empleado {employee_id}: ${target:,.0f} ({start_date.strftime('%B %Y')})")
    
    return count


def create_monthly_goals_q3():
    """Crear metas mensuales para Q3 (Julio-Septiembre)"""
    print_header("🎯 Creando Metas Mensuales Q3 (Julio-Septiembre)")
    
    goals_data = [
        # Julio 2025
        (10, date(2025, 7, 1), date(2025, 7, 31), 18000000), # Jorge
        (8, date(2025, 7, 1), date(2025, 7, 31), 11000000),  # Hugo
        
        # Agosto 2025
        (1, date(2025, 8, 1), date(2025, 8, 31), 22000000),  # Ana
        (6, date(2025, 8, 1), date(2025, 8, 31), 10000000),  # Felipe
        
        # Septiembre 2025
        (7, date(2025, 9, 1), date(2025, 9, 30), 20000000),  # Gloria
        (5, date(2025, 9, 1), date(2025, 9, 30), 7000000),   # Elena
    ]
    
    count = 0
    for employee_id, start_date, end_date, target in goals_data:
        goal = SalesGoal(
            employee_id=employee_id,
            period_type='monthly',
            start_date=start_date,
            end_date=end_date,
            target_amount=target,
            created_by_user_id=1
        )
        db.session.add(goal)
        count += 1
        print(f"  ✅ Meta mensual Empleado {employee_id}: ${target:,.0f} ({start_date.strftime('%B %Y')})")
    
    return count


def create_quarterly_goals():
    """Crear metas trimestrales para Q2 y Q3"""
    print_header("🎯 Creando Metas Trimestrales")
    
    goals_data = [
        # Q2 2025 (Abril-Junio)
        (1, date(2025, 4, 1), date(2025, 6, 30), 60000000),  # Sucursal 1 (Bogotá)
        (2, date(2025, 4, 1), date(2025, 6, 30), 50000000),  # Sucursal 2 (Bucaramanga)
        
        # Q3 2025 (Julio-Septiembre)
        (1, date(2025, 7, 1), date(2025, 9, 30), 75000000),  # Sucursal 1 (Bogotá)
        (3, date(2025, 7, 1), date(2025, 9, 30), 55000000),  # Sucursal 3 (Medellín)
        (5, date(2025, 7, 1), date(2025, 9, 30), 45000000),  # Sucursal 5 (Barranquilla)
    ]
    
    count = 0
    for branch_id, start_date, end_date, target in goals_data:
        goal = SalesGoal(
            branch_id=branch_id,
            period_type='quarterly',
            start_date=start_date,
            end_date=end_date,
            target_amount=target,
            created_by_user_id=1
        )
        db.session.add(goal)
        count += 1
        quarter = "Q2" if start_date.month == 4 else "Q3"
        print(f"  ✅ Meta trimestral Sucursal {branch_id}: ${target:,.0f} ({quarter} 2025)")
    
    return count


def verify_created_goals():
    """Verificar metas creadas"""
    print_header("📊 Verificación de Metas Creadas")
    
    # Contar por tipo de período
    monthly_count = db.session.query(SalesGoal).filter_by(period_type='monthly').count()
    quarterly_count = db.session.query(SalesGoal).filter_by(period_type='quarterly').count()
    
    print(f"\n  ✅ Metas mensuales: {monthly_count}")
    print(f"  ✅ Metas trimestrales: {quarterly_count}")
    print(f"  ✅ Total metas: {monthly_count + quarterly_count}")
    
    # Contar por período
    q2_count = db.session.query(SalesGoal).filter(
        SalesGoal.start_date >= date(2025, 4, 1),
        SalesGoal.start_date < date(2025, 7, 1)
    ).count()
    
    q3_count = db.session.query(SalesGoal).filter(
        SalesGoal.start_date >= date(2025, 7, 1),
        SalesGoal.start_date < date(2025, 10, 1)
    ).count()
    
    print(f"\n  📅 Metas Q2 (Abril-Junio): {q2_count}")
    print(f"  📅 Metas Q3 (Julio-Septiembre): {q3_count}")


def main():
    """Función principal"""
    print("\n" + "=" * 70)
    print(" CREACIÓN DE METAS RETROACTIVAS - MULTICONT")
    print(" Periodo: Abril-Septiembre 2025")
    print("=" * 70)
    
    app = create_app()
    
    with app.app_context():
        try:
            # Eliminar metas futuras (octubre 2025) para evitar confusión
            print_header("🗑️  Limpiando Metas Futuras")
            future_goals = db.session.query(SalesGoal).filter(
                SalesGoal.start_date >= date(2025, 10, 1)
            ).delete()
            db.session.commit()
            print(f"  ✅ {future_goals} metas futuras eliminadas")
            
            # Crear metas retroactivas
            q2_monthly = create_monthly_goals_q2()
            q3_monthly = create_monthly_goals_q3()
            quarterly = create_quarterly_goals()
            
            # Guardar cambios
            db.session.commit()
            
            # Verificar
            verify_created_goals()
            
            print("\n" + "=" * 70)
            print(" ✅ METAS RETROACTIVAS CREADAS EXITOSAMENTE")
            print("=" * 70)
            print(f"\n  Total metas creadas: {q2_monthly + q3_monthly + quarterly}")
            print(f"  - Mensuales Q2: {q2_monthly}")
            print(f"  - Mensuales Q3: {q3_monthly}")
            print(f"  - Trimestrales: {quarterly}")
            
            print("\n🎯 Ahora puedes probar el endpoint:")
            print("   GET /api/analytics/goals/vs_actual?period_type=monthly&start_date=2025-04-01&end_date=2025-09-30")
            print("   GET /api/analytics/goals/vs_actual?period_type=quarterly&start_date=2025-04-01&end_date=2025-09-30")
            
            print("\n📊 Deberías ver:")
            print("   - Porcentajes de cumplimiento reales")
            print("   - Status: exceeded/on_track/at_risk/failed")
            print("   - Comparación entre meta y ventas reales")
            
        except Exception as e:
            print(f"\n❌ ERROR: {e}")
            import traceback
            traceback.print_exc()
            db.session.rollback()


if __name__ == "__main__":
    main()
