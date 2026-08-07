-- =====================================================
-- EXTENSIONS
-- =====================================================

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "citext";
CREATE EXTENSION IF NOT EXISTS postgis;


-- =====================================================
-- USER
-- =====================================================

CREATE TABLE "user" (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

    nickname TEXT NOT NULL,

    phone_num TEXT NOT NULL
        CHECK (phone_num ~ '^\+?[1-9]\d{7,14}$'),
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


-- =====================================================
-- IDEA
-- =====================================================

CREATE TABLE idea (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

    title TEXT NOT NULL,
    description TEXT NOT NULL,

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    archived_at TIMESTAMPTZ,

    user_id UUID NOT NULL
        REFERENCES "user"(id),

    votes_count INTEGER NOT NULL DEFAULT 0
        CHECK (votes_count >= 0),

    creator_is_manager BOOLEAN NOT NULL DEFAULT FALSE,

    location GEOGRAPHY(POINT, 4326) NOT NULL,

    is_worldwide BOOLEAN NOT NULL DEFAULT FALSE

);

CREATE INDEX idx_idea_active_created_at
    ON idea (created_at DESC)
    WHERE archived_at IS NULL;

CREATE INDEX idx_idea_active_user
    ON idea (user_id)
    WHERE archived_at IS NULL;

CREATE INDEX idx_idea_active_location
    ON idea
    USING GIST (location)
    WHERE archived_at IS NULL;


-- =====================================================
-- INITIATIVE
-- =====================================================

CREATE TABLE initiative (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

    title TEXT NOT NULL,
    description TEXT NOT NULL,

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    archived_at TIMESTAMPTZ,

    user_id UUID NOT NULL
        REFERENCES "user"(id),

    manager_id UUID NOT NULL
        REFERENCES "user"(id),

    required_resources TEXT NOT NULL,

    deadline TIMESTAMPTZ,

    location GEOGRAPHY(POINT, 4326) NOT NULL,

    is_worldwide BOOLEAN NOT NULL DEFAULT FALSE
);

CREATE INDEX idx_initiative_active_created_at
    ON initiative (created_at DESC)
    WHERE archived_at IS NULL;

CREATE INDEX idx_initiative_active_user
    ON initiative (user_id)
    WHERE archived_at IS NULL;

CREATE INDEX idx_initiative_active_manager
    ON initiative (manager_id)
    WHERE archived_at IS NULL;

CREATE INDEX idx_initiative_active_location
    ON initiative
    USING GIST (location)
    WHERE archived_at IS NULL;


-- =====================================================
-- USER_INITIATIVE
-- =====================================================

CREATE TABLE user_initiative (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

    user_id UUID NOT NULL
        REFERENCES "user"(id)
        ON DELETE CASCADE,

    initiative_id UUID NOT NULL
        REFERENCES initiative(id)
        ON DELETE CASCADE,

    role TEXT NOT NULL,

    UNIQUE (user_id, initiative_id)
);

CREATE INDEX idx_user_initiative_user
    ON user_initiative(user_id);

CREATE INDEX idx_user_initiative_initiative
    ON user_initiative(initiative_id);


-- =====================================================
-- IDEA_VOTE
-- =====================================================

CREATE TABLE vote_idea (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

    idea_id UUID NOT NULL
        REFERENCES idea(id)
        ON DELETE CASCADE,

    user_id UUID NOT NULL
        REFERENCES "user"(id)
        ON DELETE CASCADE,

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    UNIQUE (idea_id, user_id)
);

CREATE INDEX idx_vote_idea_idea
    ON vote_idea (idea_id);

CREATE INDEX idx_vote_idea_user
    ON vote_idea (user_id);


-- =====================================================
-- TRIGGER FUNCTION
-- =====================================================

CREATE OR REPLACE FUNCTION update_vote_ideas_count()
RETURNS TRIGGER AS
$$
BEGIN
    IF TG_OP = 'INSERT' THEN
        UPDATE idea
        SET votes_count = votes_count + 1
        WHERE id = NEW.idea_id;

        RETURN NEW;

    ELSIF TG_OP = 'DELETE' THEN
        UPDATE idea
        SET votes_count = GREATEST(votes_count - 1, 0)
        WHERE id = OLD.idea_id;

        RETURN OLD;
    END IF;

    RETURN NULL;
END;
$$ LANGUAGE plpgsql;


-- =====================================================
-- TRIGGERS
-- =====================================================

CREATE TRIGGER trg_vote_idea_insert
AFTER INSERT ON vote_idea
FOR EACH ROW
EXECUTE FUNCTION update_vote_ideas_count();


CREATE TRIGGER trg_vote_idea_delete
AFTER DELETE ON vote_idea
FOR EACH ROW
EXECUTE FUNCTION update_vote_ideas_count();