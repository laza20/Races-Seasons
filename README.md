# Sistema de Gestión de Carreras (Back end)

Este proyecto es una aplicación desarrollada en **Python** utilizando el framework **FastAPI**, con **MongoDB** como base de datos. El objetivo principal es gestionar de forma estructurada los datos relacionados a **categorías de carreras automovilísticas**, organizados por **temporadas**.

## 🧠 Funcionalidades Principales

El sistema permite realizar operaciones CRUD sobre:

- **Temporadas**
- **Categorías de carrera**
- **Sistemas de puntuación**
- **Escuderías / Equipos**
- **Pilotos**

---

## 📁 Estructura del Proyecto

1. **Temporadas**  
   La base de toda la organización. Los datos de categorías, equipos y pilotos deben estar dentro de una temporada activa.

2. **Categorías de carrera**  
   Ejemplo: Fórmula 1, Rally, etc. Cada categoría puede tener su propio sistema de puntuación.

3. **Sistema de puntuación**  
   Define cómo se reparten los puntos según la posición en una carrera.

4. **Participantes**
   - **Equipos / Escuderías**
   - **Pilotos**, cada uno asociado a un equipo.

---

## 🔁 Flujo de Uso

1. Crear una **temporada**.
2. Dentro de la temporada:
   - Registrar **categorías**.
   - Definir el **sistema de puntuación**.
   - Cargar **equipos** y **pilotos**.
3. A partir de ahí, se pueden registrar resultados de carreras y calcular los puntos automáticamente.

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
