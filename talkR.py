from flask import Flask, render_template_string, request, redirect, url_for
import pyttsx3
import threading

def create_engine():
    engine = pyttsx3.init('sapi5')
    engine.setProperty('rate', 150)  # Set speaking rate
    engine.setProperty('volume', 1.0)  # Set volume
    return engine
    
app = Flask(__name__)
@app.route('/')
def index():
    html_content = '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Flask Text-to-Speech</title>
        <style>
            /* From Uiverse.io by gharsh11032000 */
            .card {
                position: relative;
                display: flex;
                align-items: center;
                justify-content: center;
                width: 320px;
                padding: 2px;
                border-radius: 24px;
                overflow: hidden;
                line-height: 1.6;
                transition: all 0.48s cubic-bezier(0.23, 1, 0.32, 1);
            }

            .content {
                display: flex;
                flex-direction: column;
                align-items: flex-start;
                gap: 24px;
                padding: 34px;
                border-radius: 22px;
                color: #ffffff;
                overflow: hidden;
                background: #ffffff;
                transition: all 0.48s cubic-bezier(0.23, 1, 0.32, 1);
            }

            .content .heading {
                font-weight: 700;
                font-size: 36px;
                line-height: 1.3;
                z-index: 1;
                transition: all 0.48s cubic-bezier(0.23, 1, 0.32, 1);
            }

            .content .para {
                z-index: 1;
                opacity: 0.8;
                font-size: 18px;
                transition: all 0.48s cubic-bezier(0.23, 1, 0.32, 1);
            }

            .card::before {
                content: "";
                position: absolute;
                height: 160%;
                width: 160%;
                border-radius: inherit;
                background: #0a3cff;
                background: linear-gradient(to right, #0a3cff, #0a3cff);
                transform-origin: center;
                animation: moving 4.8s linear infinite;
                transition: all 0.88s cubic-bezier(0.23, 1, 0.32, 1);
            }

            .card:not(:hover)::before {
                animation-play-state: paused;
            }

            .card:hover::before {
                animation-play-state: running;
                z-index: -1;
                width: 20%;
            }

            .card:hover .content .heading,
            .card:hover .content .para {
                color: #000000;
            }

            .card:hover {
                box-shadow: 0rem 6px 13px rgba(10, 60, 255, 0.1),
                    0rem 24px 24px rgba(10, 60, 255, 0.09),
                    0rem 55px 33px rgba(10, 60, 255, 0.05),
                    0rem 97px 39px rgba(10, 60, 255, 0.01), 0rem 152px 43px rgba(10, 60, 255, 0);
                scale: 1.05;
                color: #000000;
            }

            @keyframes moving {
                0% {
                    transform: rotate(0);
                }

                100% {
                    transform: rotate(360deg);
                }
            }

            .container {
                display: flex;
                flex-direction: column;
                align-items: center;
                justify-content: center;
                height: 100vh;
                background-color: #f4f4f4;
            }

            .input-field, .button-field {
                margin: 10px;
            }

            .input-field input {
                width: 100px;
                height: 100px;
                text-align: center;
            }

            .main-heading {
                font-size: 48px;
                font-weight: bold;
                margin-bottom: 20px;
            }

            .sub-heading {
                font-size: 24px;
                margin-bottom: 40px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="main-heading">TalkR.io</div>
            <div class="sub-heading">hover</div>
            <div class="card">
                <div class="content">
                    <form action="/speak" method="post">
                        <div class="input-field">
                            <input type="text" name="text" placeholder="Enter text" required>
                        </div>
                        <div class="button-field">
                            <button class="btn" type="submit">Speak</button>
                        </div>
                    </form>
                </div>
            </div>
        </div>
    </body>
    </html>
    '''
    return render_template_string(html_content)

@app.route('/speak', methods=['POST'])
def speak():
    text = request.form['text']
    threading.Thread(target=run_tts, args=(text,)).start()
    return redirect(url_for('result'))

@app.route('/result')
def result():
    html_content = '''
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Speech Synthesis Result</title>
    </head>
    <body>
        <h1>Speech synthesis in progress!</h1>
        <a href="/">Go Back</a>
    </body>
    </html>
    '''
    return render_template_string(html_content)

def run_tts(text):
    engine = create_engine()
    engine.say(text)
    engine.runAndWait()

if __name__ == '__main__':
    app.run(debug=True)
