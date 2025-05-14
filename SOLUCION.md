# Solución del Escape Room Web - "El Culto del Sello Roto"

**¡ALERTA DE SPOILER!** Este documento contiene la solución completa paso a paso.

## Etapa 1: Registro e Inspección del JWT

1. Regístrate como un nuevo usuario
2. En el panel de control, inspecciona el Token JWT que se muestra
3. Decodifica el JWT (puedes usar jwt.io)
4. Observa que contiene campos `username` y `role` con valor `initiate`

## Etapa 2: Explotación XSS en el Mural

1. Navega al "Mural de Revelaciones"
2. Publica un mensaje con el siguiente código JavaScript:
   ```html
   <script>
     fetch("/promote");
   </script>
   ```
3. Haz clic en el botón "Simular lectura del Sumo Sacerdote" (solo para demo)
4. Cuando el bot lee el mensaje, ejecuta el script y promueve tu usuario
5. Verifica en tu panel que ahora eres "Elegido" (`role: chosen`)

## Etapa 3: Acceso a la Galería Secreta

1. Ahora que eres "Elegido", puedes acceder a la "Galería Secreta"
2. Descarga la imagen "revelacion.jpg"
3. Examina los metadatos de la imagen usando herramientas como ExifTool:
   ```
   exiftool revelacion.jpg
   ```
4. En los metadatos encontrarás la siguiente ruta secreta:
   ```
   NEXT_STAGE: /temple/veil/4f5e3
   ```

## Etapa 4: Encontrar la Clave del Sumo Sacerdote

1. Visita el perfil del Sumo Sacerdote
2. Inspecciona el código fuente de la página (o selecciona todo en la biografía)
3. Encontrarás la clave oculta en un texto con color similar al fondo:
   ```
   KEY: dark3ssUnveiled
   ```

## Etapa 5: Descifrar el Mensaje Final

1. Visita la URL encontrada en los metadatos: `/temple/veil/4f5e3`
2. Verás un mensaje cifrado
3. Ingresa la clave del Sumo Sacerdote: `dark3ssUnveiled`
4. Haz clic en "Descifrar" para revelar la FLAG:
   ```
   FLAG{XSS_D4RKW4LL_M4ST3R}
   ```

¡Felicidades! Has completado el Escape Room Web.
