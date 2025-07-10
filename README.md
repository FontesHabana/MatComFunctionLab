# MatComFunctionLab

MatComFunctionLab es una aplicación completa para el análisis matemático de funciones que permite calcular, analizar y visualizar funciones matemáticas con todas sus características importantes.

## ✨ Funcionalidades Principales

### 📊 Análisis Completo de Funciones
- **Cálculo de funciones**: Evaluación precisa de funciones matemáticas
- **Derivadas**: Primera y segunda derivada con análisis completo
- **Dominio**: Determinación automática del dominio de la función
- **Interceptos**: Cálculo de interceptos con los ejes X e Y
- **Simetría**: Análisis de simetría par, impar o sin simetría especial

### 📈 Análisis de Asíntotas
- **Asíntotas verticales**: Detección automática de discontinuidades infinitas
- **Asíntotas horizontales**: Cálculo de límites en el infinito
- **Asíntotas oblicuas**: Determinación de asíntotas inclinadas cuando aplique

### 🎯 Puntos Críticos y Extremos
- **Máximos y mínimos locales**: Localización precisa usando criterio de la segunda derivada
- **Puntos críticos**: Identificación de puntos donde f'(x) = 0
- **Análisis de monotonía**: Determinación de intervalos crecientes y decrecientes

### 🔄 Análisis de Concavidad
- **Puntos de inflexión**: Localización de cambios en la concavidad
- **Intervalos de concavidad**: Análisis de concavidad hacia arriba y hacia abajo
- **Criterio de la segunda derivada**: Implementación del test de concavidad

### 📊 Visualización Avanzada
- **Graficación completa**: Representación visual de la función y todos sus elementos
- **Marcadores especiales**: 
  - Puntos rojos para máximos
  - Puntos verdes para mínimos  
  - Puntos morados para inflexiones
  - Puntos negros para interceptos
- **Asíntotas visuales**: Líneas punteadas rojas para todas las asíntotas
- **Parámetros ajustables**: Sliders interactivos para modificar parámetros en tiempo real

## 🚀 Instalación

### Requisitos
- Python 3.8 o superior
- Las dependencias se instalan automáticamente

### Instalación de dependencias
```bash
pip install -r requirements.txt
```

### Dependencias incluidas:
- `customtkinter >= 5.2.2` - Interfaz moderna
- `sympy >= 1.14.0` - Cálculo simbólico
- `numpy >= 2.3.1` - Cálculos numéricos
- `matplotlib >= 3.10.3` - Graficación
- `Pillow >= 11.3.0` - Manejo de imágenes

## 🖥️ Uso

### Ejecución
```bash
python Main.py
```

### Interfaz Principal
1. **Campo de entrada**: Introduce tu función matemática
2. **Botón "Init"**: Inicia el análisis completo
3. **Ejemplos predefinidos**: Botones F1, F2, F3 con funciones de ejemplo

### Funciones de Ejemplo Incluidas
- `sin(x) + x**a` - Función trigonométrica con parámetro
- `cos(x) - log(x+a)` - Función mixta trigonométrica-logarítmica  
- `x**a - b*x` - Función polinómica paramétrica

### Sintaxis Soportada
- **Funciones básicas**: `x**2`, `x^3`, `sqrt(x)`
- **Trigonométricas**: `sin(x)`, `cos(x)`, `tan(x)`
- **Exponenciales**: `exp(x)`, `e**x`
- **Logarítmicas**: `log(x)`, `ln(x)`
- **Constantes**: `pi`, `e`
- **Parámetros**: `a`, `b`, `c`, etc. (ajustables con sliders)

## 📱 Características de la Interfaz

### Panel Izquierdo - Análisis
- **Parámetros ajustables**: Sliders de -5 a 5 con entrada manual
- **Resultados en tiempo real**: Actualización automática al cambiar parámetros
- **Análisis completo**: Dominio, interceptos, simetría, asíntotas, derivadas, monotonía, extremos, concavidad

