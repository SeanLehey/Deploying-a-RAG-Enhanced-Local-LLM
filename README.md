# Configuring a Local LLM and Connecting it to a Retrieval Augmented Generation (RAG) Database
_Project Completed in February 2026_

> [!NOTE]
> The code in this project was developed collaboratively with Claude, Anthropic's AI assistant. I am not a software engineer and I do not claim to be an expert in Python. However, I believe it is important to understand the code Claude produces well enough to explain the function of each script and its constituent parts, rather than blindly run it as a black box solution. A more in-depth overview of my approach to AI tools can be found in my [AI ethics statement](https://github.com/SeanLehey/Personal-AI-Ethics-Statement). With that in mind, all of the planning, writing, code review, and execution of this project was done by me and my puny human fingers.

## Project Overview
Lately, I've been wanting to create a local AI assistant to help me with learning programming languages (in this case, GDScript). This project gives me the opportunity to learn more about the configuration and deployment of local AI models while building a handy tool I can use for my game development hobby. This writeup documents my experience learning about data cleaning, chunking, embedding, and creating a vector database to serve as a RAG for a local LLM. It's also a good exercise in planning and executing Python scripts in collaboration with a state-of-the-art SaaS LLM - in this case, Claude Sonnet 4.6. I aim to make this project as reproduceable as possible so readers can follow along in their own environments.

## Resources
* [Godot's Offline Documentation Repository](https://docs.godotengine.org/en/stable/index.html)
* [VSCode](https://code.visualstudio.com/)
* [Claude Sonnet 4.6](https://claude.ai/)

#### Python Libraries
* [markdownify](https://pypi.org/project/markdownify/)
* [beautifulsoup4](https://pypi.org/project/beautifulsoup4/)
* [sentence-transformers](https://pypi.org/project/sentence-transformers/)
* [lancedb](https://pypi.org/project/lancedb/)
* [ollama](https://pypi.org/project/ollama/)

## Step One: Cleaning the Data
Extracting the contents of the .zip file we downloaded from Godot's documentation website yields 1,570 .html files, consisting of tutorials, references, and explanations of various elements of Godot and GDScript. These files are easily interpreted by browsers, but not so great for large language models. They contain HTML markup tags which will pollute the plain, natural language we're aiming for as we prepare to eventually embed the data into a vector database. Using tools like beautifulsoup and markdownify, we can identify and prune these extraneous elements and convert the .html files into a more processable markdown format. Below are snippets of the same tutorial file before and after processing with `html_to_markdown.py`.

#### Raw HTML File

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

#### Processed File

```
# Creating the enemy

Now it's time to make the enemies our player will have to dodge. Their behavior
will not be very complex: mobs will spawn randomly at the edges of the screen,
choose a random direction, and move in a straight line.

We'll create a `Mob` scene, which we can then *instance* to create any number
of independent mobs in the game.
```

## Step Two: Chunking, Embedding, and Ingesting into LanceDB

With our fully converted documentation files, we can now process those further by running our `chunk_and_embed` script. This script logically separates each file into a batch of chunks, embeds those chunks by assigning them unique numerical values, and then ingests those embeddings into LanceDB to be referenced by our LLM.

![ChunkAndEmbed](https://github.com/user-attachments/assets/c0411acc-669e-4da8-b4e2-ceee2695e3de)

Once the script has run, we will see a new `godot_docs.lance` file representing our vector database in our project folder. This is the beating heart of our RAG.

<img width="1536" height="960" alt="LanceDBFolder" src="https://github.com/user-attachments/assets/f12679c7-540e-4dcb-9690-6a63297bccdf" />


## Step Three: 


