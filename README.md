# Sistema de Gestión de Carreras (Back end)

Este proyecto es una aplicación desarrollada en **Python** utilizando el framework **FastAPI**, con **MongoDB** como base de datos. El objetivo principal es gestionar de forma estructurada los datos relacionados a **categorías de carreras de deportes a motor**, organizados por **temporadas**.

## 🧠 Funcionalidades Principales

El sistema permite realizar operaciones CRUD sobre:

- **Temporadas**
- **Categorías de carrera**
- **Sistemas de puntuación**
- **Escuderías / Equipos**
- **Escuderías / Equipos dentro de una temporada**
- **Pilotos**
- **Pilotos dentro de una temporada**
- **Circuitos**
- **Circuitos dentro de una temporada**
- **Sistemas de puntuaciones**

---

## 📁 Estructura del Proyecto

1. **Temporadas**  
   La base de toda la organización. Los datos de categorías, circuitos, sistemas de puntuacion, equipos y pilotos deben estar dentro de una temporada activa.

2. **Categorías de carrera**  
   Ejemplo: Fórmula 1, Rally, etc. Cada categoría puede tener su propio sistema de puntuación.

3. **Sistema de puntuación**  
   Define cómo se reparten los puntos según la posición en una carrera.

4. **Participantes**
   - **Equipos / Escuderías**
   - **Pilotos**, cada uno asociado a un equipo.

5. **Carreras registradas**
   - **Cada carrera podra ser vista o modificada una vez cargada**

6.**Datos de carreras**
   - Se podran visualizar posiciones de una carrera cargada
   - Podios logrados en una temporada tanto por equipos como por pilotos
   - Podios logrados a lo largo de una categorira tanto como pilotos como equipos

---

## 🔁 Flujo de Uso

1. Crear una **temporada**.
2. Dentro de la temporada:
   - *Contara con una serie de campos esenciales los cuales permitiral el correcto funcionamiento*
3. Cargas esenciales:
   - *Cargar un **sistema de puntiacion** (dato para el que anteriormente se debe cargar una temporada para poder asignarsela)*
   - *Cargar **equipos** y **pilotos** como tal, fuera de temporada lo que permitira la reutilizacion*.
   - *Cargar **equipos** y **pilotos** dentro de la temporada para permitir su utilizacion en la conformacion de equipos.*
   - *Cargar las conformaciones de equipos (para esto antes deben estar cargado tanto los equipos como pilotos necesarios dentro de la temporada)*
   - *Cargar los **circuitos** que se quieran cargar (luego podran ser utilizados en una temporada o no)*
   - *Cargar los **circuitos** necesarios dentro de una temporada.*
4. A partir de ahí, se pueden registrar resultados de carreras y calcular los puntos automáticamente, ademasd de otros tipos de especificaciones de datos.

## ⚠️ Validaciones

**Se debe tener en cuenta que existen una gran serie de validaciones la cuales permiten o no realizar cargas.**

---

## 🧰 Tecnologías Utilizadas

- Python 3.x
- FastAPI
- Uvicorn (servidor ASGI)
- MongoDB (conector: Motor o PyMongo)
- Pydantic (validaciones de datos)


---

## 🚀 Cómo ejecutar el proyecto

```bash
## Instalar dependencias
pip install -r requirements.txt

# Ejecutar el servidor
uvicorn main:app --reload
