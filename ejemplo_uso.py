"""
Script de ejemplo para probar la indexación de la biblioteca
Ejecutar: python ejemplo_uso.py
"""

from pathlib import Path
import sys

# Agregar el directorio actual al path
sys.path.insert(0, str(Path(__file__).parent))

from app import index_library, search_in_content

def main():
    # Ruta de la biblioteca (ajustar según tu caso)
    base_path = Path(__file__).parent.parent
    
    print("🔍 Indexando biblioteca...")
    print(f"📂 Ruta: {base_path}")
    
    try:
        kb, count = index_library(str(base_path))
        print(f"✅ Indexación completada: {count} archivos")
        
        # Pruebas de búsqueda
        queries = [
            "facturas",
            "Azure",
            "BlueBay",
            "ZFI_BLUEBAY_GET",
            "República Dominicana"
        ]
        
        print("\n" + "="*50)
        print("🧪 Pruebas de búsqueda:")
        print("="*50)
        
        for query in queries:
            print(f"\n🔎 Buscando: '{query}'")
            results = search_in_content(query, kb)
            print(f"   📊 Encontrados: {len(results)} resultados")
            if results:
                print(f"   🎯 Top resultado: {results[0].get('name', results[0].get('path', 'N/A'))}")
        
        print("\n✅ Pruebas completadas!")
        
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()

