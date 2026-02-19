# Configuring a Local LLM and Connecting it to a Retrieval Augmented Generation (RAG) Database
Creating my GDScript coding companion

## Why Am I Doing This?
I want a local coding assistant to assist me with learning programming languages (in this case, GDScript). This project gives me the opportunity to learn more about the configuration and deployment of local AI models while building towards a useful tool I can use for my game development hobby. This writeup documents my experience learning about data cleaning, chunking, embedding, and creating a vector database to serve as a RAG for a local LLM. I aim to make it as reproduceable as possible so readers can follow along in their own environments.

## Resources
* [Godot's Offline Documentation Repository](https://docs.godotengine.org/en/stable/index.html)
* [Markdownify Python Library](https://pypi.org/project/markdownify/)
* [Beautifulsoup Python Library](https://pypi.org/project/beautifulsoup4/)
* [ChromaDB](https://www.trychroma.com/)

## Step One: Cleaning the Data
Extracting the contents of the .zip file we downloaded from Godot's documentation website yields 1,570 .html files, consisting of tutorials, references, and explanations of various elements of Godot and GDScript. These files are easily interpreted by browsers, but not so great for large language models. They contain HTML markup tags which will pollute the plain, natural language we're aiming for in our vector database. Using tools like beautifulsoup and markdownify, we can identify and prune these extraneous elements and convert the .html files into a more processable markdown format. Below are snippets of the same file before and after processing with `html_to_markdown.py`.

#### Raw HTML File:

```
<!DOCTYPE html>
<html class="writer-html5" lang="en" data-content_root="../../">
<head>
  <meta charset="utf-8" /><meta name="viewport" content="width=device-width, initial-scale=1" />
<meta property="og:title" content="Creating the enemy" />
<meta property="og:type" content="website" />
<meta property="og:url" content="getting_started/first_2d_game/04.creating_the_enemy.html" />
<meta property="og:site_name" content="Godot Engine documentation" />
<meta property="og:description" content="Now it&#x27;s time to make the enemies our player will have
to dodge. Their behavior will not be very complex: mobs will spawn randomly at the edges of the screen,
choose a random direction, and mo..." />
<meta name="description" content="Now it&#x27;s time to make the enemies our player will have to dodge.
Their behavior will not be very complex: mobs will spawn randomly at the edges of the screen, choose a
random direction, and mo..." />
```

#### Processing...

![ConvertingHTMLtoMD](https://github.com/user-attachments/assets/e5c5a8c6-e163-412a-9db8-567f3fb054bc)

#### Processed File:

```
# Creating the enemy

Now it's time to make the enemies our player will have to dodge. Their behavior
will not be very complex: mobs will spawn randomly at the edges of the screen,
choose a random direction, and move in a straight line.

We'll create a `Mob` scene, which we can then *instance* to create any number
of independent mobs in the game.
```




