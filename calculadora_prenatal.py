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
    # Habilita el desplazamiento en pantallas de teléfonos móviles
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

    def generar_pdf(nombre, dni, edad, tn, lcn, pappa, hcg, riesgo_t21, riesgo_t18_13):
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
        
        pdf.set_font("Arial", style="B", size=12)
        pdf.cell(200, 10, txt="3. Índices de Riesgo Calculados:", ln=True)
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 8, txt=f"   - Riesgo Trisomía 21: 1 en {riesgo_t21}", ln=True)
        pdf.cell(200, 8, txt=f"   - Riesgo Trisomía 18/13: 1 en {riesgo_t18_13}", ln=True)
        pdf.ln(15)

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

            factor_riesgo = (edad / 20) * (tn / 1.5) * (hcg / pappa)
            riesgo_t21_calculado = int(1000 / factor_riesgo) 
            riesgo_t18_13_calculado = int(2000 / factor_riesgo)

            archivo_generado = generar_pdf(
                nombre, dni, edad, tn, lcn, pappa, hcg, 
                riesgo_t21_calculado, riesgo_t18_13_calculado
            )

            # Lanza la URL de descarga forzando una pestaña nueva
            page.launch_url(f"/{archivo_generado}", web_window_name="_blank")

            mensaje_estado.value = "¡Éxito! El documento se ha generado y abierto en una nueva pestaña."
            mensaje_estado.color = "green"
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
        content=ft.Text("Generar y Descargar PDF", size=14, weight="bold"),
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
        mensaje_estado
    )

# Configuración de servidor en la nube
puerto = int(os.environ.get("PORT", 8080))
ft.app(target=main, assets_dir="assets", view=ft.AppView.WEB_BROWSER, host="0.0.0.0", port=puerto)
