-- Create the 'ideas' table
CREATE TABLE post_ideas (
    post_idea_id SERIAL PRIMARY KEY,
    idea TEXT,
    update_time TIMESTAMP DEFAULT NOW(),
    status TEXT
);

-- Create the 'prompts' table
CREATE TABLE prompts (
    prompt_id SERIAL PRIMARY KEY,
    post_idea_id INT REFERENCES post_ideas(post_idea_id),
    prompt TEXT,
    update_time TIMESTAMP DEFAULT NOW(),
    status TEXT
);

-- Create the 'suggestions' table with foreign key references
CREATE TABLE post_suggestions (
    suggestion_id SERIAL PRIMARY KEY,
    prompt_id INT REFERENCES prompts(prompt_id),
    caption TEXT,
    image_link TEXT,
    update_time TIMESTAMP DEFAULT NOW(),
    status TEXT
);
