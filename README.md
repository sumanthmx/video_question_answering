### Installation

1. Get an API Key at [https://platform.openai.com/settings/organization/api-keys](https://platform.openai.com/settings/organization/api-keys)

2. Clone the repo
   ```sh
   git clone https://github.com/sumanthmx/video_question_answering
   ```
3. Open up one terminal for front-end and install npm packages
   ```sh
   npm install
   ```
4. Run the application front end
   ```sh
   npm run dev
   ```
5. Open up another terminal and use conda (or another means) to create a venv
   ```sh
   conda create -n vqa python=3.10
   ```
6. Activate your venv
   ```sh
   conda activate vqa
   ```
7. Install project requirement dependencies for the back end
   ```sh
   pip install -r requirements.txt
   ```
8. Enter your OPENAI_API_KEY through the terminal
   ```sh
   export OPENAI_API_KEY="your-api-key-here"
   ```
9. Run back end
   ```sh
   uvicorn main:app --reload
   ```
10. Open up web browser and find the app at localhost:3000. Enjoy