### Panel Derecho - Visualización
- **Gráfico interactivo**: Zoom y navegación
- **Leyenda informativa**: Identificación de todos los elementos
- **Colores distintivos**: Cada tipo de punto tiene su color específico
- **Asíntotas claramente marcadas**: Líneas punteadas para mejor visualización

## 🔧 Arquitectura del Proyecto

```
MatComFunctionLab/
├── Main.py                 # Punto de entrada
├── funciones.py           # Ejemplos de funciones
├── requirements.txt       # Dependencias
├── Interface/
│   ├── App.py            # Interfaz principal
│   └── show_info.py      # Ventana de resultados
├── Models/
│   ├── function.py       # Analizador de funciones
│   ├── differential.py   # Cálculo de derivadas
│   └── main_function.py  # Procesador principal
└── Utils/
    └── math_utils.py     # Utilidades matemáticas
```

## 🧮 Capacidades Matemáticas

### Tipos de Funciones Soportadas
- ✅ Polinómicas de cualquier grado
- ✅ Racionales (cociente de polinomios)
- ✅ Trigonométricas y trigonométricas inversas
- ✅ Exponenciales y logarítmicas
- ✅ Funciones con radicales
- ✅ Funciones compuestas complejas
- ✅ Funciones paramétricas

### Análisis Matemático Completo
- ✅ Límites y continuidad
- ✅ Derivabilidad
- ✅ Comportamiento asintótico
- ✅ Clasificación de puntos críticos
- ✅ Estudio de la variación
- ✅ Análisis de la curvatura

## 🎨 Ejemplos de Uso

### Función Cuadrática
```
Entrada: x**2 - 4*x + 3
Análisis: 
- Dominio: ℝ
- Vértice en (2, -1)
- Interceptos en (1,0) y (3,0)
- Intercepto Y en (0,3)
- Cóncava hacia arriba
```

### Función Racional
```
Entrada: 1/(x**2 - 4)
Análisis:
- Dominio: ℝ \ {-2, 2}
- Asíntotas verticales en x = -2, x = 2
- Asíntota horizontal en y = 0
- Máximo en (0, -1/4)
```

### Función Trigonométrica
```
Entrada: sin(x) + cos(2*x)
Análisis:
- Dominio: ℝ
- Función periódica
- Múltiples extremos locales
- Sin asíntotas
```

## 🐛 Solución de Problemas

### Errores Comunes
1. **"Función inválida"**: Verifica la sintaxis (usa `**` para potencias, no `^`)
2. **"Error de graficación"**: La función puede tener discontinuidades extremas
3. **Parámetros faltantes**: Asegúrate de definir todos los parámetros necesarios

### Limitaciones
- Las funciones muy complejas pueden tardar en procesarse
- Los rangos de graficación están limitados a [-10, 10] por defecto
- Algunas funciones patológicas pueden no analizarse completamente

## 🔄 Actualizaciones Futuras

- [ ] Soporte para funciones de múltiples variables
- [ ] Exportación de gráficos en alta resolución
- [ ] Análisis de series de Taylor
- [ ] Integración numérica
- [ ] Ecuaciones diferenciales básicas

## 👥 Contribuciones

Este proyecto está abierto a contribuciones. Si encuentras errores o tienes sugerencias de mejora, por favor:

1. Reporta el problema detalladamente
2. Proporciona ejemplos de funciones problemáticas
3. Sugiere mejoras en la interfaz o funcionalidad

## 📜 Licencia

Ver archivo `LICENSE` para detalles de la licencia.

---

**MatComFunctionLab** - Tu laboratorio completo para el análisis de funciones matemáticas 🧪📊

**MatcomFunctionLab** es una aplicación completa para el análisis matemático de funciones que proporciona herramientas avanzadas para estudiar el comportamiento de funciones matemáticas.

## 🚀 Funcionalidades Principales

