-- Create the 'ideas' table
CREATE TABLE ideas (
    idea_id SERIAL PRIMARY KEY,
    idea TEXT
);

-- Create the 'prompts' table
CREATE TABLE prompts (
    prompt_id SERIAL PRIMARY KEY,
    idea_id INT REFERENCES ideas(idea_id),
    prompt TEXT
);

-- Create the 'suggestions' table with foreign key references
CREATE TABLE suggestions (
    suggestion_id SERIAL PRIMARY KEY,
    prompt_id INT REFERENCES prompts(prompt_id),
    caption TEXT,
    image_link TEXT
);
