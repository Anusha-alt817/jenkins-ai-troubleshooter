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

            script {
                def logStatus

                withCredentials([
                    usernamePassword(
                        credentialsId: 'jenkins-api-creds',
                        usernameVariable: 'JENKINS_USER',
                        passwordVariable: 'JENKINS_TOKEN'
                    )
                ]) {
                    logStatus = sh(
                        returnStatus: true,
                        script: 'python3 scripts/jenkins_log_collector.py'
                    )
                }

                if (logStatus == 0) {
                    echo 'Jenkins logs collected successfully.'

                    def processorStatus = sh(
                        returnStatus: true,
                        script: '''
                            LOG_DIR="$WORKSPACE/logs" python3 scripts/log_processor.py
                        '''
                    )

                    if (processorStatus == 0) {
                        echo 'Jenkins log processing completed.'

                        def aiStatus = sh(
                            returnStatus: true,
                            script: '''
                                LOG_DIR="$WORKSPACE/logs" python3 scripts/ai_analyzer.py
                            '''
                        )

                        if (aiStatus == 0) {
                            echo 'AI incident analysis completed.'
                        } else {
                            echo 'WARNING: AI incident analysis failed.'
                        }
                    } else {
                        echo 'WARNING: Jenkins log processing failed.'
                    }
                } else {
                    echo 'WARNING: Jenkins log collection failed.'
                }
            }
        }
    }
}
