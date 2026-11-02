# Especificación de Requisitos - EcoClima 360

## 1. Requisitos Funcionales (RF)
- **RF-01 (Carga de Datos):** La aplicación debe cargar automáticamente el dataset procesado desde `data/datos.csv` sin fallos de ruta.
- **RF-02 (Filtro Geográfico):** Permitir al usuario filtrar los registros meteorológicos por departamento de Colombia mediante un menú desplegable con la opción "Todos".
- **RF-03 (Indicadores Globales):** Mostrar métricas descriptivas clave en la pantalla de inicio (Total de estaciones, total de departamentos y promedio de precipitación).
- **RF-04 (Manejo de Navegación):** Garantizar la transición fluida entre las 4 páginas principales (`inicio.py`, `explorar.py`, `jugar.py`, `mis_datos.py`).
- **RF-05 (Módulo Lúdico):** Incluir una experiencia interactiva basada en datos reales dentro de la sección Jugar.

## 2. Requisitos No Funcionales (RNF)
- **RNF-01 (Usabilidad y Diseño):** Presentar una interfaz limpia, coherente con la identidad visual del proyecto y adaptable a la pantalla del usuario.
- **RNF-02 (Rendimiento):** El tiempo de respuesta al aplicar filtros sobre los datos debe ser menor a 2 segundos.
- **RNF-03 (Tolerancia a Fallos):** Implementar estructuras de control de excepciones (`try-except`) para evitar caídas del sistema ante archivos no encontrados o corruptos.