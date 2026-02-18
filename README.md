# Configuring a Local LLM and Connecting it to a Retrieval Augmented Generation (RAG) Database
Creating my GDScript coding companion

## Project Synopsis
For this project, I will be downloading Godot's offline documentation for their GDScript coding language. I will then clean that data, separate it logically into chunks, embed those chunks, and create a vector database which a locally-run LLM will reference in its role as my coding assistant.

## Tools
#### Python Libraries
markdownify

## Hardware Requirements
Generally, you'll be able to run better models with better hardware. Similar results can be achieved on less powerful systems via quantization and other methods, but I recommend you use the latest GPU you can comfortably afford. My laptop for this project has the following specifications:

Intel Core Ultra 9 275HX Processor
Nvidia GeForce RTX 5090 24GB (Mobile version, which is roughly equivalent to a desktop 4070/4080)
64GB DDR5 RAM
2TB SSD

## Why Use a RAG?
The data with which Large Language Models (LLMs) are trained is typically outdated by the time the LLM releases, especially when that data is a living, evolving programming language. An update from Godot 4.3 to 4.4 can introduce many changes which may not be accounted for by the data that the LLM was trained on. With a RAG, the LLM can reference the latest documentation and avoid providing inaccurate and out-of-date information.

## Downloading the GDScript Documentation
For this project, our RAG will be Godot's GDScript documentation - specifically, an offline copy. This is available on Godot's website at https://docs.godotengine.org/en/stable/index.html. See below for relevant section:

<img width="1580" height="222" alt="GodotDocumentationDownload" src="https://github.com/user-attachments/assets/d190644a-0feb-4bc3-9688-debec75cbb32" />

Selecting the _Stable_ option downloads a file called _godot-docs-html-stable.zip_.


## Cleaning the Data
Due to the nature of how LLMs retrieve data, our strategy will involve converting this documentation database into a vector database. Our current dataset is almost entirely formatted in HTML, which includes tags and elements that may be useful for a web browser, but represent superfluous noise to an LLM. The `html_to_markdown.py` script uses Beautifulsoup and markdownify to sanitize the HTML elements and convert the .html files into a clean markdown format.

https://github.com/user-attachments/assets/6aeb3978-489a-4fab-9c34-2cc5478cfcc1




