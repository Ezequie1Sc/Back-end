# 🌍 API ASG - Autodiagnóstico Ambiental, Social y Gobernanza

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.0+-green.svg)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-13+-orange.svg)
![Flask-RESTX](https://img.shields.io/badge/Flask--RESTX-1.0+-red.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)
![Arquitectura](https://img.shields.io/badge/Arquitectura-Modular-blue)
![Swagger](https://img.shields.io/badge/Swagger-UI-brightgreen.svg)

<div align="center">
  
  ### 🌱 **Sistema de Evaluación de Sostenibilidad Empresarial** 🌍
  
  <img src="https://raw.githubusercontent.com/tandpfun/skill-icons/main/icons/Python-Dark.svg" width="60" height="60"/>
  <img src="https://raw.githubusercontent.com/tandpfun/skill-icons/main/icons/Flask-Dark.svg" width="60" height="60"/>
  <img src="https://raw.githubusercontent.com/tandpfun/skill-icons/main/icons/PostgreSQL-Dark.svg" width="60" height="60"/>
  
</div>

API RESTful profesional para la evaluación y autodiagnóstico de empresas en criterios ASG (Ambiental, Social y Gobernanza). Permite gestionar empresas, usuarios, indicadores y evaluaciones periódicas con cálculo automático de clasificaciones.

## 📋 Tabla de Contenidos

- [Características Principales](#-características-principales)
- [Stack Tecnológico](#-stack-tecnológico)
- [Arquitectura del Sistema](#-arquitectura-del-sistema)
- [Modelo de Datos](#-modelo-de-datos)
- [Instalación](#-instalación)
- [Endpoints de la API](#-endpoints-de-la-api)
- [Ejemplos de Uso](#-ejemplos-de-uso)
- [Sistema de Clasificación](#-sistema-de-clasificación)
- [Despliegue](#-despliegue)
- [Contribución](#-contribución)

## 🎯 Características Principales

<div align="center">

| 🌱 Ambiental | 👥 Social | ⚖️ Gobernanza |
|:------------:|:---------:|:-------------:|
| <img src="https://img.icons8.com/color/48/000000/leaf.png" width="40"/> | <img src="https://img.icons8.com/color/48/000000/conference.png" width="40"/> | <img src="https://img.icons8.com/color/48/000000/balance-scale.png" width="40"/> |
| Indicadores ambientales | Indicadores sociales | Indicadores de gobierno |
| Huella de carbono | Relación con empleados | Ética corporativa |
| Gestión de residuos | Impacto comunitario | Transparencia |

</div>

### ✨ Funcionalidades Destacadas

- **Gestión de Empresas**: Registro, perfiles y logos personalizados
- **Sistema de Usuarios**: Roles (admin/company) y autenticación segura
- **Indicadores ASG**: Configurables por área (Ambiental, Social, Gobernanza)
- **Evaluaciones Periódicas**: Por semestre con cálculos automáticos
- **Clasificación Automática**: Básico, Intermedio, Avanzado según puntuación
- **Upload de Imágenes**: Gestión de logos empresariales
- **Documentación Swagger**: API completamente documentada

## 🛠️ Stack Tecnológico

<div align="center">

| | | |
|:---:|:---:|:---:|
| <img src="https://raw.githubusercontent.com/tandpfun/skill-icons/main/icons/Python-Dark.svg" width="60"/> | <img src="https://raw.githubusercontent.com/tandpfun/skill-icons/main/icons/Flask-Dark.svg" width="60"/> | <img src="https://raw.githubusercontent.com/tandpfun/skill-icons/main/icons/PostgreSQL-Dark.svg" width="60"/> |
| **Python 3.8+** | **Flask 2.0+** | **PostgreSQL 13+** |
| <img src="https://raw.githubusercontent.com/tandpfun/skill-icons/main/icons/Git.svg" width="60"/> | <img src="https://raw.githubusercontent.com/tandpfun/skill-icons/main/icons/Github-Dark.svg" width="60"/> | <img src="https://raw.githubusercontent.com/tandpfun/skill-icons/main/icons/VSCode-Dark.svg" width="60"/> |
| **Git** | **GitHub** | **VS Code** |

</div>

### Backend
| Tecnología | Versión | Uso |
|------------|---------|-----|
| **Python** | 3.8+ | Lenguaje base |
| **Flask** | 2.0+ | Framework web |
| **Flask-RESTX** | 1.0+ | API RESTful + Swagger |
| **Flask-SQLAlchemy** | 3.0+ | ORM para base de datos |
| **PostgreSQL** | 13+ | Base de datos principal |
| **Werkzeug** | - | Seguridad (passwords, uploads) |
| **Flask-CORS** | 4.0+ | Habilitar CORS |
