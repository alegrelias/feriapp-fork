# FeriApp 🏪

Sistema web de gestión de ferias y emprendedores desarrollado con Django 5.1+.
Permite administrar ferias temáticas, gestionar inscripciones de emprendedores y controlar la disponibilidad de puestos, con autenticación de usuarios y panel de administración.

---

## 🛠️ Stack

| Tecnología | Versión |
|------------|---------|
| Python | 3.13+ |
| Django | 5.1+ |
| Base de datos | SQLite (desarrollo) |
| Frontend | Bootstrap 5 |
| Tests | `django.test.TestCase` |
| Control de versiones | Git + GitHub |

---

## ✨ Funcionalidades

- 🔐 Registro, login y logout de usuarios
- 🗂️ Gestión de categorías y ferias
- 🧑‍💼 Gestión de emprendedores
- 📋 Inscripción a ferias con control de disponibilidad de puestos
- 📊 Panel de inicio con estadísticas generales
- 📈 Barra de ocupación por feria (Bootstrap progress bar)
- 🛠️ Panel de administración Django configurado
- 📱 Interfaz responsiva con Bootstrap 5

---

## 👥 Integrantes

| Nombre | Usuario GitHub |
|--------|---------------|
| Elias N. Alegre | [@alegrelias](https://github.com/alegrelias) |
| Abigail D. Gómez | [@aby-gomez](https://github.com/aby-gomez) |
| Ricardo Iraola | [@Ricardo-Iraola](https://github.com/Ricardo-Iraola) |
| Daniela A. Marchisoney | [@UzumakiN314](https://github.com/UzumakiN314) |


---

## 🚀 Instalación y uso

### 1. Clonar el repositorio

```bash
git clone https://github.com/alegrelias/feriapp-fork.git
cd feriapp-fork
```

### 2. Crear y activar el entorno virtual

```bash
# Windows
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 4. Aplicar migraciones

```bash
python manage.py migrate
```

### 5. Crear usuarios de prueba, SuperUsuario, Emprendedor y Visitante

```bash
python manage.py cargar_datos_prueba
```

### 6. Correr el servidor de desarrollo

```bash
python manage.py runserver
```

Accedé a [http://localhost:8000](http://localhost:8000)
Panel admin: [http://localhost:8000/admin](http://localhost:8000/admin)

---

## 🧪 Correr los tests

```bash
# Todos los tests con detalle
python manage.py test -v 2

# Solo tests de modelos
python manage.py test app.tests.test_models -v 2

# Solo tests de vistas
python manage.py test ferias.tests.test_views -v 2
```

---

## 🔑 Credenciales de prueba

> ⚠️ Solo para uso del corrector en entorno de desarrollo local.

| Rol | Usuario | Contraseña | Nombre |
|-----|---------|-----------|--------|
| Superusuario / Admin | `admin` | `admin1234` | — |
| Emprendedor | `emprendedor1` | `test1234` | Juan Pérez |
| Emprendedor | `emprendedor2` | `test1234` | María López |
| Emprendedor | `emprendedor3` | `test1234` | Carlos Ruiz |
| Visitante | `visitante1` | `test1234` | Ana Gómez |
| Visitante | `visitante2` | `test1234` | Pedro Díaz |
---

## 📁 Estructura del proyecto

```
feriapp/
├── feriapp/            # Configuración del proyecto Django
│   ├── settings.py
│   └── urls.py
├── ferias/             # App principal
│   ├── models.py       # Categoria, Feria, Emprendedor, Inscripcion
│   ├── views.py
│   ├── urls.py
│   ├── forms.py
│   ├── admin.py
│   ├── consultas.py    # Consultas ORM
│   └── tests/
│       ├── test_models.py
│       └── test_views.py
├── templates/
│   ├── base.html
│   └── registration/
├── static/
├── manage.py
├── requirements.txt
└── .gitignore
```

---

## Capturas

### Inicio
Siguiendo buenas prácticas el diseño es mobile first.

<table>
<tr>
<td align="center"><b>Mobile</b></td>
<td align="center"><b>Escritorio</b></td>
</tr>
<tr>
<td><img width="280" alt="Vista mobile del inicio" src="https://github.com/user-attachments/assets/6e053610-be83-4dc2-a583-c58c44db08d8" /></td>
<td><img width="500" alt="Vista escritorio del inicio" src="https://github.com/user-attachments/assets/d8c48051-8f02-4220-b95a-a46b140d4bd3" /></td>
</tr>
</table>

---

### Detalle de feria
Cada feria posee una ficha con descripciones, permiten la inscripción de emprendedores o la reseña de cada visitante en la feria.

<img width="450" alt="Detalle de feria" src="https://github.com/user-attachments/assets/443b231c-c506-4528-a903-cdab6eb8ccbf" />

---

### Panel de administración

<img width="600" alt="Panel de administración" src="https://github.com/user-attachments/assets/1b65029d-0c15-4e10-bb8f-569f806a5a4f" />

---

###  Perfil
Vistas de perfil diferenciadas según tipo de usuario. El emprendedor tiene detalle de actividad más sus inscripciones, con posibilidad de cancelarlas. El visitante puede visualizar sus reseñas. Emprendedor con permisos de organizador puede aprobar o cancelar inscripciones

<table>
<tr>
<td align="center"><b>Perfil Emprendedor</b></td>
<td align="center"><b>Perfil Visitante</td></b></td>
<td align="center"><b>Emprendedor con permisos de organizador</b></td>
  </tr>
<tr>
<td><img width="280" alt="Perfil de emprendedor" src="https://github.com/user-attachments/assets/b886070a-d49d-405b-a9f1-8d614bd3bcdf" /></td>
  <td><img width="280"  alt="image" src="https://github.com/user-attachments/assets/6016046d-81d2-40d6-a8c8-606bb02aeb8e" />
</td>
  <td><img width="280"  alt="image" src="https://github.com/user-attachments/assets/8c1d3647-569a-4f2c-a3ad-781738e4cbba" />
</td>
</tr>
</table>

---

### Login 

<table>
<tr>
<td align="center"><b>Login</b></td>
</tr>
<tr>
<td><img width="280" alt="Login" src="https://github.com/user-attachments/assets/3ac9be97-f7d9-4cbb-999f-32a1b15cff31" /></td>
  </tr>
</table>
---

## 🧩 Decisiones de diseño



Describir aquí:
- Por qué eligieron este dominio
- Cómo modelaron la disponibilidad de puestos (método vs. anotación ORM)
- Qué validaciones pusieron en el modelo vs. en el formulario
- Cómo dividieron el trabajo entre los integrantes
- Cualquier decisión no obvia (ej: por qué el constraint de puesto único, cómo manejaron lista de espera, etc.)

---

# Elección del dominio y motivación

Elegimos desarrollar FeriApp porque nos permitía trabajar con una problemática cercana a una situación real, donde no solo era necesario almacenar información, sino también administrar reglas de negocio. El sistema debía gestionar ferias, emprendedores, visitantes e inscripciones, contemplando restricciones como la disponibilidad de puestos, los distintos estados de las inscripciones y diferentes tipos de usuarios.

Además, al ser nuestro primer proyecto grande utilizando Django, nos pareció un dominio adecuado para aprender a modelar relaciones entre entidades, trabajar con el ORM, formularios, vistas, autenticación y persistencia de datos, integrando también herramientas como Git para el trabajo colaborativo.

# Modelado de la disponibilidad de puestos

Decidimos no almacenar la cantidad de puestos ocupados o disponibles como atributos de la base de datos. En su lugar, esa información se calcula dinámicamente mediante métodos del modelo (puestos_ocupados(), puestos_disponibles() y tiene_lugar()), utilizando el estado actual de las inscripciones.

Elegimos este enfoque porque evita duplicar información y reduce el riesgo de inconsistencias si una inscripción cambia de estado. Además, estos métodos se reutilizan en las vistas para mostrar la barra de ocupación de cada feria y generar estadísticas generales del sistema.

# Validaciones en el modelo y en el formulario

Una de las decisiones más importantes fue centralizar las reglas de negocio en los modelos. Durante el desarrollo observamos que todos seguían el mismo proceso al crear o actualizar objetos: validar los datos y, si eran correctos, guardarlos en la base de datos. Para evitar repetir esa lógica implementamos una clase abstracta llamada ValidableModel, que concentra el comportamiento común de validate(), new() y update(). De esta manera, todos los modelos siguen el mismo flujo y solo deben implementar sus propias reglas de validación.

En Feria se valida la coherencia de las fechas y la capacidad de puestos. En Inscripción, donde se concentra la mayor parte de la lógica del sistema, se controla que un emprendedor no pueda inscribirse dos veces en la misma feria, que un puesto solo pueda asignarse a inscripciones en lista de espera y que no existan dos inscripciones confirmadas ocupando el mismo puesto mediante el método existe_puesto(). También se restringen modificaciones que romperían la lógica del sistema, como cambiar el emprendedor o la feria de una inscripción ya existente.

Los formularios y las vistas quedaron enfocados en la interacción con el usuario, se personalizaron widgets, tipos de entrada y estilos utilizando Bootstrap, mientras que las reglas del negocio permanecieron centralizadas en los modelos.

# División del trabajo

El desarrollo del proyecto se organizó distribuyendo las principales responsabilidades entre los integrantes del equipo. Si bien cada uno estuvo a cargo de un conjunto de funcionalidades, el trabajo fue integrándose de forma continua mediante Git y GitHub, realizando revisiones cruzadas, correcciones y ajustes para mantener un diseño uniforme y respetar las decisiones de arquitectura adoptadas para toda la aplicación.

# La distribución inicial de tareas fue la siguiente:

Arquitectura de autenticación y administración: implementación del registro, inicio y cierre de sesión de usuarios, /navegación dinámica según el estado de autenticación y configuración del panel de administración de Django.
Consultas y vistas de información: desarrollo de la página principal con estadísticas generales, listado de ferias con filtro por categorías, listado de emprendedores y perfil de usuario.
Gestión de ferias: implementación del detalle de cada feria, mostrando la información general, los emprendedores inscriptos y el porcentaje de ocupación de puestos, además del formulario para crear nuevas ferias.
Gestión de inscripciones: desarrollo del proceso de inscripción de emprendedores a una feria, visualización de las inscripciones realizadas, cancelación de inscripciones y sistema de reseñas.

Aunque inicialmente existió una división de actividades, varias decisiones se tomaron en conjunto. Entre ellas, la creación de la clase abstracta ValidableModel para reutilizar la lógica de validación y persistencia, la definición de las reglas de negocio de las inscripciones, el modelado de la disponibilidad de puestos y la organización general de la arquitectura del proyecto. En relación a lo dicho, esto nos permitió mantener un criterio común durante todo el desarrollo y facilitar la integración del trabajo realizado por cada integrante.

# Otras decisiones

Además de las decisiones anteriores, incorporamos algunos cambios para mejorar la organización del sistema. Implementamos managers personalizados para encapsular consultas frecuentes, como listar emprendedores ordenados o recuperar las inscripciones confirmadas, evitando repetir consultas en las vistas.

Por otra parte, tomamos algunas decisiones de modelado que se apartan levemente del diagrama original. En esta ocasión, decidimos vincular las reseñas directamente con la feria y no con el emprendedor. Consideramos que el objetivo de una reseña es evaluar la experiencia general del visitante durante la feria (organización, infraestructura, ubicación, etc.) y no el desempeño de un expositor en particular. De esta manera, una misma feria puede recibir múltiples reseñas que reflejen la percepción global de los asistentes.

Por último, el control del flujo de creación se realiza utilizando form.save(commit=False), lo que permite completar datos que no provienen del formulario y ejecutar las validaciones del modelo antes de guardar definitivamente el objeto en la base de datos.

# Aprendizajes

El proyecto fue evolucionando a medida que avanzábamos en el aprendizaje de Python, Django y el trabajo colaborativo con Git. Varias decisiones fueron apareciendo durante el desarrollo, cuando detectamos código repetido, responsabilidades mal distribuidas o reglas de negocio que podían centralizarse mejor.

Nuestro objetivo fue construir una aplicación mantenible y coherente. La incorporación de una clase base reutilizable, la separación de responsabilidades, el uso de managers personalizados y la centralización de las validaciones para contribuir a la arquitectura del proyecto.


## ⭐ Funcionalidades opcionales implementadas

[🟪 ✔] Vista "Mis inscripciones" para el emprendedor autenticado

[🟪 ✔] Mensajes flash con `django.contrib.messages`
- [ ] Paginación en lista de ferias
- [ ] Barra de búsqueda por nombre o ubicación
      
[ 🟪 ✔] Permisos diferenciados (Organizador vs. Emprendedor)
- [ ] Tests de integración (flujo completo)

---

## Probar el sistema de permisos

1. Iniciar sesión como `admin` / `admin1234`
2. Ir a `/admin/auth/user/`
3. Elegír cualquier usuario (ej: `emprendedor1`) y editarlo
4. En la sección "Permisos de usuario",  asignar el permiso `app | inscripcion | Can change inscripcion`
5. Guardar los cambios
6. Cerrár sesión e iniciar nuevamente con ese usuario para verificar que ahora puede aprobar/cancelar inscripciones

---

## 🐛 Problemas comunes

| Problema | Solución |
|----------|----------|
| `OperationalError: no such table` | Corré `python manage.py migrate` |
| `No module named django` | Activá el entorno virtual |
| Barra de progreso muestra 0% | Verificá que `puestos_ocupados()` cuenta solo inscripciones `confirmadas` |
| Login no redirige bien | Verificá `LOGIN_REDIRECT_URL` en `settings.py` |
