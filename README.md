ALVID - MANUAL DE INSTALACIÓN Y EJECUCIÓN

Sistema Web Progresivo para la Generación de Cotizaciones y Optimización de Cortes en Carpintería basado en Machine Learning

=================================================================

1. DESCRIPCIÓN DEL SISTEMA
   =================================================================

ALVID es una aplicación web desarrollada para automatizar el proceso de generación de cotizaciones en empresas de carpintería y mueblería. El sistema permite gestionar materiales, optimizar cortes de tableros, calcular costos y generar cotizaciones de manera rápida y precisa.

=================================================================
2. REQUISITOS DEL SISTEMA
=========================

Hardware mínimo:

* Procesador Intel Core i3 o AMD Ryzen 3
* Memoria RAM: 4 GB
* Espacio disponible: 2 GB

Hardware recomendado:

* Procesador Intel Core i5 o AMD Ryzen 5
* Memoria RAM: 8 GB o superior
* Unidad SSD

Software requerido:

* Node.js versión 20 o superior
* Navegador web actualizado
* Conexión a Internet
* Cuenta de Supabase configurada

=================================================================
3. INSTALACIÓN DEL PROYECTO
===========================

Paso 1: Clonar el repositorio

git clone https://github.com/yummsleo-ai/cotizalvid.git

Paso 2: Ingresar al directorio del proyecto

cd cotizalvid

Paso 3: Instalar dependencias

npm install

Paso 4: Crear archivo de variables de entorno

Crear un archivo llamado .env en la raíz del proyecto.

Ejemplo:

VITE_SUPABASE_URL=URL_DE_SUPABASE
VITE_SUPABASE_ANON_KEY=CLAVE_PUBLICA_SUPABASE

Guardar los cambios.

=================================================================
4. EJECUCIÓN DEL SISTEMA
========================

Para iniciar el servidor de desarrollo ejecutar:

npm run dev

Una vez iniciado correctamente, abrir el navegador y acceder a:

http://localhost:5173

=================================================================
5. COMPILACIÓN PARA PRODUCCIÓN
==============================

Para generar la versión optimizada del sistema ejecutar:

npm run build

Para visualizar la compilación localmente:

npm run preview

=================================================================
6. FUNCIONALIDADES PRINCIPALES
==============================

1. Inicio de sesión de usuarios.

2. Dashboard administrativo.

3. Gestión de cotizaciones.

4. Registro y administración de materiales.

5. Optimización automática de cortes.

6. Cálculo y estimación de costos.

7. Generación de documentos de cotización.

8. Visualización de información mediante interfaz web responsiva.

=================================================================
7. ESTRUCTURA GENERAL DEL SISTEMA
=================================

src/
│
├── components/
├── pages/
├── services/
├── router/
├── composables/
└── assets/

=================================================================
8. POSIBLES ERRORES Y SOLUCIONES
================================

Error: npm no es reconocido como comando.

Solución:
Instalar Node.js y reiniciar la terminal.

---

Error: No se cargan los datos de Supabase.

Solución:
Verificar las variables VITE_SUPABASE_URL y
VITE_SUPABASE_ANON_KEY en el archivo .env.

---

Error: El servidor no inicia.

Solución:
Ejecutar nuevamente:

npm install

Posteriormente:

npm run dev

=================================================================
9. AUTOR
========

Leo Osvaldo Mamani Callisaya

Carrera de Ingeniería de Sistemas

Universidad Privada Franz Tamayo (UNIFRANZ)

=================================================================
10. PROPÓSITO
=============

El sistema ALVID fue desarrollado como proyecto académico para mejorar el proceso de cotización y optimización del uso de materiales en empresas de carpintería mediante tecnologías web modernas y técnicas de Machine Learning.