### 📊 Análisis Matemático Completo
- **Cálculo de función**: Evaluación de funciones en puntos específicos
- **Derivadas**: Cálculo automático de primera y segunda derivada
- **Máximos y mínimos**: Identificación de extremos locales y globales
- **Puntos de inflexión**: Localización de cambios en la concavidad
- **Asíntotas**: Detección de asíntotas horizontales, verticales y oblicuas
- **Dominio y rango**: Análisis del dominio de definición
- **Interceptos**: Puntos de intersección con los ejes
- **Simetría**: Análisis de simetría par/impar
- **Monotonía**: Intervalos de crecimiento y decrecimiento
- **Concavidad**: Análisis de concavidad hacia arriba/abajo

### 📈 Visualización Avanzada
- **Graficación completa**: Representación visual de la función
- **Marcadores especiales**: Visualización de extremos, puntos de inflexión e interceptos
- **Asíntotas visuales**: Representación gráfica de todas las asíntotas
- **Parámetros ajustables**: Sliders interactivos para funciones parametrizadas
- **Zoom y navegación**: Herramientas para explorar diferentes regiones del gráfico

### 🔧 Características Técnicas
- **Motor simbólico**: Powered by SymPy para cálculos exactos
- **Interfaz moderna**: Construida con CustomTkinter
- **Graficación profesional**: Matplotlib integrado
- **Manejo de errores**: Sistema robusto de validación y manejo de excepciones
- **Modularidad**: Arquitectura limpia y extensible

## 🛠️ Instalación

### Prerrequisitos
- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### Instalación de dependencias
```bash
pip install -r requirements.txt
```

### Dependencias principales
- `customtkinter>=5.2.2`: Interfaz de usuario moderna
- `sympy>=1.14.0`: Motor de cálculo simbólico
- `numpy>=2.3.1`: Cálculos numéricos
- `matplotlib>=3.10.3`: Graficación
- `Pillow>=11.3.0`: Manejo de imágenes

## 🚀 Uso

### Ejecutar la aplicación
```bash
python Main.py
```

### Ejemplos de funciones soportadas
- **Polinómicas**: `x**3 - 2*x**2 + x - 1`
- **Racionales**: `(x**2 - 1)/(x - 2)`
- **Trigonométricas**: `sin(x) + cos(2*x)`
- **Exponenciales**: `exp(-x**2/2)`
- **Logarítmicas**: `log(x + 1)`
- **Mixtas**: `x*sin(x) + exp(-x)`
- **Parametrizadas**: `a*sin(b*x + c) + d*x**2`

### Sintaxis soportada
- Operadores básicos: `+`, `-`, `*`, `/`, `**` (potencia)
- Funciones trigonométricas: `sin()`, `cos()`, `tan()`, etc.
- Funciones exponenciales: `exp()`, `log()`, `sqrt()`
- Constantes: `pi`, `e`
- Parámetros: cualquier letra excepto `x`

## 📁 Estructura del Proyecto

```
MatcomFunctionLab/
├── Main.py                 # Punto de entrada de la aplicación
├── requirements.txt        # Dependencias del proyecto
├── funciones.py           # Ejemplos y utilidades de funciones
├── README.md              # Documentación
├── LICENSE                # Licencia del proyecto
├── Interface/             # Módulos de interfaz de usuario
│   ├── __init__.py
│   ├── App.py            # Ventana principal
│   └── show_info.py      # Ventana de resultados
├── Models/               # Lógica de negocio y cálculos
│   ├── __init__.py
│   ├── function.py       # Analizador principal de funciones
│   ├── differential.py   # Cálculos diferenciales
│   └── main_function.py  # Coordinador de análisis
├── Utils/                # Utilidades matemáticas
│   ├── __init__.py
│   └── math_utils.py     # Funciones auxiliares
└── GUI/                  # Recursos gráficos
    ├── Functionapp.py    # Interfaz alternativa
    └── ecuacion_latex.png
```

## 🎯 Casos de Uso

