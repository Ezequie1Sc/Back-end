

-- =========================================================
-- 1. TABLA DE ROLES
-- =========================================================
CREATE TABLE roles (
    id SERIAL PRIMARY KEY,
    name VARCHAR(50) UNIQUE NOT NULL
);

INSERT INTO roles (name) VALUES ('admin'), ('company');



-- =========================================================
-- 2. TABLA DE EMPRESAS
-- =========================================================
CREATE TABLE companies (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    sector VARCHAR(255),
    contact_name VARCHAR(255),
    contact_phone VARCHAR(50),

    logo_url TEXT,                           -- Logo de la empresa

    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);


-- =========================================================
-- 3. TABLA DE USUARIOS
-- =========================================================
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,

    role_id INTEGER NOT NULL REFERENCES roles(id),
    company_id UUID REFERENCES companies(id) ON DELETE SET NULL,

    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);



-- =========================================================
-- 4. TABLA DE ÁREAS (Ambiental / Social / Gobernanza)
-- =========================================================
CREATE TABLE areas (
    id SERIAL PRIMARY KEY,
    code VARCHAR(5) UNIQUE NOT NULL,     -- A, S, G
    name VARCHAR(255) NOT NULL,
    description TEXT
);

INSERT INTO areas (code, name) VALUES
('A', 'Ambiental'),
('S', 'Social'),
('G', 'Gobernanza');



-- =========================================================
-- 5. TABLA DE NIVELES DE MADUREZ
-- =========================================================
CREATE TABLE levels (
    id SERIAL PRIMARY KEY,
    key VARCHAR(50) UNIQUE NOT NULL,     -- basic, intermediate, advanced
    label VARCHAR(50) NOT NULL,          -- Básico / Intermedio / Avanzado
    score NUMERIC NOT NULL               -- 6 / 8 / 10
);

INSERT INTO levels (key, label, score) VALUES
('basic', 'Básico', 6),
('intermediate', 'Intermedio', 8),
('advanced', 'Avanzado', 10);



-- =========================================================
-- 6. TABLA DE INDICADORES (PREGUNTAS)
-- =========================================================
CREATE TABLE indicators (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    area_id INTEGER NOT NULL REFERENCES areas(id),

    question TEXT NOT NULL,
    display_order INTEGER DEFAULT 0,
    active BOOLEAN DEFAULT TRUE,

    created_by UUID REFERENCES users(id) ON DELETE SET NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);



-- =========================================================
-- 7. TABLA DE EVALUACIONES (SEMESTRALES)
-- =========================================================
CREATE TABLE evaluations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    company_id UUID NOT NULL REFERENCES companies(id) ON DELETE CASCADE,

    year INTEGER NOT NULL,
    semester INTEGER NOT NULL CHECK (semester IN (1, 2)),

    created_by UUID REFERENCES users(id),
    created_at TIMESTAMP DEFAULT NOW(),

    UNIQUE (company_id, year, semester)  -- una evaluación por semestre
);



-- =========================================================
-- 8. TABLA DE RESPUESTAS
-- =========================================================
CREATE TABLE answers (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    evaluation_id UUID NOT NULL REFERENCES evaluations(id) ON DELETE CASCADE,
    indicator_id UUID NOT NULL REFERENCES indicators(id),

    level_id INTEGER NOT NULL REFERENCES levels(id),
    numeric_value NUMERIC NOT NULL,   -- 6, 8 o 10

    created_at TIMESTAMP DEFAULT NOW(),

    UNIQUE (evaluation_id, indicator_id)
);



-- =========================================================
-- 9. TABLA DE ESTADÍSTICAS (PROMEDIOS CALCULADOS)
-- =========================================================
CREATE TABLE evaluation_stats (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    evaluation_id UUID UNIQUE NOT NULL REFERENCES evaluations(id) ON DELETE CASCADE,

    avg_environmental NUMERIC,
    avg_social NUMERIC,
    avg_governance NUMERIC,
    avg_global NUMERIC,

    classification_environmental VARCHAR(50),
    classification_social VARCHAR(50),
    classification_governance VARCHAR(50),
    classification_global VARCHAR(50),

    calculated_at TIMESTAMP DEFAULT NOW()
);
