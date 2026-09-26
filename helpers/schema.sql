CREATE TABLE IF NOT EXISTS jobs(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    job_id TEXT NOT NULL,
    provider TEXT NOT NULL,
    title TEXT DEFAULT no_title_available,
    description TEXT DEFAULT no_description_available, 
    link TEXT NOT NULL,
    applied INTEGER NOT NULL DEFAULT 0 CHECK(applied IN (0,1)),
    showable INTEGER NOT NULL DEFAULT 0 CHECK(applied IN (0,1)),
    date DATETIME DEFAULT CURRENT_TIMESTAMP,

    UNIQUE(job_id,provider)
);