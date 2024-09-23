CREATE TABLE IF NOT EXISTS mainmenu (
    id SERIAL PRIMARY KEY,
    title text NOT NULL,
    url text NOT NULL
);

CREATE TABLE IF NOT EXISTS posts (
    id SERIAL PRIMARY KEY,
    title text NOT NULL,
    text text NOT NULL,
    time integer NOT NULL
);