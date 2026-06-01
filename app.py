from flask import Flask

app = Flask(__name__)

# ---------------- HOME ----------------
@app.route("/")
def home():
    return """
    <html>
    <head>
        <title>DevOps Portfolio</title>
    </head>
    <body style="font-family:Arial; text-align:center; margin-top:50px;">
        <h1>🚀 Welcome to My DevOps Portfolio</h1>
        <p>I am a DevOps Engineer passionate about CI/CD, Docker, and Cloud.</p>

        <a href="/about">About</a> |
        <a href="/contact">Contact</a>
    </body>
    </html>
    """

# ---------------- ABOUT ----------------
@app.route("/about")
def about():
    return """
    <html>
    <head>
        <title>About Me</title>
    </head>
    <body style="font-family:Arial; text-align:center; margin-top:50px;">
        <h1>👨‍💻 About Me</h1>
        <p>I build CI/CD pipelines using Jenkins, Docker, GitHub Actions, and AWS.</p>
        <p>Skills: Linux, Docker, Jenkins, Kubernetes, AWS</p>

        <a href="/">Home</a> |
        <a href="/contact">Contact</a>
    </body>
    </html>
    """

# ---------------- CONTACT ----------------
@app.route("/contact")
def contact():
    return """
    <html>
    <head>
        <title>Contact</title>
    </head>
    <body style="font-family:Arial; text-align:center; margin-top:50px;">
        <h1>📞 Contact Me</h1>
        <p>Email: devops@example.com</p>
        <p>GitHub: https://github.com/your-profile</p>
        <p>LinkedIn: https://linkedin.com/in/your-profile</p>

        <a href="/">Home</a> |
        <a href="/about">About</a>
    </body>
    </html>
    """

# ---------------- RUN APP ----------------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