### Para Estudiantes
- Verificación de tareas de cálculo
- Visualización de conceptos matemáticos
- Exploración interactiva de funciones
- Comprensión de derivadas e integrales

### Para Profesores
- Herramienta de enseñanza visual
- Generación de ejemplos
- Demostración de conceptos
- Preparación de material didáctico

### Para Investigadores
- Análisis rápido de funciones
- Validación de resultados teóricos
- Exploración de familias de funciones
- Prototipado matemático

## 🔄 Desarrollo y Contribución

### Arquitectura
El proyecto utiliza una arquitectura modular:
- **Interface**: Manejo de la interfaz de usuario
- **Models**: Lógica matemática y cálculos
- **Utils**: Funciones auxiliares y utilidades

### Extensibilidad
- Fácil adición de nuevos tipos de análisis
- Sistema de plugins para funciones especiales
- Interfaz configurable y personalizable

## 📋 Ejemplos de Análisis

### Función Polinómica: f(x) = x³ - 3x² + 2x + 1
- **Dominio**: ℝ (todos los reales)
- **Derivada**: f'(x) = 3x² - 6x + 2
- **Puntos críticos**: x ≈ 0.423, x ≈ 1.577
- **Punto de inflexión**: x = 1
- **Extremos**: Máximo local en (0.423, 1.519), Mínimo local en (1.577, 0.481)

### Función Racional: f(x) = (x² - 1)/(x - 2)
- **Dominio**: ℝ \ {2}
- **Asíntota vertical**: x = 2
- **Asíntota oblicua**: y = x + 2
- **Interceptos X**: x = ±1
- **Intercepto Y**: y = 1/2

## 🐛 Solución de Problemas

### Errores Comunes
1. **"Función inválida"**: Verificar sintaxis matemática
2. **"División por cero"**: Revisar denominadores en funciones racionales
3. **"Dominio no definido"**: Considerar restricciones como logaritmos de números negativos

### Limitaciones Conocidas
- Funciones muy complejas pueden requerir tiempo de cálculo adicional
- Algunas funciones especiales pueden no estar completamente soportadas
- La graficación tiene límites en rangos muy extremos

## 📧 Soporte

Para reportar errores, sugerir mejoras o solicitar nuevas funcionalidades, por favor contacta al equipo de desarrollo.

## 📄 Licencia

Este proyecto está bajo la licencia especificada en el archivo LICENSE.

---

**MatcomFunctionLab** - Herramienta profesional para análisis de funciones matemáticas 🧮✨

Una aplicación completa para el análisis matemático de funciones desarrollada en Python con interfaz gráfica moderna.

## ✨ Funcionalidades

### 📊 Análisis Completo de Funciones
- **Cálculo de derivadas**: Primera y segunda derivada
- **Dominio**: Determinación automática del dominio de la función
- **Interceptos**: Encuentra interceptos con los ejes X e Y
- **Simetría**: Análisis de simetría par, impar o ninguna
- **Asíntotas**: Detección de asíntotas verticales, horizontales y oblicuas
- **Puntos críticos**: Encuentra máximos y mínimos locales
- **Monotonía**: Análisis de intervalos crecientes y decrecientes
- **Puntos de inflexión**: Detección de cambios de concavidad
- **Concavidad**: Análisis de intervalos cóncavos hacia arriba/abajo

### 📈 Visualización Avanzada
- **Gráficos interactivos**: Representación visual completa de la función
- **Marcadores especiales**: 
  - Máximos locales (triángulos rojos)
  - Mínimos locales (triángulos verdes)
  - Puntos de inflexión (círculos naranjas)
  - Interceptos X (cuadrados azules)
  - Interceptos Y (diamantes púrpuras)
- **Asíntotas visuales**: Líneas punteadas para todas las asíntotas
- **Parámetros ajustables**: Sliders para modificar parámetros en tiempo real

