CREATE TABLE "legal_text" (
  "id" serial primary key,
  "url" varchar(255),
  "title" varchar(255),
  "row_text" text,
  "row_vector" vector(768)
);