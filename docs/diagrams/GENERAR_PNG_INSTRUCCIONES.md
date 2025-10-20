# INSTRUCCIONES: Generar PNG desde PlantUML

**Fecha**: 19 de Octubre, 2025  
**Autor**: Wilker  
**Objetivo**: Exportar los 7 diagramas PlantUML a formato PNG para entrega académica

---

## Opción 1: PlantUML Online (RECOMENDADO - Más Rápido)

### Paso a paso:

1. **Abrir el servidor online de PlantUML:**
   - URL: https://www.plantuml.com/plantuml/uml/

2. **Para cada archivo .puml en `docs/diagrams/`:**
   
   **a) ERD_database.puml**
   - Abrir el archivo en VSCode
   - Copiar TODO el contenido
   - Pegar en el editor de PlantUML online
   - Click en "Submit"
   - Click derecho en la imagen generada → "Guardar imagen como..."
   - Guardar como: `docs/diagrams/ERD_database.png`

   **b) ARCHITECTURE_layers.puml**
   - Repetir proceso anterior
   - Guardar como: `docs/diagrams/ARCHITECTURE_layers.png`

   **c) CLASS_diagram.puml**
   - Repetir proceso
   - Guardar como: `docs/diagrams/CLASS_diagram.png`

   **d) USE_CASES.puml**
   - Repetir proceso
   - Guardar como: `docs/diagrams/USE_CASES.png`

   **e) SEQ_auth.puml**
   - Repetir proceso
   - Guardar como: `docs/diagrams/SEQ_auth.png`

   **f) SEQ_invoice.puml**
   - Repetir proceso
   - Guardar como: `docs/diagrams/SEQ_invoice.png`

---

## Opción 2: VSCode Extension (Si tienes Java instalado)

### Instalación:

1. Abrir VSCode
2. Ir a Extensions (Ctrl+Shift+X)
3. Buscar: "PlantUML"
4. Instalar: "PlantUML" by jebbs

### Uso:

1. Abrir cualquier archivo `.puml` en VSCode
2. Presionar `Alt+D` para preview
3. Click derecho en preview → "Export Current Diagram"
4. Seleccionar formato: PNG
5. Guardar en la misma carpeta `docs/diagrams/`

### Verificar Java:

```powershell
java -version
```

Si no tienes Java, instalar desde: https://www.java.com/download/

---

## Opción 3: Línea de Comandos (Avanzado)

### Si tienes PlantUML JAR:

```powershell
# Navegar a la carpeta de diagramas
cd docs\diagrams

# Generar todos los PNG de una vez
java -jar plantuml.jar *.puml

# Verificar que se generaron
dir *.png
```

### Descargar PlantUML JAR:
- URL: https://plantuml.com/download
- Descargar: plantuml.jar
- Guardar en alguna carpeta de tu sistema

---

## Checklist de Archivos Generados

Al finalizar, deberías tener estos 7 archivos PNG:

- [ ] `docs/diagrams/ERD_database.png` - Diagrama Entidad-Relación (21 tablas)
- [ ] `docs/diagrams/ARCHITECTURE_layers.png` - Clean Architecture (3 capas)
- [ ] `docs/diagrams/CLASS_diagram.png` - UML Clases (Handlers)
- [ ] `docs/diagrams/USE_CASES.puml` - Casos de uso (3 actores, 15+ casos)
- [ ] `docs/diagrams/SEQ_auth.png` - Secuencia de autenticación JWT
- [ ] `docs/diagrams/SEQ_invoice.png` - Secuencia de creación de factura

---

## Verificación Visual

Cada PNG debería mostrar:
- ✅ Texto legible (zoom al 100%)
- ✅ Conexiones claras entre elementos
- ✅ Colores distintivos (según el tema PlantUML)
- ✅ Tamaño adecuado (mínimo 800px de ancho)

Si algún diagrama se ve muy pequeño o ilegible:
- En PlantUML online: Ajustar con `scale 1.5` al inicio del código
- En VSCode: Cambiar configuración de DPI en settings

---

## Problemas Comunes

### Error: "Syntax Error" en PlantUML Online
- **Causa**: Código PlantUML incorrecto
- **Solución**: Verificar que copiaste TODO el contenido del archivo .puml
- **Verificar**: Que las líneas `@startuml` y `@enduml` estén incluidas

### PNG se ve cortado o muy pequeño
- **Solución 1**: Agregar `scale 1.5` después de `@startuml`
- **Solución 2**: Usar formato SVG y luego convertir a PNG
- **Solución 3**: Aumentar resolución en configuración de PlantUML

### Java no reconocido (Opción 2/3)
- **Causa**: Java no está instalado o no está en PATH
- **Solución**: Usar Opción 1 (online) que no requiere Java
- **Alternativa**: Instalar Java JDK 11+ y agregar a PATH del sistema

---

## Tiempo Estimado

- **Opción 1 (Online)**: 15-20 minutos (recomendado)
- **Opción 2 (VSCode)**: 10-15 minutos (si ya tienes Java)
- **Opción 3 (CLI)**: 5 minutos (si ya tienes PlantUML JAR)

---

## Próximo Paso

Una vez generados los 7 PNG, continuar con:
- ✅ Wireframes (WF-001 a WF-008) usando Figma/Excalidraw
- ✅ Verificación de documentos de requerimientos
- ✅ Commit y push de todos los artefactos

---

**¡Éxito!** 🚀
