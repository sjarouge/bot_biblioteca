# Estructura Organizada de la Biblioteca W2M

## 📁 Organización por Categorías

### 01_Programas_Principales/
Programas principales organizados por módulo funcional:

#### FI_Finanzas/
- **Facturas_y_Abonos/**: Programas relacionados con procesamiento de facturas y abonos
- **Contabilizacion/**: Programas de contabilización automática
- **Pagos/**: Programas de gestión de pagos y transferencias
- **Formularios/**: Formularios y configuraciones de impresión

#### UT_Utilidades/
- Programas utilitarios generales (ZARR, ZUTR)

#### Integraciones/
- Programas de integración con sistemas externos

### 02_Reports/
Reportes y listados (programas ZFIR)

### 03_Clases_y_Funciones/
- Clases ABAP
- Módulos de función
- Includes reutilizables

### 04_Formularios_y_Smartforms/
- Formularios SAP
- Smartforms
- Configuraciones de impresión

### 05_Interfaces_y_WebServices/
#### Azure/
- Programas de integración con Azure

#### FTP/
- Programas de transferencia FTP

#### WebServices_Externos/
- Servicios web con sistemas externos

#### BlueBay/
- Integración específica con BlueBay

### 06_Monitores_y_Jobs/
#### Monitores_FI/
- Monitores de procesos financieros

#### Jobs_Procesamiento/
- Jobs de procesamiento batch

### 07_Documentacion_Tecnica/
- Documentación técnica
- Manuales
- Plantillas
- Catálogos

### 08_Utilidades_Desarrollo/
- Scripts de desarrollo
- Herramientas de búsqueda
- Referencias cruzadas

### 09_Archivos_Temporales/
- Archivos de trabajo temporal
- Pruebas

### 10_Backup_y_Versiones/
- Versiones anteriores
- Backups de programas

## 🔍 Convenciones de Nomenclatura

### Prefijos de Programas:
- **ZFI_**: Finanzas
- **ZFIR**: Reports de Finanzas  
- **ZFII**: Interfaces de Finanzas
- **ZARR**: Utilidades generales
- **ZUTR**: Utilidades de transporte

### Sufijos Comunes:
- **_GET**: Obtención de datos
- **_POST**: Envío de datos
- **_PROC**: Procesamiento
- **_LOG**: Logging
- **_MON**: Monitor
- **_UPD**: Actualización

## 📋 Categorización de Programas Existentes

### Programas de Azure:
- ZFI_AZURE_PDF_UPLOAD

### Programas de BlueBay:
- ZFI_BLUEBAY_GET
- ZFI_BLUEBAY_PROC

### Programas FTP:
- ZFI_FTP_ITEM
- ZFI_FTP_LISTA  
- ZFI_FTP_MAIL
- ZFI_FTP_READ

### Monitores:
- ZFI_MONITOR_0002
- ZFI_MONITOR_0003
- ZFI_MONITOR_0004

### Reports:
- ZFIR00412_FIX
- ZFIR00425 - ZFIR00444
- ZFIR00491
- ZFIR01141
- ZFIR02162

### WebServices:
- ZFI_GUEST_WS_GET
- ZFI_GUEST_WS_POST
- ZFI_GUITART_WS_GET
- ZFI_GUITART_WS_POST
- ZFI_WS_GET

### Utilidades:
- ZARR00171
- ZARR00172  
- ZARR00173
- ZUTR00024
- ZUTR00025

## 🚀 Próximos Pasos

1. ✅ Crear estructura de carpetas
2. 🔄 Mover programas a carpetas correspondientes
3. 📝 Actualizar índices y catálogos
4. 🔗 Crear referencias cruzadas
5. 📖 Actualizar documentación

---
*Última actualización: $(Get-Date -Format "dd/MM/yyyy HH:mm")*
