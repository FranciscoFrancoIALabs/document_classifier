# prompts/base_prompts.py
# 🧠 Prompts centrales para clasificadores
# Versión detallada y optimizada para clasificación documental multimodal

PROMPT_TEXT_CLASSIFICATION = (
    "=== INSTRUCCIÓN ===\n"
    "CLASIFICA este documento en UNA de las siguientes categorías específicas:\n\n"

    "=== CATEGORÍAS VÁLIDAS ===\n"
    "(Usa EXACTAMENTE estos nombres, sin tildes ni variaciones de mayúsculas)\n"
    "- 'Resolucion' → documentos legales, resoluciones administrativas\n"
    "- 'Plano' → planos prediales, cartográficos o topográficos\n"
    "- 'Escritura' → documentos notariales, contratos o títulos de propiedad\n"
    "- 'Croquis' → dibujos simples, bosquejos o diagramas\n"
    "- 'Documento de Apoyo' → tablas, listados, bases de datos o informes\n"
    "- 'Otros' → cualquier otro tipo no cubierto\n\n"

    "=== PALABRAS CLAVE Y SEÑALES ===\n\n"

    "Resolucion:\n"
    "- 'RESOLUCIÓN', 'DECRETO', 'ACUERDO', 'ACTA', 'EXPEDIENTE', 'PROCEDIMIENTO'\n"
    "- 'ARTÍCULO', 'PARÁGRAFO', 'CONSIDERANDO', 'RESUELVE', 'ADMINISTRATIVO'\n"
    "- 'MINISTERIO', 'AGENCIA', 'SUBDIRECCIÓN', 'DIRECCIÓN', 'OFICIAL'\n"
    "- Formato legal con numeración de artículos y considerandos\n\n"

    "Plano:\n"
    "- 'PLANO', 'PREDIAL', 'CATASTRAL', 'TOPOGRAFÍA', 'CARTOGRAFÍA'\n"
    "- 'COORDENADAS', 'LINDEROS', 'LÍMITES', 'NORTE', 'SUR', 'ESTE', 'OESTE'\n"
    "- 'ESCALA', 'LEVANTAMIENTO', 'GEOREFERENCIACIÓN', 'LATITUD', 'LONGITUD'\n"
    "- 'ÁREA', 'PERÍMETRO', 'MTS', 'HECTÁREAS', 'METROS CUADRADOS'\n"
    "- Contiene coordenadas, medidas o escalas gráficas\n\n"

    "Escritura:\n"
    "- 'ESCRITURA', 'NOTARÍA', 'NOTARIAL', 'CONTRATO', 'COMPRAVENTA'\n"
    "- 'PROPIEDAD', 'DOMINIO', 'REGISTRO', 'INSCRIPCIÓN', 'FOLIO'\n"
    "- 'HEREDEROS', 'CESIÓN', 'TRANSFERENCIA', 'TÍTULO DE PROPIEDAD'\n"
    "- Formato notarial con firmas y sellos oficiales\n\n"

    "Croquis:\n"
    "- 'CROQUIS', 'BOSQUEJO', 'ESQUEMA', 'DIAGRAMA', 'BOCETO'\n"
    "- 'DIBUJO', 'TRAZADO', 'BORRADOR', 'MAQUETA', 'PROTOTIPO'\n"
    "- Representaciones simples sin escala precisa\n\n"

    "Documento de Apoyo:\n"
    "- 'TABLA', 'LISTADO', 'INVENTARIO', 'CATÁLOGO', 'BASE DE DATOS'\n"
    "- 'INFORME', 'ANÁLISIS', 'ESTADÍSTICA', 'DATOS', 'REGISTROS'\n"
    "- 'EXCEL', 'HOJA DE CÁLCULO', 'COLUMNAS', 'FILAS', 'CELDAS'\n"
    "- Estructura tabular o datos numéricos organizados\n\n"

    "=== REGLAS DE CLASIFICACIÓN ===\n"
    "1️⃣ Prioriza palabras clave explícitas ('RESOLUCIÓN', 'PLANO', 'ESCRITURA', etc.).\n"
    "2️⃣ Si hay 'RESOLUCIÓN', casi siempre es 'Resolucion'.\n"
    "3️⃣ Si hay 'PLANO', casi siempre es 'Plano'.\n"
    "4️⃣ Si hay 'ESCRITURA', casi siempre es 'Escritura'.\n"
    "5️⃣ Si tiene estructura legal (artículos, considerandos) → 'Resolucion'.\n"
    "6️⃣ Si es principalmente visual con coordenadas → 'Plano'.\n\n"

    "=== FORMATO Y REGLAS DE SALIDA ===\n"
    "- Usa EXACTAMENTE los nombres de categoría definidos.\n"
    "- No uses tildes, mayúsculas diferentes ni espacios extra.\n\n"

    "=== EJEMPLOS CONCRETOS ===\n"
    "- 'RESOLUCIÓN No. 202342001490026' → Resolucion\n"
    "- 'PLANO PREDIAL' con coordenadas → Plano\n"
    "- Contrato de compraventa notariado → Escritura\n"
    "- Dibujo simple de distribución → Croquis\n"
    "- Archivo Excel con registros o precios → Documento de Apoyo\n\n"

    "=== INSTRUCCIÓN FINAL ===\n"
    "Analiza el documento con base en las palabras clave y señales.\n"
    "RESPONDE solo con el nombre de la categoría y una breve explicación razonada."
)

PROMPT_IMAGE_CLASSIFICATION = (
    "Eres un asistente experto en clasificación documental. "
    "Analiza visualmente la imagen del documento y clasifícala en UNA de las siguientes categorías: "
    "Resolucion, Plano, Escritura, Croquis, Documento de Apoyo u Otros. "
    "Explica brevemente las razones de tu decisión basándote en su estructura visual, texto visible y formato."
)
