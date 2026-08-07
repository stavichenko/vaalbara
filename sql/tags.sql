-- =====================================================
-- TAG
-- =====================================================

CREATE TABLE tag (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

    name TEXT NOT NULL,

    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),

    UNIQUE (name)
);


-- =====================================================
-- USER_TAG (many-to-many)
-- =====================================================

CREATE TABLE user_tag (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

    user_id UUID NOT NULL
        REFERENCES "user"(id)
        ON DELETE CASCADE,

    tag_id UUID NOT NULL
        REFERENCES tag(id)
        ON DELETE CASCADE,

    UNIQUE (user_id, tag_id)
);

CREATE INDEX idx_user_tag_user
    ON user_tag(user_id);

CREATE INDEX idx_user_tag_tag
    ON user_tag(tag_id);


-- =====================================================
-- IDEA_TAG (many-to-many)
-- =====================================================

CREATE TABLE idea_tag (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

    idea_id UUID NOT NULL
        REFERENCES idea(id)
        ON DELETE CASCADE,

    tag_id UUID NOT NULL
        REFERENCES tag(id)
        ON DELETE CASCADE,

    UNIQUE (idea_id, tag_id)
);

CREATE INDEX idx_idea_tag_idea
    ON idea_tag(idea_id);

CREATE INDEX idx_idea_tag_tag
    ON idea_tag(tag_id);


-- =====================================================
-- INITIATIVE_TAG (many-to-many)
-- =====================================================

CREATE TABLE initiative_tag (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),

    initiative_id UUID NOT NULL
        REFERENCES initiative(id)
        ON DELETE CASCADE,

    tag_id UUID NOT NULL
        REFERENCES tag(id)
        ON DELETE CASCADE,

    UNIQUE (initiative_id, tag_id)
);

CREATE INDEX idx_initiative_tag_initiative
    ON initiative_tag(initiative_id);

CREATE INDEX idx_initiative_tag_tag
    ON initiative_tag(tag_id);