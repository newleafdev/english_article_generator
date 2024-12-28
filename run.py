from app import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)

#TODO - apply changes to the app from the claude conversation, prompt engineering, export function, fix markdown display, ensure performance is okay (maybe as the LLM directly instead of via requests)