-- =========================
-- EXTENSIONS
-- =========================
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "citext";
CREATE EXTENSION IF NOT EXISTS postgis;

-- =========================
-- TABLE: user
-- =========================
CREATE TABLE "user" (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

    nickname TEXT NOT NULL,

    phone_num TEXT NOT NULL CHECK (
        phone_num ~ '^\+?[1-9]\d{7,14}$'
    ),
    phone_num_verified BOOLEAN NOT NULL DEFAULT FALSE,

    email CITEXT NOT NULL,
    email_verified BOOLEAN NOT NULL DEFAULT FALSE,

    karma INTEGER NOT NULL DEFAULT 0,

    image TEXT NOT NULL,

    first_name TEXT,
    second_name TEXT,
    last_name TEXT,
    qualification TEXT,

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    UNIQUE (nickname),
    UNIQUE (email),
    UNIQUE (phone_num)
);

-- =========================
-- TABLE: idea
-- =========================
CREATE TABLE idea (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

    title TEXT NOT NULL,
    description TEXT NOT NULL,

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    user_id UUID NOT NULL REFERENCES "user"(id),

    likes_count INTEGER NOT NULL DEFAULT 0 CHECK (likes_count >= 0),

    location GEOGRAPHY(POINT, 4326) NOT NULL,

    creator_is_manager BOOLEAN NOT NULL DEFAULT FALSE
);

CREATE INDEX idx_idea_user_id ON idea(user_id);
CREATE INDEX idx_idea_location ON idea USING GIST (location);

-- =========================
-- TABLE: initiative
-- =========================
CREATE TABLE initiative (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

    title TEXT NOT NULL,
    description TEXT NOT NULL,

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    user_id UUID NOT NULL REFERENCES "user"(id),
    manager_id UUID NOT NULL REFERENCES "user"(id),

    required_resources TEXT NOT NULL,

    location GEOGRAPHY(POINT, 4326) NOT NULL,

    deadline TIMESTAMPTZ
);

CREATE INDEX idx_initiative_user_id ON initiative(user_id);
CREATE INDEX idx_initiative_manager_id ON initiative(manager_id);
CREATE INDEX idx_initiative_location ON initiative USING GIST (location);

-- =========================
-- TABLE: user_initiative
-- =========================
CREATE TABLE user_initiative (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

    user_id UUID NOT NULL REFERENCES "user"(id) ON DELETE CASCADE,
    initiative_id UUID NOT NULL REFERENCES initiative(id) ON DELETE CASCADE,

    role TEXT NOT NULL,

    UNIQUE (user_id, initiative_id)
);

CREATE INDEX idx_user_initiative_user_id ON user_initiative(user_id);
CREATE INDEX idx_user_initiative_initiative_id ON user_initiative(initiative_id);