# Escape Room Web - "El Culto del Sello Roto"

Una aplicación web vulnerable basada en Flask que simula un escape room digital con varias vulnerabilidades de seguridad intencionadas para practicar habilidades de ciberseguridad.

## Descripción

Este proyecto simula un "culto digital" con un sistema de autenticación vulnerable. Los usuarios deben explotar varias vulnerabilidades para progresar a través de diferentes niveles y finalmente obtener una FLAG secreta.

## Vulnerabilidades incluidas

1. **JWT no verificado** - Los tokens JWT pueden ser manipulados
2. **XSS almacenado** - Mural de mensajes vulnerable a inyección de código JavaScript
3. **Metadatos sensibles** - Información oculta en imágenes
4. **Secretos visibles** - Datos ocultos en el código fuente del sitio

## Instrucciones de instalación

### Requisitos previos

- Docker y Docker Compose

### Pasos para ejecutar

1. Clona este repositorio:

   ```
   git clone https://github.com/tu-usuario/escape-room-web.git
   cd escape-room-web
   ```

2. Inicia el contenedor con Docker Compose:

   ```
   docker-compose up --build
   ```

3. Accede a la aplicación en tu navegador:
   ```
   http://localhost:5000
   ```

## Cómo jugar

1. Regístrate como un nuevo usuario
2. Explora el sitio y encuentra las vulnerabilidades
3. Aprovecha cada vulnerabilidad para seguir avanzando
4. Tu objetivo final es encontrar la FLAG oculta

## Solución

> **¡ALERTA DE SPOILER!**
>
> La solución paso a paso está disponible en el archivo `SOLUCION.md`, pero te recomendamos intentar resolver el desafío por tu cuenta primero.

## Advertencia

Esta aplicación es intencionalmente vulnerable con fines educativos. NO la despliegues en un entorno de producción o en un servidor público.

## Licencia

MIT
