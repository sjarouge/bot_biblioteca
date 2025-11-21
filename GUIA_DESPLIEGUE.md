# 🚀 Guía de Despliegue - BOT Biblioteca W2M

Esta guía te ayudará a desplegar el BOT de forma que tu compañero pueda usarlo **sin instalar nada**.

## 📋 Opciones de Despliegue

### Opción 1: Streamlit Cloud (Recomendada - Gratis) ⭐

**Ventajas:**
- ✅ Completamente gratis
- ✅ Sin instalación para usuarios
- ✅ Acceso desde cualquier navegador
- ✅ Actualizaciones automáticas desde GitHub
- ✅ URL pública permanente

**Pasos:**

1. **Preparar el repositorio:**
   ```bash
   cd bot_biblioteca
   git init
   git add .
   git commit -m "BOT Biblioteca W2M"
   ```

2. **Subir a GitHub:**
   - Crea un repositorio en GitHub (puede ser privado o público)
   - Conecta tu repositorio local:
   ```bash
   git remote add origin https://github.com/TU_USUARIO/bot-biblioteca-w2m.git
   git push -u origin main
   ```

3. **Desplegar en Streamlit Cloud:**
   - Ve a [share.streamlit.io](https://share.streamlit.io)
   - Inicia sesión con tu cuenta de GitHub
   - Click en **"New app"**
   - Configura:
     - **Repository:** Selecciona tu repositorio
     - **Branch:** `main` (o `master`)
     - **Main file path:** `bot_biblioteca/app.py`
     - **Python version:** `3.8` o superior
   - Click en **"Deploy"**

4. **Compartir:**
   - Streamlit generará una URL como: `https://tu-app.streamlit.app`
   - Comparte esta URL con tu compañero
   - **¡Listo!** Tu compañero solo necesita abrir el enlace

**Nota importante:** Para que el BOT funcione, necesitas que la biblioteca esté accesible. Tienes dos opciones:

- **Opción A:** Subir la biblioteca al repositorio (puede ser grande)
- **Opción B:** Usar una ruta compartida o OneDrive (si Streamlit puede acceder)

### Opción 2: Streamlit Community Cloud (Alternativa)

Similar a la Opción 1, pero usando el servicio comunitario de Streamlit.

### Opción 3: Ejecución Local con Compartir Pantalla

Si prefieres mantener todo local:

1. **Ejecutar localmente:**
   ```bash
   cd bot_biblioteca
   pip install -r requirements.txt
   streamlit run app.py
   ```

2. **Compartir acceso:**
   - Usa herramientas como **ngrok** para crear un túnel:
   ```bash
   ngrok http 8501
   ```
   - Comparte la URL de ngrok con tu compañero

### Opción 4: Servidor Propio

Si tienes un servidor disponible:

1. Instala Python y Streamlit en el servidor
2. Clona el repositorio
3. Ejecuta con `streamlit run app.py --server.port 8501`
4. Configura un proxy inverso (nginx) si es necesario
5. Comparte la URL del servidor

## 🔧 Configuración de la Biblioteca

### Para Streamlit Cloud

Si subes la biblioteca al repositorio:

1. **Estructura recomendada:**
   ```
   tu-repo/
   ├── bot_biblioteca/
   │   ├── app.py
   │   └── requirements.txt
   └── biblioteca/  (o enlace simbólico)
       ├── BIBLIOTECA_W2M_CONOCIMIENTO_BOT.txt
       └── ...
   ```

2. **Modificar app.py:**
   Cambia la ruta por defecto para apuntar a la biblioteca en el repo:
   ```python
   default_path = str(Path(__file__).parent.parent / 'biblioteca')
   ```

### Para OneDrive/Compartida

Si la biblioteca está en OneDrive o una carpeta compartida:

1. **En Windows:**
   - Usa la ruta completa de OneDrive
   - Ejemplo: `C:\Users\sjaro\OneDrive\W2M\03 Biblioteca`

2. **En Streamlit Cloud:**
   - Necesitarás subir la biblioteca al repositorio
   - O usar un servicio de almacenamiento en la nube accesible

## 📝 Checklist de Despliegue

- [ ] Código subido a GitHub
- [ ] Repositorio conectado a Streamlit Cloud
- [ ] Aplicación desplegada correctamente
- [ ] Biblioteca accesible (subida o en ruta compartida)
- [ ] URL compartida con el compañero
- [ ] Probado que funciona desde otro dispositivo

## 🐛 Solución de Problemas

### Error: "No se encuentra la biblioteca"
- Verifica que la ruta sea correcta
- En Streamlit Cloud, asegúrate de que los archivos estén en el repositorio
- Usa rutas relativas desde `app.py`

### Error: "Módulo no encontrado"
- Verifica que `requirements.txt` tenga todas las dependencias
- Streamlit Cloud instalará automáticamente, pero revisa los logs

### La aplicación es lenta
- Considera indexar solo archivos importantes
- Limita el tamaño de los archivos indexados
- Usa caché de Streamlit para la indexación

## 💡 Mejoras Futuras

Para hacer el BOT aún mejor:

1. **Base de datos vectorial:** Usar ChromaDB o Pinecone para búsqueda semántica
2. **Embeddings:** Implementar embeddings con sentence-transformers
3. **Caché persistente:** Guardar la indexación en disco
4. **Autenticación:** Agregar login si es necesario
5. **API REST:** Crear una API para integraciones

## 📞 Soporte

Si tienes problemas con el despliegue:
1. Revisa los logs en Streamlit Cloud
2. Verifica que todos los archivos estén en el repositorio
3. Prueba ejecutando localmente primero

---

**¡Listo para compartir! 🎉**

