pipeline {
    agent any

    environment {
        IMAGE_NAME = 'jenkins-ai-troubleshooter'
    }

    stages {

        stage('Checkout') {
            steps {
                echo 'Source code checked out from GitHub'
            }
        }

        stage('Build and Test') {
            steps {
                dir('app') {
                    sh 'mvn clean test package'
                }
            }
        }

        stage('Docker Build') {
            steps {
                sh 'docker build -t ${IMAGE_NAME}:${BUILD_NUMBER} .'
                sh 'docker tag ${IMAGE_NAME}:${BUILD_NUMBER} ${IMAGE_NAME}:latest'
            }
        }
    }

    post {
        always {
            echo 'Jenkins pipeline execution completed.'
            echo "Build result: ${currentBuild.currentResult}"
        }
    }
}
