# Funcionalidad LaTeX en MatComFunctionLab

## Descripción

Se ha agregado soporte para renderizado LaTeX en la ventana de información detallada de funciones. Esta funcionalidad permite mostrar las funciones matemáticas y sus derivadas en formato LaTeX profesional, mejorando significativamente la legibilidad y presentación de las expresiones matemáticas.

## Características Implementadas

### 1. Renderizado LaTeX de Funciones
- La función principal se muestra en formato LaTeX: `f(x) = expresión`
- Soporte completo para símbolos matemáticos, fracciones, exponentes y funciones especiales
- Integración con el tema oscuro de la aplicación

### 2. Renderizado LaTeX de Derivadas
- Primera derivada: `f'(x) = expresión`
- Segunda derivada: `f''(x) = expresión`
- Formato matemático profesional con símbolos apropiados

### 3. Manejo de Errores
- Fallback automático a texto plano si el renderizado LaTeX falla
- Mensajes de error informativos
- Validación robusta de expresiones

## Tecnologías Utilizadas

- **Matplotlib**: Para renderizado LaTeX
- **SymPy**: Para conversión de expresiones a formato LaTeX
- **PIL (Pillow)**: Para procesamiento de imágenes
- **CustomTkinter**: Para integración con la interfaz

## Nuevos Métodos Implementados

### `_create_latex_image(latex_string, font_size)`
Crea una imagen PNG a partir de una cadena LaTeX usando matplotlib.

**Parámetros:**
- `latex_string`: Cadena en formato LaTeX
- `font_size`: Tamaño de fuente (por defecto 14)

**Retorna:** Objeto `ImageTk.PhotoImage` para mostrar en tkinter

### `_sympy_to_latex(expr_str)`
Convierte una expresión de SymPy a formato LaTeX.

**Parámetros:**
- `expr_str`: Cadena de expresión de SymPy

**Retorna:** Cadena formateada en LaTeX

### `_add_latex_display(parent_frame, latex_string, row, label_text, font_size)`
Agrega una expresión matemática renderizada en LaTeX al frame.

**Parámetros:**
- `parent_frame`: Frame padre donde agregar el display
- `latex_string`: Cadena LaTeX a renderizar
- `row`: Número de fila actual
- `label_text`: Texto de etiqueta opcional
- `font_size`: Tamaño de fuente

**Retorna:** Próximo número de fila

## Ejemplos de Uso

### Función Cuadrática
```
Entrada: x**2 + 3*x + 2
LaTeX: f(x) = x^2 + 3x + 2
Primera derivada: f'(x) = 2x + 3
Segunda derivada: f''(x) = 2
```

### Función Trigonométrica
```
Entrada: sin(x) + cos(x)
LaTeX: f(x) = \sin(x) + \cos(x)
Primera derivada: f'(x) = \cos(x) - \sin(x)
Segunda derivada: f''(x) = -\sin(x) - \cos(x)
```

### Función Exponencial
```
Entrada: exp(x) * x
LaTeX: f(x) = e^x \cdot x
Primera derivada: f'(x) = e^x \cdot x + e^x
Segunda derivada: f''(x) = e^x \cdot x + 2e^x
```

## Configuración del Tema

El renderizado LaTeX está optimizado para el tema oscuro de CustomTkinter:
- Fondo: `#2b2b2b`
- Texto: Blanco
- Fuente: Serif para mejor legibilidad matemática
- DPI: 120 para alta calidad

## Manejo de Casos Especiales

1. **Expresiones inválidas**: Se muestra un mensaje de error en LaTeX
2. **Expresiones complejas**: Fallback automático a texto plano
3. **Funciones no disponibles**: Muestra "No disponible" en formato LaTeX
4. **Parámetros**: Se muestran como valores numéricos en la descripción

## Mejoras Futuras

- [ ] Soporte para funciones de múltiples variables
- [ ] Renderizado LaTeX para asíntotas y puntos críticos
- [ ] Exportación de expresiones LaTeX a archivos
- [ ] Configuración personalizable de colores y tamaños
- [ ] Soporte para matemáticas en línea vs display

## Troubleshooting

### Problema: Las imágenes LaTeX no se muestran
**Solución:** Verificar que matplotlib tenga soporte LaTeX instalado

### Problema: Expresiones muy largas se cortan
**Solución:** Las imágenes se redimensionan automáticamente, pero se puede ajustar `max_width` en `_create_latex_image`

### Problema: Colores no coinciden con el tema
**Solución:** Los colores están configurados para tema oscuro en `#2b2b2b`
