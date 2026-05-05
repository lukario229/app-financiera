import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime

# Configuración de la página
st.set_page_config(page_title="Analizador Financiero - UAN", page_icon="📊", layout="wide")

# --- ESTILOS PERSONALIZADOS (CSS) ---
st.markdown(f"""
    <style>
    /* 1. CUADRO DE MÉTRICA EN NEGRO Y TEXTO BLANCO */
    [data-testid="stMetric"] {{
        background-color: #000000 !important;
        padding: 20px;
        border-radius: 10px;
        border: 1px solid #333333;
        box-shadow: 0 4px 6px rgba(0,0,0,0.3);
    }}
    
    [data-testid="stMetricValue"], [data-testid="stMetricLabel"] {{
        color: #ffffff !important;
    }}

    /* 2. CUADRO DE OPINIÓN TRANSPARENTE */
    .stAlert {{
        background-color: transparent !important;
        border: none !important;
        padding: 0px !important;
    }}
    
    .stAlert p {{
        color: #ffffff !important; 
        font-size: 1.1rem;
        font-weight: 500;
    }}

    /* Estilo general y marca de agua */
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
        background-color: rgba(17, 24, 39, 0.8);
        color: #ffffff;
        text-align: center;
        padding: 10px;
        font-size: 12px;
        z-index: 100;
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
    # Columnas para alinear logo y título a la izquierda
    col_logo, col_titulo = st.columns([1, 6])
    with col_titulo:
        st.title("🛡️ SISTEMA DE INTELIGENCIA FINANCIERA")
        st.subheader("Bienvenido, esta página ha sido creada para ayudar a empresarios como usted.")
        st.caption("Proyecto de Tecnología de la Información e Innovación Digital - Universidad Autónoma de Nayarit")

# --- MÓDULOS DEL PROGRAMA ---

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
        fig = px.pie(names=['Utilidad', 'Costos'], values=[utilidad, ingresos-utilidad], hole=0.4)
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
        if fcf > 0: st.markdown("✅ **Excedente de efectivo detectado.**")
        else: st.markdown("⚠️ **Consumo de efectivo superior a la generación.**")
    with col2:
        fig = go.Figure(go.Waterfall(
            name = "Flujo", orientation = "v",
            measure = ["relative", "relative", "total"],
            x = ["Op. Entradas", "Inversión (Salida)", "Flujo Libre"],
            textposition = "outside",
            text = [f"+{f_operativo}", f"-{capex}", f"{fcf}"],
            y = [f_operativo, -capex, 0],
            connector = {"line":{"color":"rgb(63, 63, 63)"}},
        ))
        fig.update_layout(title="Análisis de Movimiento de Efectivo", template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
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
        fig = go.Figure(go.Indicator(mode="gauge+number", value=roe, title={'text': "Retorno sobre Capital %"}))
        fig.update_layout(template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)')
        st.plotly_chart(fig, use_container_width=True)

def modulo_pe():
    st.header("🎯 Punto de Equilibrio")
    col1, col2 = st.columns([1, 1.5])
    with col1:
        f = st.number_input("Costos Fijos ($)", min_value=0.0, value=2000.0)
        p = st.number_input("Precio ($)", min_value=0.1, value=100.0)
        v = st.number_input("Costo Variable ($)", min_value=0.0, value=60.0)
        if p > v:
            pe = f / (p - v)
            st.metric("Unidades para Equilibrio", f"{int(pe + 1)}")
        else:
            st.error("El precio debe ser mayor al costo variable.")
            pe = 0
    with col2:
        if pe > 0:
            unidades = list(range(0, int(pe * 2) + 10))
            ingresos = [p * u for u in unidades]
            costos = [f + (v * u) for u in unidades]
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=unidades, y=ingresos, name="Ingresos Totales", line=dict(color='#00ff00', width=3)))
            fig.add_trace(go.Scatter(x=unidades, y=costos, name="Costos Totales", line=dict(color='#ff4b4b', width=3)))
            fig.add_trace(go.Scatter(x=[pe], y=[p*pe], mode='markers', name='Punto de Equilibrio', marker=dict(color='white', size=12, symbol='star')))
            fig.update_layout(title="Gráfica de Punto de Equilibrio", template="plotly_dark", paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig, use_container_width=True)

# --- ESTRUCTURA PRINCIPAL ---
mostrar_cabecera()
st.divider()

with st.sidebar:
    # Logo también en el sidebar
    st.image("https://uacbi.uan.mx/wp-content/uploads/2022/10/ESCUDO-UAN-Azul-1024x1024.png", width=250)
    st.title("Menú Principal")
    opcion = st.radio("Seleccione un Módulo:", ["Balance General", "Estado de Resultados", "Flujos de Efectivo", "Capital Contable", "Punto de Equilibrio"])
    st.divider()
    st.markdown(" 📜 IMPORTANTE")
    st.caption("Este sistema procesa datos de manera local. Recuerde que la confidencialidad de su información financiera es un derecho protegido por la Ley Federal de Protección de Datos Personales.")
    st.caption("Cálculos basados en estándares internacionales de contabilidad y modelos matemáticos de álgebra lineal.")
    st.caption("Versión del Sistema: v1.0 - Desarrollado para la materia Contabilidad Empresarial.")

# Renderizado
if opcion == "Balance General": modulo_balance()
elif opcion == "Estado de Resultados": modulo_resultados()
elif opcion == "Flujos de Efectivo": modulo_flujos()
elif opcion == "Capital Contable": modulo_capital()
elif opcion == "Punto de Equilibrio": modulo_pe()

# Pie de página
st.markdown(f"""
    <div class="footer">
        © {datetime.now().year} Derechos Reservados - <b>Heliu</b> | UAN - Tecnología de la Información
    </div>
    """, unsafe_allow_html=True)