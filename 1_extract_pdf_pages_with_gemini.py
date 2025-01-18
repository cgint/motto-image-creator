# %%
# Copyright 2023 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# %% [markdown]
# ## Identifying Relevant Pages in a PDF using Gemini 1.5
# 
# The goal of this notebook is to extract specific information from a large PDF by using Gemini to identify relevant pages and create a new, focused PDF.
# 
# In this notebook, you will:
#  - Use Gemini to identify pages in a large PDF that contain information about a given question.
#  - Extract and compile the identified pages into a new PDF.
#  - Save the PDF to a file

# %%
# Install python packages
# ! pip install -U pypdf
# ! pip install -U google-cloud-aiplatform
# ! pip install -U pdf2image

# %%
# Import all the required python packages
import io
import json
import pypdf
import vertexai

from pdf2image import convert_from_bytes
from IPython.display import display
from typing import Iterable

from vertexai.preview.generative_models import (
    GenerationResponse,
    GenerativeModel,
    HarmBlockThreshold,
    HarmCategory,
    Part
)

# %% [markdown]
# Include information about your project in the next cell.

# %%
PROJECT_ID = "gen-lang-client-0910640178"  # Replace with your project ID
LOCATION = "europe-west1"  # Replace with your location
MODEL_NAME = "gemini-1.5-flash-002"

vertexai.init(project=PROJECT_ID, location=LOCATION)
model = GenerativeModel(MODEL_NAME)
BLOCK_LEVEL = HarmBlockThreshold.BLOCK_ONLY_HIGH

# %% [markdown]
# The following is the prompt used to extract the pages related to the question.

# %%
PROMPT_PAGES = """
Return the numbers of all pages in the document above that contain information related to the question below.
<Instructions>
 - Use the document above as your only source of information to determine which pages are related to the question below.
 - Return the page numbers of the document above that are related to the question. When in doubt, return the page anyway.
 - The response should be a JSON list, as shown in the example below.
</Instructions>
<Suggestions>
 - The document above is a financial report with various tables, charts, infographics, lists, and additional text information.
 - Pay CLOSE ATTENTION to the chart legends and chart COLORS to determine the pages. Colors may indicate which information is important for determining the pages.
 - The color of the chart legends represents the color of the bars in the chart.
 - Use ONLY this document as context to determine the pages.
 - In most cases, the page number can be found in the footer.
</Suggestions>
<Question>
{question}
</Question>
<Example JSON Output>
{{
  "pages": [1, 2, 3, 4, 5]
}}
</Example JSON Output>
json:"""

# %%
def pdf_cut(pdf_bytes: bytes, pages: list[int]) -> bytes:
    """Using the pdf bytes and a list of page numbers,
    return the pdf bytes of a new pdf with only those pages
    Args:
        pdf_bytes:
            Bytes of a pdf file
        pages:
            List of page numbers to extract from the pdf bytes
    Returns:
        Bytes of a new pdf with only the extracted pages
    """
    pdf_reader = pypdf.PdfReader(io.BytesIO(pdf_bytes))
    pdf_writer = pypdf.PdfWriter()
    for page in pages:
        try:
            pdf_writer.add_page(pdf_reader.pages[page - 1])
        except Exception as e:
            pass
    output = io.BytesIO()
    pdf_writer.write(output)
    return output.getvalue()

# %%
def generate(
    prompt: list,
    max_output_tokens: int = 2048,
    temperature: int = 2,
    top_p: float = 0.4,
    stream: bool = False,
) -> GenerationResponse | Iterable[GenerationResponse]:
    """
    Function to generate response using Gemini 1.5 Pro

    Args:
        prompt:
            List of prompt parts
        max_output_tokens:
            Max Output tokens
        temperature:
            Temperature for the model
        top_p:
            Top-p for the model
        stream:
            Strem results?

    Returns:
        Model response

    """
    responses = model.generate_content(
        prompt,
        generation_config={
            "max_output_tokens": max_output_tokens,
            "temperature": temperature,
            "top_p": top_p,
        },
        safety_settings={
            HarmCategory.HARM_CATEGORY_HATE_SPEECH: BLOCK_LEVEL,
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: BLOCK_LEVEL,
            HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: BLOCK_LEVEL,
            HarmCategory.HARM_CATEGORY_HARASSMENT: BLOCK_LEVEL,
        },
        stream=stream
    )

    return responses

# %%
def pdf_pages(
    question: str, 
    pdf_bytes: bytes, 
    instructions_prompt: str = PROMPT_PAGES
) -> list[int]:
    """
    Function to generate a list of page numbers with pdf bytes and a question

    Args:
        question:
            Question to ask the model
        pdf_bytes:
            PDF bytes
        instructions_prompt:
            Prompt for the model

    Returns:
        List of page numbers
    """
    pdf_document = Part.from_data(data=pdf_bytes, mime_type="application/pdf")
    prompt = [
        "<Document>",
        pdf_document,
        "</Document>",
        instructions_prompt.format(question=question),
    ]
    responses = generate(prompt=prompt)
    print("Responses:", str(responses))

    if isinstance(responses, GenerationResponse):
        output_text  = responses.text
    else:
        output_text = " ".join([response.text for response in responses])
    output_text = output_text.replace("```json", "").replace("```", "").strip()
    output_json = json.loads(output_text)
    return output_json["pages"]

# %% [markdown]
# In the next cell, include information about your question and the pdf_path.  
# 
# **(Optional)**  
# If you are using Colab to test this notebook, you can try the following code to upload your PDF files.  
# ```python
# from google.colab import files
# files.upload()
# ```
# 
# You can uncomment the code in the cell to use this method.

# %%
# from google.colab import files
# files.upload()

# %%
# Include your question and the path to your PDF
# question = "What are the key trends for financial services industry?"
question = "What was bought and from whom?"
pdf_path = "./data/Inbox/1f5763e9-e15f-51ba-8703-d61ee0780582.pdf"

# %%
# Open the file, extract the pages using Gemini 1.5 and print them
with open(pdf_path, "rb") as f:
    pdf_bytes = f.read()
pages = pdf_pages(question=question, pdf_bytes=pdf_bytes)
print(pages)

# %%
# To ensure we find the answer to the question, it will also retrieve the page immediately after those.
expanded_pages = set(pages)
expanded_pages.update({i+1 for i in pages})
new_pdf = pdf_cut(pdf_bytes=pdf_bytes, pages=list(expanded_pages))

# %%
# Write the result to a new PDF document
with open("./sample.pdf", "wb") as fp:
    fp.write(new_pdf)

# %% [markdown]
# #### (Optional) Print the PDF pages

# %%
images = convert_from_bytes(new_pdf)
for i, image in enumerate(images):
    display(image)


