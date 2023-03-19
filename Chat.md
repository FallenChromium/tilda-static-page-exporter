The staring prompt was as follows:

    "Hi! Could you please assist me in writing some Python code today? I want to use Tilda.cc API to export static pages and save them on my server for hosting them. I need a script that would listen on a webhook call and then execute the following instructions provided by Tilda:
    1. Get information on the project you need by sending the getprojectinfo request.
    2. Loop through the image array that you've received in the request response. There is a list of files in it. You can find the source address of the file in the from variable and the local name you need to use for saving the file in the to variable. Copy the files where you need to. These files are common for all the pages in the project.
    3. Get the list of all pages in our project by sending the getpageslist request.
    4. Loop through the page list you've received. For each page:
    4.1 Get the page information for export by sending the getpagefullexport request;
    4.2 Save images, scripts, and styles used on the page from the images, js, and css arrays to the server;
    5. Create a new page file (using the name from the filename variable) and fill it with the html variable value.

    The script should include comments, follow best practices and be simple to use and maintain"

From now on I've just asked for corrections and additions to the code which was generated, such as:

- 
    ```
    It looks great! Can you add the code that would read public and secret API keys from system environment variables?
    ```
- 
    ```
    Can you change the functions so that it would be possible to add a custom prefix to a `local_path` which can be set as a constant or as an env variable?
    ```
- 
    ```
    Can you generate a Dockerfile for this project?
    ```
- 
    ```
    Can you change the Dockerfile to use gunicorn as an entrypoint?
    ```
- 
    ```
    Nice! Can you generate a Docker Compose definition for it too?
    ```
- 
    ```
    Add best practices to the Dockerfile including preservation of pip cache (try to use BuildKit caches)
    ```
- 
    ```
    Try to minimize the weight of a resulting Docker image"
    ```
- 
    ```
    Refactor the code so that the files export for a given project will be a separate function called by the webhook handler"
    ```
- 
    ```
    Please correct the previous code considering the following information: *copied info from Tilda docs*" 
    ```
    (IT WORKED!)
- 
    ```
    Print the changed handle_webhook function condidering that the webhook uses GET HTTP request"
    ```
- 
    ```
    Can you generate a README for this project that would include usage recommendations and the mention that it was made with ChatGPT, including the successful prompts (including this one) that I've used for generation? (it actually failed to include the prompts, and the README was a bit weak)
    ```
- 
    ```
    Include a mention that using API requires Tilda Business account. Delete the instructions provided by Tilda. Change the instructions for installation so that it would use requirements.txt file that I've made. Use gunicorn in the start step. Include some prompts that I've used in this conversation" (Still bad, but it was a good base to build on top of)
    ```
