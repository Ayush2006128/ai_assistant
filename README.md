# coolGemini

coolGemini is an AI-powered assistant application built using Streamlit. It provides a chat interface powered by Google Gemini and search capabilities using Tavily and YouTube APIs. The app is designed for educational purposes and demonstrates the integration of multiple APIs to create a seamless user experience.

## Features

- **Chat AI Assistant**: Interact with an AI assistant powered by Google Gemini.
- **Search Engine**: Perform web searches using Tavily API and video searches using YouTube Data API.
- **Multi-tab Interface**: View results categorized into All, Images, Videos, and Web tabs.

## Technologies Used

- **Streamlit**: For building the web application.
- **Google Gemini API**: For AI chat functionality.
- **Tavily API**: For web search functionality.
- **YouTube Data API**: For video search functionality.
- **LangChain**: For managing AI agent interactions.

## Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd ai_assistant
   ```

2. Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the project root and add the following environment variables:
   ```env
   GOOGLE_API_KEY=<your_google_api_key>
   TAVILY_API_KEY=<your_tavily_api_key>
   YOUTUBE_API_KEY=<your_youtube_api_key>
   MODEL_NAME=gemini-2.0-flash
   TEMPERATURE=0.8
   ```

4. Run the application:
   ```bash
   streamlit run main.py
   ```

## Usage

- Navigate to the chat page to interact with the AI assistant.
- Use the search page to perform web and video searches.
- Visit the about page to learn more about the application.

## License

This application is licensed under the BSD 3-Clause License. See the LICENSE file for details.

## Disclaimer

This application is for educational purposes only and is not affiliated with Google or Tavily.