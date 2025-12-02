Ejercicio individual
Contexto del Proyecto: Plataforma de Gestión de Productos

Imagina que estás desarrollando una plataforma para gestionar productos en una tienda en línea utilizando Django. El proyecto debe incluir un sistema administrativo donde los usuarios puedan crear, editar y eliminar productos, pero con diferentes niveles de acceso. Tu tarea será configurar y personalizar el sitio administrativo de Django para gestionar productos de manera eficiente.

Requerimientos

1.-Creación de un Superusuario:
Utilizando manage.py, crea un superusuario para acceder al sitio administrativo de Django.
Asegúrate de que el superusuario tenga acceso completo a todas las funcionalidades del sitio administrativo.

2.-Accediendo al Sitio Administrativo:
Inicia el servidor de desarrollo de Django y accede al sitio administrativo en http://127.0.0.1:8000/admin/.
Usa las credenciales del superusuario para iniciar sesión y ver el panel de administración.

3.-Creación de un Modelo de Producto:
Crea un modelo Producto en tu aplicación que incluya los campos básicos como nombre, descripción, precio, stock, y fecha de creación.
Registra este modelo en el archivo admin.py para que sea visible en el sitio administrativo.

4.-Manejo de Usuarios:
Crea varios usuarios de prueba con diferentes permisos (por ejemplo, un usuario administrador y un usuario normal).
Asigna a estos usuarios distintos niveles de acceso y asegúrate de que solo el administrador pueda eliminar productos.

5.-Manejo de Grupos en la Página Administrativa:
Crea grupos en el sitio administrativo de Django (por ejemplo, un grupo de "Administradores" y un grupo de "Gestores de Productos").
Asigna permisos específicos a cada grupo, como permitir que los administradores puedan editar y eliminar productos, mientras que los gestores de productos solo puedan agregar y modificar productos.

6.-Configuración de Permisos para Usuarios:
En la página administrativa, configura permisos específicos para los usuarios. Por ejemplo, asegúrate de que algunos usuarios solo puedan ver los productos, mientras que otros puedan modificar y eliminar productos.
Prueba que los permisos estén funcionando correctamente al intentar realizar diferentes acciones con usuarios de distintos roles.

7.-Limitación de Acceso al Sitio Administrativo:
Configura tu proyecto para limitar el acceso al sitio administrativo solo a los usuarios autenticados. Asegúrate de que no sea accesible para usuarios no registrados o no autenticados.

8.-Manejo de Errores en el Modelo Auth:
Asegúrate de que el sistema de autenticación maneje correctamente los errores, como contraseñas incorrectas o intentos fallidos de acceso.
Muestra un mensaje claro de error cuando un usuario intente acceder al sitio administrativo con credenciales incorrectas.

9.-Probando el Modelo Auth con los Usuarios:
Realiza pruebas para verificar que los usuarios con diferentes roles tengan acceso solo a las funcionalidades que se les ha permitido.
Si un usuario sin permisos intenta realizar una acción no permitida (por ejemplo, eliminar un producto), Django debe redirigirlo a una página de error o de acceso denegado.