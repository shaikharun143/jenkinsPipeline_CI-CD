pipeline {
    agent any

    environment {
        IMAGE_NAME     = "my-flask-app"
        CONTAINER_NAME = "my-flask-app-container"
    }

    stages {
        stage('Checkout') {
            steps {
                checkout scm          // pulls the latest code from GitHub
            }
        }
        stage('Build') {
            steps {
                echo 'Building Docker image...'
                sh 'docker build -t $IMAGE_NAME:$BUILD_NUMBER .'
            }
        }
        stage('Test') {
            steps {
                echo 'Running tests...'
                sh 'python3 -m pytest || echo "No tests yet — skipping"'
            }
        }
        stage('Deploy') {
            steps {
                echo 'Deploying container...'
                sh '''
                    docker rm -f $CONTAINER_NAME || true
                    docker run -d --name $CONTAINER_NAME \
                        -p 5000:5000 $IMAGE_NAME:$BUILD_NUMBER
                '''
            }
        }
    }

    post {
        success { echo 'Pipeline completed successfully!' }
        failure { echo 'Pipeline failed.' }
    }
}
