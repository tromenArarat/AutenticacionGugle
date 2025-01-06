Pasos para iniciar Autenticación por terceros de Google con Python:

1. Crear un entorno virtual
   -- python -m venv venv
2. Activar el entorno virtual
  -- source venv/bin/activate (en Linux)
  -- venv\Scripts\activate (en Windou)
3. Instalar dependencias dentro del entorno virtual
  -- pip install -r requirements.txt
4. Configuración en la consola de Google Cloud
  a) Crear un proyecto en Google Cloud:
     - Ve a Google Cloud Console.
     - Crea un nuevo proyecto o selecciona uno existente.
  b) Habilitar la API de OAuth 2.0:
     - Ve a la sección "APIs y servicios" > "Biblioteca".
     - Busca y habilita la API "Google OAuth 2.0".
  c) Configurar credenciales:
      - Ve a "APIs y servicios" > "Credenciales".
  d) Crea una nueva credencial de tipo "ID de cliente de OAuth"
      - Tipo de aplicación: Selecciona "Aplicación web"
      - Añade los orígenes autorizados (e.g., http://localhost:5000) y URI de redireccionamiento (e.g., http://localhost:5000/callback)
5. Carga las variables de entorno en tu código


Deploy en: https://doguito.onrender.com/
