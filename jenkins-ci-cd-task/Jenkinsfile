pipeline {
    agent any

    stages {
        stage('Preparation') {
            steps {
                bat 'echo Preparing workspace...'
            }
        }

        stage('Build') {
            steps {
                bat 'echo Build step - Static HTML, nothing to compile.'
            }
        }

        stage('Deploy') {
            steps {
                bat 'echo Starting server on http://localhost:8081'
                bat 'start /min cmd /c "python -m http.server 8081 --directory app"'
            }
        }
    }
}
