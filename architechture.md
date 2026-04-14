# 🏗️ System Architecture

## Flow

Client → Flask API → AI Service → Ollama → Response → MySQL → Client

## Layers

### 1. Routes

Handles API endpoints

### 2. DTO

Validates input data

### 3. Service

Processes AI logic

### 4. Repository

Handles DB operations

### 5. Database

Stores generated posts

## Benefits

* Clean structure
* Scalable
* Easy to maintain
