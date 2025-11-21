# 📚 BOT Biblioteca W2M

Asistente inteligente para consultar la biblioteca de programas SAP ABAP de W2M.

## 🚀 Características

- ✅ **Búsqueda inteligente** en toda la biblioteca
- ✅ **Interfaz de chat** intuitiva
- ✅ **Sin instalación** para el usuario final
- ✅ **Indexación automática** de archivos
- ✅ **Búsqueda por programa, funcionalidad o contenido**

## 📋 Requisitos

- Python 3.8 o superior
- Streamlit

## 🛠️ Instalación Local (Opcional)

Si quieres ejecutarlo localmente:

```bash
# Instalar dependencias
pip install -r requirements.txt

# Ejecutar la aplicación
streamlit run app.py
```

## ☁️ Despliegue en Streamlit Cloud (Recomendado)

### Opción 1: Desde GitHub (Sin instalación para usuarios)

1. **Sube el código a GitHub:**
   ```bash
   git init
   git add .
   git commit -m "BOT Biblioteca W2M"
   git remote add origin [TU_REPO_GITHUB]
   git push -u origin main
   ```

2. **Conecta con Streamlit Cloud:**
   - Ve a [share.streamlit.io](https://share.streamlit.io)
   - Inicia sesión con GitHub
   - Click en "New app"
   - Selecciona tu repositorio
   - Configura:
     - **Main file path:** `bot_biblioteca/app.py`
     - **Python version:** 3.8+
   - Click "Deploy"

3. **Comparte el enlace:**
   - Streamlit Cloud generará un enlace público
   - Comparte este enlace con tu compañero
   - **No necesita instalar nada**, solo abrir el enlace en el navegador

### Opción 2: Streamlit Community Cloud (Gratis)

Streamlit Cloud ofrece hosting gratuito para aplicaciones públicas. Tu compañero solo necesita:
- Un navegador web
- El enlace que compartas

## 📁 Estructura del Proyecto

```
bot_biblioteca/
├── app.py              # Aplicación principal Streamlit
├── requirements.txt    # Dependencias Python
└── README.md          # Este archivo
```

## 🎯 Uso

1. **Indexar la biblioteca:**
   - En la barra lateral, ingresa la ruta de tu biblioteca
   - Click en "🔄 Indexar Biblioteca"
   - Espera a que se complete la indexación

2. **Hacer consultas:**
   - Escribe tu pregunta en el chat
   - El BOT buscará en toda la biblioteca
   - Revisa los resultados y detalles

3. **Preguntas sugeridas:**
   - Usa las preguntas sugeridas en la barra lateral
   - O escribe tus propias preguntas

## 💡 Ejemplos de Preguntas

- "¿Qué programas hay para facturas?"
- "¿Cómo funciona la integración con Azure?"
- "¿Qué reports de finanzas existen?"
- "¿Dónde están los programas de BlueBay?"
- "¿Qué programas hay para República Dominicana?"
- "¿Cómo se procesan los pagos?"

## 🔧 Configuración Avanzada

### Personalizar la búsqueda

Puedes modificar `app.py` para:
- Ajustar el número de resultados mostrados
- Cambiar el tamaño del contexto extraído
- Agregar más tipos de archivos a indexar
- Mejorar el algoritmo de relevancia

### Agregar más fuentes de datos

Edita la función `index_library()` para incluir:
- Más carpetas de documentación
- Archivos de código fuente
- Bases de datos externas

## 📝 Notas

- La primera indexación puede tardar unos segundos
- Los archivos se indexan en memoria (se reinicia al recargar)
- Para producción, considera usar una base de datos vectorial

## 🆘 Solución de Problemas

**Error al indexar:**
- Verifica que la ruta de la biblioteca sea correcta
- Asegúrate de tener permisos de lectura

**No encuentra resultados:**
- Intenta reformular la pregunta
- Usa términos más específicos
- Verifica que la biblioteca esté indexada

## 📞 Soporte

Para problemas o sugerencias, contacta al desarrollador.

---

**Desarrollado para W2M - Santiago Jarouge**

