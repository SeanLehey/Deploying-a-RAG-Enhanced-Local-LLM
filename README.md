# Deploying a RAG-Enhanced Local LLM
_Project Completed in February 2026_

> [!NOTE]
> I developed the code in this project collaboratively with Claude, which is one of many SaaS LLM products available to the public. I am not a software engineer and I do not claim to be an expert in Python. However, I believe it is important to understand the code Claude produces well enough to explain the function of each script and its constituent parts, rather than blindly run it as a black box solution. A more in-depth overview of my approach to AI tools can be found in my [AI ethics statement](https://github.com/SeanLehey/Personal-AI-Ethics-Statement). With that in mind, all of the planning, writing, iteration, and execution of this project was performed by me.

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
Extracting the contents of the .zip file we downloaded from Godot's documentation website yields 1,570 .html files, consisting of tutorials, references, and explanations of various elements of Godot and GDScript. These files are easily interpreted by browsers, but they're not so great for retrieval-augmented generation. They contain HTML markup tags which will pollute the plain, natural language we're aiming for as we prepare to eventually embed the data into a vector database. Using tools like beautifulsoup and markdownify, we can identify and prune these extraneous elements and convert the .html files into a more legible markdown format. Below are snippets of the same tutorial file before and after processing with `html_to_markdown.py`.

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

#### Chunking Strategy

Chunking is the act of splitting text into discrete "chunks" of related text. Chunking strategies vary depending on the nature of the data and the intended use case. For this project, we will be chunking the Godot documentation in a structure-based fashion rather than a fixed-size fashion. This is because the documentation is already logically separated into distinct sections, unlike other raw text sources which may not be. Additionally, due to the different formatting styles of `class` documentation versus `tutorial`, `getting started`, and other documentation types, we will be using separate chunking strategies for each group of files.

#### Execution

With our fully converted documentation files, we can now process those further by running our `chunk_and_embed` script. This script logically separates each file into a batch of chunks, embeds those chunks by assigning them unique numerical values, and then ingests those embeddings into LanceDB to be referenced by our LLM.

![ChunkAndEmbed](https://github.com/user-attachments/assets/c0411acc-669e-4da8-b4e2-ceee2695e3de)

Once the script has run, we will see a new `godot_docs.lance` file representing our vector database in our project folder. This is the beating heart of our RAG.

<img width="1180" height="387" alt="image" src="https://github.com/user-attachments/assets/a4e4a09a-8f08-41b6-ad49-d62df77c6245" />

## Step Three: Model Selection, Web Application, and Tying it all Together

Now is the time to download Ollama if you haven't already. The model we're using for this project is `qwen3-coder:30b`.

The two files we're using for this portion of the project are `query_server.py` and `interface.html`. The query server file contains the backend code enabling our model to interact with the visually-appealing local webapp represented by the interface file. The model's system prompt can be found in `query_server.py`. It reads as:

```
system_prompt = (
        "You are a helpful Godot game engine assistant. "
        "You are helping a developer who is coding in GDScript. "
        "Answer questions using only the provided documentation context. "
        "If the answer is not in the context, say so clearly."
    )
```

This can be edited to your liking if, for instance, you're using C# and have chunked the documentation appropriately for that language instead.

Open up a command prompt window, navigate to where the script is located, and type `python query_server.py`. After you do this, go ahead and open `interface.html` with a browser of your choice. You should be presented with the following.

<img width="2560" height="1600" alt="WebAppFirstLook" src="https://github.com/user-attachments/assets/a182aa29-53c5-410b-9e45-5bd1040d6557" />

The RAG allows us to ask questions about Godot and GDScript without laboriously providing language and engine context, a lengthy system prompt, and other time-wasters we'd encounter with an unspecialized LLM. Let's test it with our first basic question without mentioning the engine or language.

<img width="2560" height="1600" alt="image" src="https://github.com/user-attachments/assets/a44a2a60-1bf3-4169-a833-bd4818e2bffc" />

Voilà! Our local, RAG-assisted LLM is now working perfectly. Towards the bottom of the screen, we can even see the source documentation files the LLM is referencing thanks to the metadata we attached to the chunk via `chunk_and_embed.py`.

Let's ask it to produce some sample GDScript code.

<img width="2560" height="1600" alt="image" src="https://github.com/user-attachments/assets/25b35408-eb94-4e0e-8d37-8f9332129331" />

<img width="2559" height="1049" alt="image" src="https://github.com/user-attachments/assets/9f2cdbeb-3333-477f-904f-397904e294cc" />

As we can see, the LLM is providing legitimate GDScript code for implementing WASD movement for our 2D character. It even provides supplementary information on assigning input maps in the project settings - a crucial step and another indicator that our RAG is working as intended.

## Final Thoughts
In this project, we cleaned, chunked, embedded, and connected Godot's offline GDScript documentation repository to a local LLM, and demonstrated that it works as intended. The most important takeaway is that this methodology can be applied to other databases as well. Using textbooks, knowledge bases, and other long-form written content will achieve the same effect for various learning goals.

At the time of writing this in February of 2026, it's becoming clearer what role LLMs are going to play in the future of work. In my case, I utilize them to produce an initial codebase, and then iterate with my own input from that point forward according to the project plan I created. My next project will likely be an implementation of guardrails and supervisor agents for a local LLM, and then eventually creating custom alerting after setting up log ingestion with a tool like SOF ELK.

[Return to Sean's Profile](https://github.com/SeanLehey)
