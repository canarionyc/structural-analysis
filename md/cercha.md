---
format:
	pdf
---

# Análisis Estructural de Cercha y Unión Atornillada

## 1. Geometría de la Cercha

La cercha analizada tiene las siguientes dimensiones y configuración de nodos y barras:

*   **Distancias Horizontales (desde Soporte A):**
    *   `x_A = 0.0 m`
    *   `x_E = 1.5 m`
    *   `x_B = 3.0 m`
    *   `x_F = 4.5 m`
    *   `x_C = 6.0 m`
    *   `x_G = 7.5 m`
    *   `x_D = 9.0 m`
*   **Profundidad Vertical (h):** `1.5 m`

Los nodos y barras se configuran como se muestra en la siguiente figura:

![Truss Geometry and Node Labels](../img/truss_geometry.png)

## 2. Cargas Externas

Se aplican las siguientes cargas externas a la cercha:

*   **Cargas Verticales en el Cordón Inferior:**
    *   `F_Ey = -60.0 kN`
    *   `F_Fy = -200.0 kN`
    *   `F_Gy = -100.0 kN`
*   **Cargas Inclinadas en Nodos B y C (200 kN a 70 grados):**
    *   `F_Bx = -68.40 kN`
    *   `F_By = -187.94 kN`
    *   `F_Cx = -68.40 kN`
    *   `F_Cy = -187.94 kN`

## 3. Reacciones Globales

Las reacciones calculadas en los apoyos son:

*   **Reacción en A (X-dir):** `R_Ax = 136.81 kN`
*   **Reacción en A (Y-dir):** `R_Ay = 380.08 kN`
*   **Reacción en D (Y-dir):** `R_Dy = 355.80 kN`

## 4. Método de las Secciones (Barra EF)

Aplicando el método de las secciones y sumando momentos alrededor del Nodo B, se obtiene la fuerza axial en la barra EF:

*   **Fuerza Axial en Barra EF (N_Ed):** `649.22 kN`
*   **Estado:** Tensión (Tracción)

## 5. Dimensionado del Perfil (Tracción)

Para la barra EF, que está a tracción, se realiza el dimensionado del perfil:

*   **Esfuerzo de diseño (N_Ed):** `649.22 kN`
*   **Resistencia de cálculo (f_yd):** `261.90 N/mm2`
*   **Área total requerida:** `24.79 cm2`
*   **Área requerida por cada perfil UPN:** `12.40 cm2`

**Perfil Seleccionado:** DOBLE UPN 120
*   **Área aportada por un UPN 120:** `17.00 cm2`
*   **Área total aportada (2x):** `34.00 cm2 > 24.79 cm2 (OK!)`

## 6. Unión Atornillada (Diseño de Tornillos)

Se diseña la unión atornillada para la barra EF con las siguientes propiedades:

*   **Carga de diseño (N_Ed):** `649.22 kN`
*   **Diámetro del tornillo (d_bolt):** `20.0 mm`
*   **Diámetro del agujero (d_hole):** `22.0 mm`
*   **Espesor de la cartela (t_cartela):** `14.0 mm`
*   **Espesor del alma de UPN (t_upn_web):** `6.0 mm`

### 6.1. Comprobación a Cortadura (Shear)

*   **Tensión de cortadura de diseño:** `143.60 N/mm2`
*   **Resistencia de un tornillo a cortadura (doble cortadura):** `90.25 kN`

### 6.2. Comprobación a Contacto (Bearing)

*   **Espesor mínimo gobernante (Cartela vs 2x UPN):** `12.0 mm` (2x UPN web)
*   **Tensión de contacto de diseño:** `523.81 N/mm2`
*   **Resistencia de un tornillo a contacto:** `125.71 kN`

### 6.3. Cálculo Final de Tornillos

*   **Capacidad gobernante por tornillo:** `90.25 kN` (gobernado por cortadura)
*   **Número teórico de tornillos:** `7.19`
*   **Número de tornillos a instalar:** `8 tornillos` (en una fila)

### 6.4. Representación 3D de la Conexión

A continuación se muestra la representación 3D de la unión atornillada con 8 tornillos M20:

![Final 8 Bolt Connection Render](../img/final_connection_render.png)

### CONCLUSIÓN: Unión de 8 tornillos M20 para carga de 649.22 kN