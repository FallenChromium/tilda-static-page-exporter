# Tilda Static Pages Exporter

This Python script exports static pages from a [Tilda.cc](https://tilda.cc) project using Tilda API and saves them locally to your server. It also listens to a webhook, so that your pages always remain up-to-date. You can use this script to host your website on your own server and synchronize it with the Tilda page builder.

**Note**: Exporting static pages from Tilda using the API requires a Tilda Business account.

## Prerequisites

- Python 3.7+
- A Tilda Business account
- Tilda API keys: public key and secret key
- Flask, requests dotenv and (optionally) gunicorn Python modules

## Installation

### Docker

You can use my `docker-compose.yml` to run this service in Docker.

The exported pages will be saved in `./static` directory inside the project folder (you can change that in `docker-compose.yml` in the `volumes` section)
1. Clone the repository to your server. 

    ```sh
    git clone https://github.com/FallenChromium/tilda-static-pages-exporter.git
    ```
1. Copy the `env.example` file to `.env` file and fill in the API keys and other parameters.
1. Run the service
    ```sh
    docker compose up -d
    ```
1. The service should become available at `http://your-ip:5000` (if you didn't change the default bind port in .env file). 

I recommend using the endpoint of this service from behind a reverse-proxy with HTTPS enabled, but it's up to you.

### Running manually
You would need to install the dependencies first: `pip3 isntall -r requirements.txt`

You can run my project in a one-off mode by running the script with the Tilda's "projectid" as an argument, for example:
```sh
python3 app.py 123123
```
To run it in a server mode use one of the WSGI servers, for example gunicorn:
```sh
gunicorn --bind 0.0.0.0:5000 'app:app' --timeout 90
```


## Usage

To export the static pages from a Tilda.cc project, you need to set up a webhook in your Tilda account that will call the server URL where the script is running. Here's how to do it:

1. Log in to your Tilda account and open the project you want to export.
2. Click the "Export project" button in the top-right corner.
3. In the "Export project" dialog, click the "Add webhook" button.
4. In the "Add webhook" dialog, enter the URL of your server followed by `/webhook` (e.g., `https://your-server.com/webhook`).
5. Click the "Add webhook" button to save the webhook.

Now, every time you publish some page in the project, Tilda will call your server URL with a `GET` request that includes the `projectid` parameter.

The script will then extract the project and its pages, saving the images, scripts, and styles to your server and creating HTML files for each page.

## Hosting

For this small adventure I've used Caddy web server to host the website (and to allow access to the Tilda page exporter too). Here's an example configuration that may help you too:

```
<your-domain> {
        reverse_proxy /webhook 127.0.0.1:5000
        root * <path-to-tilda-static-page-exporter>/static
        file_server {
                index <id_of_your_index_page>.html
        }
}
```


## Limitations
1. My script supports only one Tilda project at the moment. Adding support for multiple projects would probably require a full-fledged web server inside my script, and that's not what I needed for my task that made me write this script in the first place.
2. I do not personally use Tilda, but I thought that it'd be better to share my service with the world if someone else would have the same trouble as my friends did. Don't count on any updates if this script will become obsolete or Tilda will introduce breaking changes. Contributions are very welcome though!
3. This code isn't perfect, and it was not intended to. This solution to the problem was a part of an experiment, read on to know what's the deal ;)

## Acknowledgements
To be honest, this task was kinda boring, so I decided to check what are the capabilities of neural networks and whether they could help me in my day-to-day job. 

Turns out, they can help a lot! I've used ChatGPT to generate Python code, Dockerfiles, and even parts of this very README! This ended being tons of fun, though not without problems. Occasionally it would hit the token limit or lose context, and the code used outdated API URLs and methods (you can check it in the commit history, hahah), but generally speaking, all the bits that were not working properly were caused by the lack of information or context in a prompt that described the task. I am very impressed by the code which was generated literally in seconds.

You can read about this in detail in a separate [Chat.md](./Chat.md) file. All in all, even though sometimes it was cumbersome to get the good and correct code out of it, and I've had to employ some prompt hacks, ChatGPT saved me a lot of time during this project. I am going to embrace this tool in my day-to-day workflow and boost my productivity even more!

For those wondering: I am not afraid ChatGPT will replace me **in areas I am interested to work on**. The quality of the output is pretty much defined by the clarity of the input and the vision of the human, so you'll still need expertise to get good results. The thing is that you should never send a human to do a machine's job, and some aspects of coding are ready to become a machine's job. Don't trust everything into a machine's hands and be creative about what you do and you'll get great results! (And won't be replaced by a machine, too :D)
