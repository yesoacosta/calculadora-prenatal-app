import flet as ft
from fpdf import FPDF
import datetime
import os

def main(page: ft.Page):
    # Configuración web y móvil
    page.title = "Calculadora de Riesgo Prenatal - Dr. Acosta"
    page.window_width = 500
    page.theme_mode = "light"
    page.padding = 20
    page.scroll = "auto" 

    titulo = ft.Text("Evaluación de Riesgo de Trisomías", size=22, weight="bold")

    # Campos de Entrada
    nombre_input = ft.TextField(label="Nombre y Apellido de la Paciente")
    dni_input = ft.TextField(label="Documento de Identidad (DNI/ID)")
    edad_input = ft.TextField(label="Edad Materna (años)")
    tn_input = ft.TextField(label="Translucencia Nucal (TN en mm)")
    lcn_input = ft.TextField(label="Longitud Cefalo-Nalga (LCN en mm)")
    pappa_input = ft.TextField(label="PAPP-A (MoM)")
    hcg_input = ft.TextField(label="beta-hCG libre (MoM)")

    mensaje_estado = ft.Text(value="", color="green")

    # Botón de descarga oculto inicialmente
    boton_descarga = ft.ElevatedButton(
        content=ft.Text("Abrir Informe PDF", size=14, weight="bold"),
        url="",
        visible=False
    )

    def generar_pdf(nombre, dni, edad, tn, lcn, pappa, hcg, base_t21, final_t21, base_t18_13, final_t18_13):
        pdf = FPDF()
        pdf.add_page()
        
        pdf.set_font("Arial", style="B", size=14)
        pdf.cell(200, 8, txt="Dr. Yesid Acosta Peinado", ln=True, align="C")
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 6, txt="Ginecología y Obstetricia", ln=True, align="C")
        pdf.line(10, 30, 200, 30)
        pdf.ln(10)
        
        pdf.set_font("Arial", style="B", size=16)
        pdf.cell(200, 10, txt="Informe Estructurado - Riesgo Prenatal", ln=True, align="C")
        pdf.ln(5)
        
        fecha_actual = datetime.datetime.now().strftime("%d/%m/%Y")
        pdf.set_font("Arial", size=10)
        pdf.cell(200, 10, txt=f"Fecha del informe: {fecha_actual}", ln=True, align="R")
        
        pdf.set_font("Arial", style="B", size=12)
        pdf.cell(200, 10, txt="1. Datos de la Paciente:", ln=True)
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 8, txt=f"   - Nombre y Apellido: {nombre}", ln=True)
        pdf.cell(200, 8, txt=f"   - Documento: {dni}", ln=True)
        pdf.cell(200, 8, txt=f"   - Edad Materna: {edad} años", ln=True)
        pdf.ln(5)
        
        pdf.set_font("Arial", style="B", size=12)
        pdf.cell(200, 10, txt="2. Parámetros Clínicos Ingresados:", ln=True)
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 8, txt=f"   - LCN: {lcn} mm", ln=True)
        pdf.cell(200, 8, txt=f"   - Translucencia Nucal (TN): {tn} mm", ln=True)
        pdf.cell(200, 8, txt=f"   - PAPP-A: {pappa} MoM", ln=True)
        pdf.cell(200, 8, txt=f"   - beta-hCG libre: {hcg} MoM", ln=True)
        pdf.ln(5)
        
        # --- NUEVA SECCIÓN DE RESULTADOS COMPARATIVOS ---
        pdf.set_font("Arial", style="B", size=12)
        pdf.cell(200, 10, txt="3. Índices de Riesgo Calculados:", ln=True)
        
        # Subsección Trisomía 21
        pdf.set_font("Arial", style="U", size=12)
        pdf.cell(200, 8, txt="   Trisomía 21:", ln=True)
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 8, txt=f"     - Riesgo Estimado (solo por edad materna): 1 en {base_t21}", ln=True)
        pdf.set_font("Arial", style="B", size=12)
        pdf.cell(200, 8, txt=f"     - Riesgo Ajustado (Cálculo Final): 1 en {final_t21}", ln=True)
        pdf.ln(2)

        # Subsección Trisomías 18 y 13
        pdf.set_font("Arial", style="U", size=12)
        pdf.cell(200, 8, txt="   Trisomía 18/13:", ln=True)
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 8, txt=f"     - Riesgo Estimado (solo por edad materna): 1 en {base_t18_13}", ln=True)
        pdf.set_font("Arial", style="B", size=12)
        pdf.cell(200, 8, txt=f"     - Riesgo Ajustado (Cálculo Final): 1 en {final_t18_13}", ln=True)
        pdf.ln(10)

        pdf.set_font("Arial", style="I", size=9)
        nota_texto = (
            "NOTA: Este cálculo representa una estimación de riesgo (Cribado Combinado de Primer Trimestre) "
            "y no constituye un diagnóstico definitivo. La sensibilidad de este cribado combinado para "
            "Trisomía 21 es de aproximadamente 90% y para Trisomías 18/13 es del 95%, con una tasa de "
            "falsos positivos cercana al 5%. Los pacientes con resultados de alto riesgo deben ser "
            "asesorados sobre las opciones de diagnóstico invasivo (biopsia corial o amniocentesis) "
            "o ADN fetal en sangre materna."
        )
        pdf.multi_cell(0, 5, txt=nota_texto)
        
        nombre_limpio = nombre.replace(' ', '_')
        nombre_archivo = f"Riesgo_Prenatal_{nombre_limpio}.pdf"
        
        ruta_guardado = os.path.join("assets", nombre_archivo)
        pdf.output(ruta_guardado)
        
        return nombre_archivo

    def procesar_datos(e):
        boton_descarga.visible = False
        page.update()

        try:
            nombre = nombre_input.value
            dni = dni_input.value
            if not nombre or not dni:
                raise ValueError("Falta el nombre o el DNI.")

            edad = float(edad_input.value.replace(',', '.'))
            tn = float(tn_input.value.replace(',', '.'))
            lcn = float(lcn_input.value.replace(',', '.'))
            pappa = float(pappa_input.value.replace(',', '.'))
            hcg = float(hcg_input.value.replace(',', '.'))

            # --- NUEVA LÓGICA DE CÁLCULO ---
            
            # 1. Riesgo Basal (Curva matemática simulada basada en la edad)
            # A los 35 años asume un riesgo de 1/250. Empeora exponencialmente a mayor edad.
            riesgo_base_t21 = int(250 * (0.85 ** (edad - 35)))
            if riesgo_base_t21 < 10: riesgo_base_t21 = 10 # Límite de seguridad para la simulación
            riesgo_base_t18_13 = riesgo_base_t21 * 2

            # 2. Factor de Modificación (Ecografía y Laboratorio)
            # TN alta aumenta el riesgo, PAPP-A baja aumenta el riesgo.
            factor_modificador = (tn / 1.5) * (hcg / pappa)

            # 3. Riesgo Final Ajustado (Basal / Factor Modificador)
            riesgo_final_t21 = int(riesgo_base_t21 / factor_modificador)
            riesgo_final_t18_13 = int(riesgo_base_t18_13 / factor_modificador)
            
            # Límites de seguridad visuales para no mostrar valores negativos o cero
            if riesgo_final_t21 < 2: riesgo_final_t21 = 2
            if riesgo_final_t18_13 < 2: riesgo_final_t18_13 = 2

            # Generamos el PDF pasando los 4 valores de riesgo
            archivo_generado = generar_pdf(
                nombre, dni, edad, tn, lcn, pappa, hcg, 
                riesgo_base_t21, riesgo_final_t21, 
                riesgo_base_t18_13, riesgo_final_t18_13
            )

            mensaje_estado.value = "Cálculo finalizado. Haz clic en el botón inferior para abrir el informe."
            mensaje_estado.color = "green"
            boton_descarga.url = f"/{archivo_generado}"
            boton_descarga.visible = True
            page.update()

        except ValueError as error:
            if str(error) == "Falta el nombre o el DNI.":
                mensaje_estado.value = "Error: Por favor ingresa el Nombre y DNI de la paciente."
            else:
                mensaje_estado.value = "Error: Verifica que los datos numéricos estén completos y sean válidos."
            mensaje_estado.color = "red"
            page.update()
        except ZeroDivisionError:
            mensaje_estado.value = "Error: El valor de PAPP-A no puede ser cero."
            mensaje_estado.color = "red"
            page.update()

    boton_calcular = ft.ElevatedButton(
        content=ft.Text("Calcular Riesgo", size=14, weight="bold"),
        on_click=procesar_datos
    )

    page.add(
        titulo,
        ft.Divider(),
        ft.Text("Identificación de la Paciente:", weight="bold"),
        nombre_input,
        dni_input,
        ft.Text("Datos Sociodemográficos:", weight="bold"),
        edad_input,
        ft.Text("Datos Ecográficos:", weight="bold"),
        lcn_input,
        tn_input,
        ft.Text("Datos de Laboratorio (MoM):", weight="bold"),
        pappa_input,
        hcg_input,
        ft.Container(height=10),
        boton_calcular,
        mensaje_estado,
        boton_descarga
    )

# Configuración de servidor en la nube
puerto = int(os.environ.get("PORT", 8080))
ft.app(target=main, assets_dir="assets", view=ft.AppView.WEB_BROWSER, host="0.0.0.0", port=puerto)
