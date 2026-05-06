import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime

# Configuración de la página
st.set_page_config(page_title="Analizador Financiero - UAN", page_icon="📊", layout="wide")

# --- ESTILOS PERSONALIZADOS (CSS) ---
st.markdown(f"""
    <style>
    [data-testid="stMetric"] {{
        background-color: #0e1117 !important;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #333333;
    }}
    
    [data-testid="stMetricValue"], [data-testid="stMetricLabel"] {{
        color: #ffffff !important;
    }}

    .stAlert {{
        background-color: transparent !important;
        border: none !important;
    }}

    .watermark-bg {{
        position: fixed;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%) rotate(-45deg);
        font-size: 80px;
        color: rgba(220, 220, 220, 0.05);
        z-index: -1;
        white-space: nowrap;
        user-select: none;
    }}
    
    .footer {{
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: rgba(17, 24, 39, 0.95);
        color: #ffffff;
        text-align: center;
        padding: 15px;
        font-size: 11px;
        z-index: 100;
        border-top: 1px solid #333;
    }}
    </style>
    <div class="watermark-bg">© Heliu - UAN 2026</div>
    """, unsafe_allow_html=True)

# --- FUNCIONES DE SOPORTE ---
def generar_opinion(valor, tipo):
    if tipo == "liquidez":
        if valor >= 1.5: return "🟢 **Situación Óptima:** Solvencia garantizada."
        if valor >= 1.0: return "🟡 **Riesgo Moderado:** Vigilancia requerida."
        return "🔴 **Alerta Crítica:** Insuficiencia de fondos inmediata."
    if tipo == "margen":
        if valor >= 20: return "🟢 **Alta Rentabilidad:** Generación eficiente de valor."
        return "🔴 **Rentabilidad Baja:** Revisar estructura de costos."
    if tipo == "roe":
        if valor >= 15: return "🟢 **Excelente Retorno:** Gran eficiencia en el uso del capital."
        return "🟡 **Retorno Moderado:** Se sugiere optimizar la inversión patrimonial."

def mostrar_cabecera():
    col_logo, col_titulo = st.columns([1, 6])
    with col_titulo:
        st.title("🛡️ SISTEMA DE INTELIGENCIA FINANCIERA")
        st.subheader("Análisis Estratégico para la Toma de Decisiones")
        st.caption("Proyecto de Innovación Digital - Universidad Autónoma de Nayarit")

# --- MÓDULOS DE ANÁLISIS ---

def modulo_balance():
    st.header("⚖️ Balance General")
    col1, col2 = st.columns([1, 1])
    with col1:
        activo = st.number_input("Activo Circulante ($)", min_value=0.0, value=1500.0)
        pasivo = st.number_input("Pasivo Circulante ($)", min_value=0.0, value=1000.0)
        if pasivo > 0:
            liq = activo / pasivo
            st.metric("Razón de Liquidez", f"{liq:.2f}")
            st.info(generar_opinion(liq, "liquidez"))
    with col2:
        fig = go.Figure(go.Bar(x=['Activos', 'Pasivos'], y=[activo, pasivo], marker_color=['#1a4a7a', '#c0392b']))
        fig.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)

def modulo_resultados():
    st.header("📈 Estado de Resultados")
    col1, col2 = st.columns([1, 1])
    with col1:
        ingresos = st.number_input("Ingresos Totales ($)", min_value=0.0, value=5000.0)
        utilidad = st.number_input("Utilidad Neta ($)", min_value=0.0, value=1000.0)
        if ingresos > 0:
            margen = (utilidad / ingresos) * 100
            st.metric("Margen Neto", f"{margen:.2f}%")
            st.info(generar_opinion(margen, "margen"))
    with col2:
        fig = px.pie(names=['Utilidad', 'Costos'], values=[utilidad, max(0, ingresos-utilidad)], hole=0.4)
        fig.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)

def modulo_flujos():
    st.header("💸 Flujos de Efectivo")
    col1, col2 = st.columns([1, 1])
    with col1:
        f_operativo = st.number_input("Flujo Actividades Operación ($)", value=3000.0)
        capex = st.number_input("Inversión (CAPEX) ($)", value=1200.0)
        fcf = f_operativo - capex
        st.metric("Flujo Libre de Efectivo", f"${fcf:,.2f}")
    with col2:
        fig = go.Figure(go.Waterfall(
            name = "Flujo", orientation = "v",
            measure = ["relative", "relative", "total"],
            x = ["Op. Entradas", "Inversión", "Flujo Libre"],
            y = [f_operativo, -capex, 0],
        ))
        fig.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)

def modulo_capital():
    st.header("🏢 Estado de Capital Contable")
    col1, col2 = st.columns([1, 1])
    with col1:
        utilidad_n = st.number_input("Utilidad Neta ($)", min_value=0.0, value=1000.0)
        capital_t = st.number_input("Capital Contable ($)", min_value=1.0, value=5000.0)
        roe = (utilidad_n / capital_t) * 100
        st.metric("ROE", f"{roe:.2f}%")
        st.info(generar_opinion(roe, "roe"))
    with col2:
        fig = go.Figure(go.Indicator(mode="gauge+number", value=roe, gauge={'axis': {'range': [None, 40]}}))
        fig.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)

def modulo_pe():
    st.header("🎯 Punto de Equilibrio (Básico)")
    col1, col2 = st.columns([1, 1])
    with col1:
        f = st.number_input("Costos Fijos ($)", min_value=0.0, value=2000.0)
        p = st.number_input("Precio ($)", min_value=0.1, value=100.0)
        v = st.number_input("Costo Variable ($)", min_value=0.0, value=60.0)
        if p > v:
            pe = f / (p - v)
            st.metric("Unidades para Equilibrio", f"{int(pe + 1)}")
        else:
            st.error("El precio debe ser mayor al costo variable.")