### 🎛️ Interfaz Intuitiva
- **Diseño moderno**: Interfaz limpia y profesional con CustomTkinter
- **Panel de parámetros**: Ajuste en tiempo real con sliders y campos de texto
- **Panel de análisis**: Resultados detallados y organizados
- **Ejemplos predefinidos**: Funciones de ejemplo para empezar rápidamente

## 🚀 Instalación

### Requisitos
- Python 3.7 o superior
- Las dependencias se instalan automáticamente

### Instalación rápida
```bash
git clone https://github.com/usuario/MatComFunctionLab.git
cd MatComFunctionLab
pip install -r requirements.txt
python Main.py
```

### Dependencias principales
```
customtkinter>=5.2.2
sympy>=1.14.0
numpy>=2.3.1
matplotlib>=3.10.3
Pillow>=11.3.0
```

## 📖 Uso

1. **Iniciar la aplicación**: `python Main.py`
2. **Ingresar función**: Escribir la función matemática (ej: `x**2 + 2*x - 3`)
3. **Hacer clic en "Init"**: Para comenzar el análisis
4. **Ajustar parámetros**: Usar los sliders si la función tiene parámetros
5. **Explorar resultados**: Ver análisis detallado y gráfico interactivo

### Ejemplos de funciones soportadas:
- **Polinomiales**: `x**3 - 2*x**2 + x - 1`
- **Trigonométricas**: `sin(x)`, `cos(2*x)`, `tan(x/2)`
- **Exponenciales**: `exp(x)`, `2**x`
- **Logarítmicas**: `log(x)`, `ln(x+1)`
- **Racionales**: `1/x`, `(x+1)/(x-2)`
- **Con parámetros**: `a*x**2 + b*x + c`

## 🔧 Características Técnicas

### Arquitectura del proyecto:
```
MatComFunctionLab/
├── Main.py                 # Punto de entrada
├── Interface/
│   ├── App.py             # Interfaz principal
│   └── show_info.py       # Ventana de resultados
├── Models/
│   ├── function.py        # Análisis de funciones
│   ├── differential.py    # Cálculos diferenciales
│   └── main_function.py   # Coordinador principal
├── Utils/
│   └── math_utils.py      # Utilidades matemáticas
└── requirements.txt       # Dependencias
```

### Algoritmos implementados:
- **Análisis simbólico** con SymPy
- **Resolución de ecuaciones** algebraicas
- **Cálculo de límites** para asíntotas
- **Derivación automática** hasta tercer orden
- **Evaluación numérica** segura
- **Filtrado de soluciones** reales

## 🎯 Casos de uso

- **Estudiantes**: Aprender análisis de funciones visualizando conceptos
- **Profesores**: Herramienta didáctica para enseñanza de cálculo
- **Ingenieros**: Análisis rápido de funciones técnicas
- **Investigadores**: Exploración de comportamiento de funciones

## 🛠️ Desarrollo

### Estructura de clases principales:
- **FunctionAnalyzer**: Análisis completo de funciones
- **DifferentialCalculator**: Cálculos diferenciales especializados
- **MainFunctionProcessor**: Coordinador de análisis
- **MathUtils**: Utilidades matemáticas compartidas

### Extensiones futuras:
- Análisis de funciones de múltiples variables
- Exportación de resultados a PDF/LaTeX
- Interfaz web
- Análisis numérico avanzado
- Integración simbólica

## 📝 Contribuir

1. Fork del repositorio
2. Crear rama para nueva función (`git checkout -b feature/nueva-funcion`)
3. Commit de cambios (`git commit -am 'Agregar nueva función'`)
4. Push a la rama (`git push origin feature/nueva-funcion`)
5. Crear Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver archivo `LICENSE` para más detalles.

## 🆘 Soporte

Si encuentras algún problema o tienes sugerencias:
- Crear un Issue en GitHub
- Contactar a los desarrolladores
- Revisar la documentación

---

**MatcomFunctionLab** - Haciendo el análisis matemático más accesible y visual. 🧮✨