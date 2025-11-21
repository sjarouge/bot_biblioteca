"""
BOT Biblioteca W2M - Asistente de Consulta de Biblioteca SAP ABAP
Desarrollado para W2M - Santiago Jarouge
"""

import streamlit as st
import os
import sys
from pathlib import Path
from typing import List, Dict, Tuple

# Manejo seguro de __file__ para Streamlit Cloud
try:
    if __file__:
        SCRIPT_DIR = Path(__file__).parent.absolute()
    else:
        SCRIPT_DIR = Path.cwd() / 'bot_biblioteca'
except:
    SCRIPT_DIR = Path.cwd() / 'bot_biblioteca'

# Configuración de la página
st.set_page_config(
    page_title="BOT Biblioteca W2M",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Título principal
st.title("📚 BOT Biblioteca W2M")
st.markdown("**Asistente inteligente para consultar la biblioteca de programas SAP ABAP**")
st.markdown("---")

# Inicializar variables de sesión
if 'knowledge_base' not in st.session_state:
    st.session_state.knowledge_base = None
if 'indexed_files' not in st.session_state:
    st.session_state.indexed_files = 0  # Cambiado de [] a 0 (entero)
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []


def load_text_file(file_path: Path) -> str:
    """Carga el contenido de un archivo de texto"""
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            return f.read()
    except Exception as e:
        return f"Error al leer archivo: {str(e)}"


def index_library(base_path: str) -> Tuple[Dict, int]:
    """Indexa todos los archivos de la biblioteca"""
    base = Path(base_path)
    knowledge_base = {
        'files': [],
        'programs': {},
        'documentation': {},
        'structure': {}
    }
    
    indexed_count = 0
    
    # Verificar que la ruta existe
    if not base.exists():
        raise FileNotFoundError(f"La ruta {base_path} no existe")
    
    # Archivo principal - BIBLIOTECA_W2M_CONOCIMIENTO_BOT.txt (muy importante)
    main_file = base / 'BIBLIOTECA_W2M_CONOCIMIENTO_BOT.txt'
    if main_file.exists():
        content = load_text_file(main_file)
        knowledge_base['files'].append({
            'path': 'BIBLIOTECA_W2M_CONOCIMIENTO_BOT.txt',
            'content': content,
            'type': 'documentation'
        })
        indexed_count += 1
        # Este archivo es tan completo que podemos extraer información de programas de él
        _extract_programs_from_knowledge_file(content, knowledge_base)
    
    # Archivos adicionales opcionales
    additional_files = [
        'README_NUEVA_ESTRUCTURA.md',
        'ESTRUCTURA_BIBLIOTECA_ORGANIZADA.md',
        'INDICE_BIBLIOTECA_ORGANIZADA.md'
    ]
    
    # Indexar archivos adicionales si existen
    for filename in additional_files:
        file_path = base / filename
        if file_path.exists():
            content = load_text_file(file_path)
            knowledge_base['files'].append({
                'path': filename,
                'content': content,
                'type': 'documentation'
            })
            indexed_count += 1
    
    # Indexar documentación técnica (opcional - solo si existe)
    doc_path = base / '07_Documentacion_Tecnica'
    if doc_path.exists():
        for file_path in doc_path.rglob('*.md'):
            try:
                content = load_text_file(file_path)
                rel_path = str(file_path.relative_to(base))
                knowledge_base['documentation'][rel_path] = content
                knowledge_base['files'].append({
                    'path': rel_path,
                    'content': content,
                    'type': 'documentation'
                })
                indexed_count += 1
            except Exception as e:
                continue
    
    # Indexar archivos de programas (opcional - solo si existe la carpeta)
    programs_path = base / '01_Programas_Principales'
    if programs_path.exists():
        for file_path in programs_path.rglob('*.txt'):
            # Solo archivos principales (no includes)
            if '_top.txt' in file_path.name or '_sel.txt' in file_path.name or '_lcl.txt' in file_path.name:
                continue
            if file_path.name.endswith('_top.txt') or file_path.name.endswith('_sel.txt'):
                continue
            
            # Solo archivos principales del programa
            if not any(suffix in file_path.name for suffix in ['_top', '_sel', '_lcl', '_eve', '_f01', '_mod']):
                try:
                    content = load_text_file(file_path)
                    program_name = file_path.stem.upper()
                    knowledge_base['programs'][program_name] = {
                        'path': str(file_path.relative_to(base)),
                        'content': content[:5000],  # Primeros 5000 caracteres
                        'folder': str(file_path.parent.relative_to(base))
                    }
                    indexed_count += 1
                except Exception as e:
                    continue
    
    # Indexar reports (opcional - solo si existe la carpeta)
    reports_path = base / '02_Reports'
    if reports_path.exists():
        for folder in reports_path.iterdir():
            if folder.is_dir():
                main_file = folder / f"{folder.name}.txt"
                if main_file.exists():
                    try:
                        content = load_text_file(main_file)
                        program_name = folder.name.upper()
                        knowledge_base['programs'][program_name] = {
                            'path': str(main_file.relative_to(base)),
                            'content': content[:5000],
                            'folder': str(folder.relative_to(base))
                        }
                        indexed_count += 1
                    except Exception as e:
                        continue
    
    return knowledge_base, indexed_count


def _extract_programs_from_knowledge_file(content: str, knowledge_base: Dict):
    """Extrae información de programas del archivo BIBLIOTECA_W2M_CONOCIMIENTO_BOT.txt"""
    import re
    
    # Buscar nombres de programas (patrones como ZFI_*, ZFIR*, etc.)
    program_patterns = [
        r'\b(ZFI[A-Z_0-9]+)\b',
        r'\b(ZFIR[A-Z_0-9]+)\b',
        r'\b(ZFII[A-Z_0-9]+)\b',
        r'\b(ZARR[A-Z_0-9]+)\b',
        r'\b(ZUTR[A-Z_0-9]+)\b',
        r'\b(ZCL_[A-Z_0-9]+)\b',
    ]
    
    found_programs = set()
    for pattern in program_patterns:
        matches = re.findall(pattern, content, re.IGNORECASE)
        found_programs.update(m.upper() for m in matches)
    
    # Extraer información contextual de cada programa
    for program_name in found_programs:
        # Buscar secciones que mencionen este programa
        program_sections = []
        lines = content.split('\n')
        current_section = []
        in_program_section = False
        
        for i, line in enumerate(lines):
            if program_name.upper() in line.upper():
                in_program_section = True
                # Capturar contexto alrededor (10 líneas antes y después)
                start = max(0, i - 10)
                end = min(len(lines), i + 10)
                context = '\n'.join(lines[start:end])
                program_sections.append(context)
        
        if program_sections:
            # Combinar toda la información del programa
            program_info = '\n'.join(program_sections)
            knowledge_base['programs'][program_name] = {
                'path': f'BIBLIOTECA_W2M_CONOCIMIENTO_BOT.txt',
                'content': program_info[:5000],  # Primeros 5000 caracteres
                'folder': 'Biblioteca Principal'
            }


def search_in_content(query: str, knowledge_base: Dict) -> List[Dict]:
    """Busca el query en todo el contenido indexado"""
    query_lower = query.lower()
    query_words = set(query_lower.split())
    
    results = []
    
    # Buscar en archivos de documentación
    for file_info in knowledge_base.get('files', []):
        content = file_info.get('content', '').lower()
        path = file_info.get('path', '')
        
        # Calcular relevancia
        word_matches = sum(1 for word in query_words if word in content)
        exact_match = query_lower in content
        
        if word_matches > 0 or exact_match:
            # Extraer contexto relevante
            context = extract_context(content, query_lower, 200)
            relevance = word_matches * 2 + (10 if exact_match else 0)
            
            results.append({
                'type': 'documentation',
                'path': path,
                'content': context,
                'relevance': relevance,
                'full_content': file_info.get('content', '')
            })
    
    # Buscar en programas
    for program_name, program_info in knowledge_base.get('programs', {}).items():
        content = program_info.get('content', '').lower()
        path = program_info.get('path', '')
        folder = program_info.get('folder', '')
        
        # Buscar en nombre del programa
        name_match = query_lower in program_name.lower()
        content_match = any(word in content for word in query_words)
        
        if name_match or content_match:
            context = extract_context(content, query_lower, 200)
            relevance = (20 if name_match else 0) + (word_matches if content_match else 0)
            
            results.append({
                'type': 'program',
                'name': program_name,
                'path': path,
                'folder': folder,
                'content': context,
                'relevance': relevance,
                'full_content': program_info.get('content', '')
            })
    
    # Ordenar por relevancia
    results.sort(key=lambda x: x['relevance'], reverse=True)
    return results[:10]  # Top 10 resultados


def extract_context(text: str, query: str, context_size: int = 200) -> str:
    """Extrae el contexto alrededor de la búsqueda"""
    text_lower = text.lower()
    query_lower = query.lower()
    
    # Buscar la primera ocurrencia
    idx = text_lower.find(query_lower)
    if idx == -1:
        # Si no hay match exacto, buscar palabras individuales
        words = query_lower.split()
        for word in words:
            idx = text_lower.find(word)
            if idx != -1:
                break
    
    if idx == -1:
        return text[:context_size] + "..."
    
    # Extraer contexto alrededor
    start = max(0, idx - context_size // 2)
    end = min(len(text), idx + len(query) + context_size // 2)
    
    context = text[start:end]
    if start > 0:
        context = "..." + context
    if end < len(text):
        context = context + "..."
    
    return context


def format_response(query: str, results: List[Dict]) -> str:
    """Formatea la respuesta del BOT"""
    if not results:
        return "No encontré información específica sobre tu consulta. Intenta reformular la pregunta o buscar por:\n\n- Nombre de programa (ej: ZFI_BLUEBAY_GET)\n- Funcionalidad (ej: facturas, pagos, Azure)\n- Tipo de programa (ej: reports, interfaces, utilidades)"
    
    response = f"Encontré {len(results)} resultado(s) relevante(s):\n\n"
    
    for i, result in enumerate(results[:5], 1):  # Mostrar top 5
        if result['type'] == 'program':
            response += f"**{i}. Programa: {result['name']}**\n"
            response += f"   📁 Ubicación: `{result['folder']}`\n"
            response += f"   📄 Archivo: `{result['path']}`\n"
        else:
            response += f"**{i}. Documentación: {result['path']}**\n"
        
        # Agregar contexto relevante
        context = result['content']
        if len(context) > 300:
            context = context[:300] + "..."
        response += f"   💡 Contexto: {context}\n\n"
    
    # Agregar sugerencias
    response += "\n---\n"
    response += "**💡 Sugerencias:**\n"
    response += "- Puedes preguntar sobre programas específicos, funcionalidades, o estructura de la biblioteca\n"
    response += "- Ejemplos: '¿Qué programas hay para facturas?', '¿Cómo funciona ZFI_BLUEBAY_GET?', '¿Dónde están los reports?'\n"
    
    return response


def get_suggested_questions() -> List[str]:
    """Retorna preguntas sugeridas"""
    return [
        "¿Qué programas hay para facturas?",
        "¿Cómo funciona la integración con Azure?",
        "¿Qué reports de finanzas existen?",
        "¿Dónde están los programas de BlueBay?",
        "¿Qué utilidades hay disponibles?",
        "¿Cuál es la estructura de la biblioteca?",
        "¿Qué programas hay para República Dominicana?",
        "¿Cómo se procesan los pagos?"
    ]


    # Sidebar
with st.sidebar:
    st.header("⚙️ Configuración")
    
    # Selector de ruta de biblioteca
    st.subheader("📂 Ubicación de la Biblioteca")
    
    # Verificar si ya está indexada
    if st.session_state.indexed_files > 0:
        st.success(f"✅ Biblioteca indexada: {st.session_state.indexed_files} archivos")
        if st.button("🔄 Re-indexar Biblioteca", type="secondary"):
            st.session_state.knowledge_base = None
            st.session_state.indexed_files = 0
            st.rerun()
    else:
        st.info("ℹ️ Primero necesitas indexar la biblioteca para poder hacer consultas")
    
    # Intentar detectar la ruta automáticamente
    try:
        repo_root = SCRIPT_DIR.parent
        
        # En Streamlit Cloud, la ruta típica es /mount/src/
        # Buscar en varias ubicaciones posibles
        possible_paths = [
            repo_root,  # Mismo nivel que bot_biblioteca
            repo_root.parent,  # Un nivel arriba
            Path('/mount/src'),  # Ruta típica de Streamlit Cloud
            Path('/mount/src') / repo_root.name,  # Si bot_biblioteca está en /mount/src/bot_biblioteca
        ]
        
        detected_path = None
        for path in possible_paths:
            if path.exists() and (path / 'BIBLIOTECA_W2M_CONOCIMIENTO_BOT.txt').exists():
                detected_path = str(path)
                break
        
        if detected_path:
            default_path = detected_path
            st.success(f"✅ Biblioteca detectada automáticamente en: `{detected_path}`")
        else:
            # Ruta por defecto para Streamlit Cloud
            # Intentar detectar si estamos en Streamlit Cloud
            if Path('/mount/src').exists():
                # Estamos en Streamlit Cloud
                default_path = "/mount/src"
                st.info("ℹ️ En Streamlit Cloud. Si subiste el archivo a la raíz del repo, usa: `/mount/src`")
            else:
                # Estamos en local
                default_path = str(repo_root)
                st.info(f"ℹ️ Ruta sugerida: `{repo_root}` (ajusta si es necesario)")
    except Exception as e:
        # Ruta por defecto para Streamlit Cloud
        default_path = "/mount/src" if Path('/mount/src').exists() else ""
    
    library_path = st.text_input(
        "Ruta de la biblioteca:",
        value=default_path,
        help="Ruta donde está ubicada la biblioteca W2M. Debe contener el archivo BIBLIOTECA_W2M_CONOCIMIENTO_BOT.txt"
    )
    
    # Mostrar instrucciones
    with st.expander("📖 ¿Cómo obtener la ruta de la biblioteca?"):
        st.markdown("""
        **En Streamlit Cloud:**
        - Si subiste `BIBLIOTECA_W2M_CONOCIMIENTO_BOT.txt` a la **raíz** del repositorio:
          - Usa: `/mount/src`
        - Si está en otra ubicación, ajusta la ruta
        
        **En tu computadora local (Windows):**
        - Copia la ruta completa donde está el archivo
        - Ejemplo: `C:\\Users\\sjaro\\OneDrive\\W2M\\03 Biblioteca`
        - El archivo debe estar en esa carpeta
        
        **Verificar:**
        - El archivo debe llamarse exactamente: `BIBLIOTECA_W2M_CONOCIMIENTO_BOT.txt`
        - Debe estar en la carpeta que indiques en la ruta
        """)
    
    if st.button("🔄 Indexar Biblioteca", type="primary", disabled=not library_path):
        if not library_path:
            st.error("❌ Por favor, ingresa una ruta de biblioteca")
        else:
            with st.spinner("Indexando biblioteca... Esto puede tardar unos segundos"):
                try:
                    kb, count = index_library(library_path)
                    st.session_state.knowledge_base = kb
                    st.session_state.indexed_files = count
                    st.success(f"✅ Biblioteca indexada correctamente: {count} archivos")
                    st.balloons()  # Animación de celebración
                    st.rerun()  # Recargar para mostrar el estado actualizado
                except FileNotFoundError as e:
                    st.error(f"❌ No se encontró la ruta: {str(e)}\n\nVerifica que la ruta sea correcta y que contenga el archivo BIBLIOTECA_W2M_CONOCIMIENTO_BOT.txt")
                except Exception as e:
                    st.error(f"❌ Error al indexar: {str(e)}")
    
    st.markdown("---")
    st.subheader("💡 Preguntas Sugeridas")
    questions = get_suggested_questions()
    for idx, question in enumerate(questions):
        # Usar índice en lugar de hash para evitar problemas
        if st.button(question, key=f"suggest_{idx}", use_container_width=True):
            st.session_state.current_query = question
    
    st.markdown("---")
    st.markdown("**Desarrollado para W2M**")
    st.markdown("Santiago Jarouge")


# Área principal de chat
st.subheader("💬 Consulta la Biblioteca")

# Mostrar historial de chat
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Input de consulta
if 'current_query' in st.session_state:
    query = st.session_state.current_query
    del st.session_state.current_query
else:
    query = st.chat_input("Escribe tu pregunta sobre la biblioteca...")

if query:
    # Agregar pregunta al historial
    st.session_state.chat_history.append({"role": "user", "content": query})
    
    with st.chat_message("user"):
        st.markdown(query)
    
    # Buscar respuesta
    if st.session_state.knowledge_base is None:
        response = """⚠️ **La biblioteca no está indexada aún.**

Para poder hacer consultas, primero necesitas:

1. **Ir a la barra lateral** (← izquierda)
2. **Ingresar la ruta de la biblioteca** (o usar la detectada automáticamente)
3. **Click en "🔄 Indexar Biblioteca"**
4. **Esperar a que termine la indexación**

Una vez indexada, podrás hacer todas las consultas que quieras. 🚀"""
        results = []
    else:
        with st.spinner("Buscando en la biblioteca..."):
            try:
                results = search_in_content(query, st.session_state.knowledge_base)
                response = format_response(query, results)
            except Exception as e:
                response = f"❌ Error al buscar: {str(e)}"
                results = []
    
    # Mostrar respuesta
    with st.chat_message("assistant"):
        st.markdown(response)
    
    # Agregar respuesta al historial
    st.session_state.chat_history.append({"role": "assistant", "content": response})
    
    # Mostrar detalles de resultados si hay
    if st.session_state.knowledge_base and 'results' in locals() and results:
        with st.expander("📋 Ver detalles de resultados"):
            for i, result in enumerate(results[:3], 1):
                st.markdown(f"### Resultado {i}")
                if result['type'] == 'program':
                    st.code(f"Programa: {result['name']}\nUbicación: {result['folder']}", language=None)
                else:
                    st.code(f"Archivo: {result['path']}", language=None)
                st.text_area("Contenido completo:", result['full_content'][:1000], height=200, key=f"detail_{i}")

# Footer
st.markdown("---")
st.markdown("**📚 BOT Biblioteca W2M** - Asistente de consulta de biblioteca SAP ABAP")
st.markdown("*Desarrollado para facilitar el acceso a la información de la biblioteca*")