def modulo_escenario_mixto():
    st.header("🚀 SIMULADOR DE ESCENARIOS DINÁMICOS")

    col_inp, col_res = st.columns([1, 1.5])

    with col_inp:
        st.subheader("⚙️ Parámetros")
        pv_base = st.number_input("Precio de Venta Base ($)", min_value=0.0, value=1300.0)
        extra_premium = st.number_input("Ingreso Adicional / Plus ($)", min_value=0.0, value=70.0)
        cv_u = st.number_input("Costo Variable Unitario ($)", min_value=0.0, value=200.0)
        cf_total = st.number_input("Costos Fijos Totales ($)", min_value=0.0, value=15000.0)

        pv_final = pv_base + extra_premium
        mc_calculado = pv_final - cv_u

        st.divider()
        utilidad_deseada = st.number_input("Utilidad Neta Objetivo ($)", min_value=0.0, value=30000.0)

        # Guía manual con instrucciones agregadas
        with st.expander("📖 Guía de Cálculo Manual"):
            datos_manuales = {
                "Concepto": ["PV Final", "Margen (MC)", "PE", "Ventas Meta"],
                "Fórmula": ["Base+Plus", "PV-CV", "Fijos/MC", "(Fijos+Meta)/MC"],
                "Resultado": [
                    f"**${pv_final}**",
                    f"**${mc_calculado}**",
                    f"**{cf_total/mc_calculado if mc_calculado > 0 else 0:.2f}**",
                    f"**{(cf_total+utilidad_deseada)/mc_calculado if mc_calculado > 0 else 0:.2f}**"
                ]
            }
            st.table(datos_manuales)
            
            # --- SECCIÓN DE INSTRUCCIONES ---
            st.write("") # Espacio de separación
            st.divider()
            st.markdown("### 📝 Glosario Rápido")
            st.caption("Usa esta guía para entender tus resultados de forma sencilla:")
            
            st.info("""
            *   **PV Final:** Es tu precio real de venta (Base + cobros extras).
            *   **Margen (MC):** Lo que te sobra de cada venta tras pagar sus costos directos.
            *   **Punto de Equilibrio (PE):** ¿Cuántos clientes necesitas para no ganar ni perder?
            *   **Ventas Meta:** Clientes necesarios para alcanzar la utilidad que escribiste arriba.
            """)

    with col_res:
        st.subheader("📊 Resultados Proyectados")
        m1, m2, m3 = st.columns(3)
        m1.metric("PV Final", f"${pv_final:,.2f}")
        m2.metric("Margen (MC)", f"${mc_calculado:,.2f}")

        if mc_calculado > 0:
            pe_q = cf_total / mc_calculado
            m3.metric("P.E. (Clientes)", f"{int(pe_q + 1)}")

            clientes_necesarios = (cf_total + utilidad_deseada) / mc_calculado
            st.success(f"### 🎯 Objetivo: {int(clientes_necesarios + 1)} Clientes")

            st.divider()
            clientes_reales = st.slider("Simular Volumen de Ventas (Clientes)", 0, int(clientes_necesarios * 1.5), int(pe_q + 5))
            utilidad_proyectada = (clientes_reales * mc_calculado) - cf_total

            st.metric("Utilidad Proyectada", f"${utilidad_proyectada:,.2f}", 
                      delta=f"{utilidad_proyectada - utilidad_deseada:,.2f} vs Meta")

            fig = px.area(x=list(range(0, int(clientes_necesarios * 1.3))), 
                          y=[(x * mc_calculado) - cf_total for x in range(0, int(clientes_necesarios * 1.3))], 
                          labels={'x': 'Clientes', 'y': 'Utilidad ($)'}, title="Curva de Rentabilidad")
            fig.add_hline(y=0, line_dash="dash", line_color="red")
            fig.add_hline(y=utilidad_deseada, line_dash="dot", line_color="green")
            fig.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.error("⚠️ El Costo Variable supera al Precio. Revisa tus números.")

# --- ESTRUCTURA PRINCIPAL ---
mostrar_cabecera()
st.divider()

with st.sidebar:
    st.image("https://uacbi.uan.mx/wp-content/uploads/2022/10/ESCUDO-UAN-Azul-1024x1024.png", width=200)
    st.title("Menú de Análisis")
    opcion = st.radio("Seleccione un Módulo:", [
        "Balance General", "Estado de Resultados", "Flujos de Efectivo", 
        "Capital Contable", "Punto de Equilibrio", "Escenario Mixto"
    ])
    st.divider()
    st.caption("Este sistema procesa datos de manera local. Recuerde que la confidencialidad de su información financiera es un derecho protegido por la Ley Federal de Protección de Datos Personales.")
    st.caption("Cálculos basados en estándares internacionales de contabilidad y modelos matemáticos de álgebra lineal.")
    st.caption("Versión del Sistema: v1.0 - Desarrollado para la materia Contabilidad Empresarial.")

# NAVEGACIÓN
if opcion == "Balance General": modulo_balance()
elif opcion == "Estado de Resultados": modulo_resultados()
elif opcion == "Flujos de Efectivo": modulo_flujos()
elif opcion == "Capital Contable": modulo_capital()
elif opcion == "Punto de Equilibrio": modulo_pe()
elif opcion == "Escenario Mixto": modulo_escenario_mixto()

st.markdown(f"""
    <div class="footer">
        <b>© {datetime.now().year} | Heliu Gahel Ciañez | Universidad Autónoma de Nayarit</b><br>
        <i>Tecnologías de la Información - Área de Contabilidad Empresarial</i>
    </div>
    """, unsafe_allow_html=True)
