import tkinter as tk
from tkinter import messagebox, simpledialog, scrolledtext
import numpy as np

class SimplexMinimization:
    def __init__(self, c, A, b, signs):
        self.c = np.array(c, dtype=float)
        self.A = np.array(A, dtype=float)
        self.b = np.array(b, dtype=float)
        self.signs = signs
        self.tableaux = []
        self.steps = []
        self.var_names = []
        self.n = len(c)
        self.m = len(b)

    def build_tableau(self):
        # Construye la tabla inicial considerando restricciones mixtas y método Big M
        n, m = self.n, self.m
        slack_cols = []
        artificial_cols = []
        self.var_names = ['x'+str(i+1) for i in range(n)]
        for i, sign in enumerate(self.signs):
            slack = [0]*m
            art = [0]*m
            if sign == '<=':
                slack[i] = 1
            elif sign == '>=':
                slack[i] = -1
                art[i] = 1
            elif sign == '=':
                art[i] = 1
            slack_cols.append(slack)
            artificial_cols.append(art)
        S = np.array(slack_cols).T
        A = np.array(artificial_cols).T
        tableau = np.hstack([self.A, S, A, self.b.reshape(-1,1)])
        # Objetivo extendido con penalización Big M
        M = 1e6
        c_ext = np.hstack([self.c, [0]*m, [-M]*m, [0]])
        self.tableaux = [tableau]
        self.c_ext = c_ext
        self.var_names += ['s'+str(i+1) for i in range(m)]
        self.var_names += ['a'+str(i+1) for i in range(m)]
        self.var_names += ['RHS']
        self.steps = ['Tabla inicial (Big M)']

    def is_optimal(self, tableau):
        # En minimización, óptimo si todos los coeficientes de la fila Z (excepto RHS) son >= 0
        z_row = self.get_z_row(tableau)
        return np.all(z_row[:-1] >= 0)

    def get_z_row(self, tableau):
        # Calcula la fila Z para el método Big M, sumando -M solo si la artificial está en la base
        num_cols = tableau.shape[1] - 1  # sin RHS
        num_rows = tableau.shape[0]
        c_ext = self.c_ext[:num_cols]
        M = 1e6
        # Encuentra las variables básicas y sus costos
        basic_vars = []
        basic_costs = []
        for row in range(num_rows):
            col_idx = None
            for col in range(num_cols):
                col_vals = tableau[:, col]
                if np.count_nonzero(col_vals) == 1 and np.isclose(col_vals[row], 1.0):
                    col_idx = col
                    break
            if col_idx is not None:
                basic_vars.append(col_idx)
                # Si la variable es artificial, su costo es -M
                if self.var_names[col_idx].startswith('a'):
                    basic_costs.append(-M)
                else:
                    basic_costs.append(c_ext[col_idx])
            else:
                basic_vars.append(None)
                basic_costs.append(0.0)
        # Calcula Zj para cada columna
        Z = np.zeros(num_cols)
        for j in range(num_cols):
            for i in range(num_rows):
                Z[j] += basic_costs[i] * tableau[i, j]
        # Zj - Cj
        z_row = Z - c_ext
        # Agrega el RHS (no se usa en la fila Z)
        z_row = np.append(z_row, 0.0)
        return z_row

    def iterate(self):
        tableau = self.tableaux[-1].copy()
        z_row = self.get_z_row(tableau)
        # Selecciona la columna con el valor más negativo en la fila Z
        candidates = np.where(z_row[:-1] < 0)[0]
        if len(candidates) == 0:
            return False
        col = candidates[np.argmin(z_row[candidates])]
        # Selección de fila pivote (mínima razón positiva)
        ratios = []
        for i in range(tableau.shape[0]):
            if tableau[i, col] > 1e-8:
                ratios.append(tableau[i, -1] / tableau[i, col])
            else:
                ratios.append(np.inf)
        min_ratio = min(ratios)
        if min_ratio == np.inf:
            self.steps.append("Problema sin solución factible (solución ilimitada)")
            return False
        row = ratios.index(min_ratio)
        # Guardar paso algebraico
        paso = f"Pivote en fila {row+1}, columna {col+1} ({self.var_names[col]})\n"
        paso += f"1/{tableau[row, col]:.2f} * F{row+1}\n"
        for i in range(tableau.shape[0]):
            if i != row:
                paso += f"F{i+1} = F{i+1} - ({tableau[i, col]:.2f}) * F{row+1}\n"
        pivot = tableau[row, col]
        tableau[row, :] = tableau[row, :] / pivot
        for i in range(tableau.shape[0]):
            if i != row:
                tableau[i, :] -= tableau[i, col] * tableau[row, :]
        self.tableaux.append(tableau)
        self.steps.append(paso)
        return True

    def solve(self, max_iter=100):
        self.build_tableau()
        iter_count = 0
        while not self.is_optimal(self.tableaux[-1]):
            if not self.iterate():
                break
            iter_count += 1
            if iter_count >= max_iter:
                self.steps.append(f"Se alcanzó el límite de {max_iter} iteraciones. Puede que el problema sea degenerado o no tenga solución óptima.")
                break
        # Mostrar solución óptima
        self.steps.append(self.get_solution())

    def get_solution(self):
        tableau = self.tableaux[-1]
        num_vars = self.n
        sol = [0.0]*num_vars
        for j in range(num_vars):
            col = tableau[:, j]
            if np.count_nonzero(col) == 1 and np.isclose(np.max(col), 1.0):
                row = np.argmax(col)
                sol[j] = tableau[row, -1]
        z = np.dot(self.c, sol)
        res = "\nSolución óptima:\n"
        for i, val in enumerate(sol):
            res += f"x{i+1} = {val:.4f}\n"
        res += f"Valor óptimo de Z = {z:.4f}\n"
        return res

    def get_steps(self):
        result = ""
        for i, tableau in enumerate(self.tableaux):
            result += f"{self.steps[i]}\n"
            result += self.format_tableau(tableau) + "\n"
        return result

    def format_tableau(self, tableau):
        s = "\t".join(self.var_names) + "\n"
        # Fila Z como primera fila
        z_row = self.get_z_row(tableau)
        s += "Z\t" + "\t".join([f"{v:.2f}" for v in z_row]) + "\n"
        # Filas de restricciones
        for i, row in enumerate(tableau):
            s += f"F{i+1}\t" + "\t".join([f"{v:.2f}" for v in row]) + "\n"
        return s

class SimplexApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Calculadora Simplex Minimización")
        self.create_widgets()

    def create_widgets(self):
        tk.Label(self.root, text="Función objetivo (ejemplo: z = 2x1 + x2)").pack()
        self.entry_c = tk.Entry(self.root, width=50)
        self.entry_c.pack()
        tk.Label(self.root, text="Número de variables:").pack()
        self.entry_n = tk.Entry(self.root, width=10)
        self.entry_n.pack()
        tk.Label(self.root, text="Restricciones (una por línea, ejemplo: 2x1 + x2 <= 18)").pack()
        self.text_restricciones = scrolledtext.ScrolledText(self.root, width=80, height=8)
        self.text_restricciones.pack()
        tk.Button(self.root, text="Resolver", command=self.get_restrictions).pack(pady=10)
        tk.Label(self.root, text="Resultado y tablas:").pack()
        self.text_steps = scrolledtext.ScrolledText(self.root, width=80, height=30)
        self.text_steps.pack()

    def get_restrictions(self):
        try:
            n = int(self.entry_n.get())
        except Exception:
            messagebox.showerror("Error", "Verifica el número de variables.")
            return
        expr_obj = self.entry_c.get()
        restricciones = self.text_restricciones.get("1.0", tk.END).strip().splitlines()
        if not expr_obj or not restricciones:
            messagebox.showerror("Error", "Debes ingresar la función objetivo y al menos una restricción.")
            return
        c = self.parse_expression(expr_obj, n)
        A, b, signs = [], [], []
        for expr in restricciones:
            if expr.strip():
                try:
                    coefs, signo, bi = self.parse_constraint(expr, n)
                except Exception:
                    messagebox.showerror("Error", f"Error en la restricción: {expr}")
                    return
                A.append(coefs)
                signs.append(signo)
                b.append(bi)
        self.solve_simplex(c, A, b, signs)

    def parse_expression(self, expr, n):
        # Elimina 'z =' si está presente y espacios
        expr = expr.replace('Z', '').replace('z', '').replace('=', '').replace(' ', '').strip()
        coefs = [0.0]*n
        import re
        # Encuentra todos los términos tipo axk
        terms = re.findall(r'([+-]?\d*\.?\d*)x(\d+)', expr)
        for coef, var in terms:
            if coef in ['', '+', '-']:
                coef = coef+'1' if coef else '1'
            coefs[int(var)-1] = float(coef)
        return coefs

    def parse_constraint(self, expr, n):
        import re
        expr = expr.replace(' ', '')
        # Encuentra el signo
        if '<=' in expr:
            signo = '<='
            left, right = expr.split('<=')
        elif '>=' in expr:
            signo = '>='
            left, right = expr.split('>=')
        elif '=' in expr:
            signo = '='
            left, right = expr.split('=')
        else:
            raise ValueError('Signo de restricción no reconocido.')
        coefs = [0.0]*n
        terms = re.findall(r'([+-]?\d*\.?\d*)x(\d+)', left)
        for coef, var in terms:
            if coef in ['', '+', '-']:
                coef = coef+'1' if coef else '1'
            coefs[int(var)-1] = float(coef)
        bi = float(right)
        return coefs, signo, bi

    def solve_simplex(self, c, A, b, signs):
        simplex = SimplexMinimization(c, A, b, signs)
        simplex.solve()
        steps = simplex.get_steps()
        self.text_steps.delete(1.0, tk.END)
        self.text_steps.insert(tk.END, steps)

if __name__ == "__main__":
    root = tk.Tk()
    app = SimplexApp(root)
    root.mainloop()
